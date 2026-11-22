"""
solar_photon_flux.py  (Team Omega)

Hourly clear-sky solar photon flux (photons per m^2 per hour) on a horizontal
surface for any latitude/longitude, date and hour interval, plus a ready-made
table for the 10 iFlex municipalities that joins onto combined_data.parquet.

Requirements:  pip install polars pvlib      (pvlib pulls in scipy, h5py, pandas)

Quick use
---------
    from solar_photon_flux import photon_flux, municipality_flux_table

    # One location, one date, hours 9-15 (Hour 9 = 08:00-09:00 local)
    photon_flux(59.9139, 10.7522, "2020-06-21", hours=range(9, 16))

    # Named iFlex location, a date range
    photon_flux(location="Tromsø", dates=("2020-12-01", "2020-12-31"))

    # Table for all 10 municipalities, then join to the hourly data
    flux = municipality_flux_table("2020-01-06", "2021-03-26")
    hourly = pl.scan_parquet("Data/combined_data.parquet")
    hourly = hourly.join(flux.lazy(), on=["Municipality", "Date", "Hour"], how="left")

Method
------
1. Sun position (NREL SPA via pvlib) and clear-sky global horizontal irradiance
   GHI (W/m^2) from the Ineichen-Perez model, using pvlib's monthly Linke
   turbidity climatology for the site and the site altitude.
2. GHI is sampled every minute (bin midpoints) and summed to energy per hour
   (J/m^2 per hour; also reported as Wh/m^2).
3. Energy is converted to photons with a fixed photons-per-joule factor taken
   from the ASTM G173-03 global (AM1.5) reference spectrum, 280-4000 nm:
     full spectrum : 4.304e18 photons per J
     PAR 400-700 nm: 1.191e18 photons per J of total GHI
                     (PAR = 43.0 % of energy; 4.60 umol/J of PAR energy,
                      i.e. 1.977 umol photons per J of GHI)
   Photon count = energy x factor.  PAR is also given in mol/m^2 per hour.

Conventions matching combined_data.parquet
------------------------------------------
* Hour h (1-24) = local wall-clock interval [h-1, h) in Europe/Oslo.
  Note: the `From` column is labelled UTC but is really Norwegian local time;
  Date + Hour are the safe keys to join on.
* DST: on the spring-forward day local hour 3 does not exist (no row); on the
  fall-back day local hour 3 contains two real hours. No experiment day in
  combined_data falls on a DST changeover, so this does not affect the join.

Assumptions / limits (state these in the write-up)
------------------------------------------------
* CLEAR SKY: no clouds. This is the potential sunlight, an upper bound.
  Norwegian coastal sites are often overcast, so measured values will be lower.
* Horizontal surface, no terrain shading (fjords/mountains are ignored).
* Runtime: ~7 s per location-year at 1-minute steps; pass step_minutes=5 to go faster.
* Fixed AM1.5 spectral shape. At the low sun angles typical of Norwegian winter
  the real spectrum is redder, so the true photons-per-joule is a few percent
  higher; the energy (Wh/m^2) is unaffected by this assumption.
* Polar night: Tromsø (~27 Nov - 15 Jan) and Bodø (~5 Dec - 7 Jan) get zero
  direct sun; the model returns 0 for those days (twilight is not counted).
* Coordinates are city-centre points (see LOCATIONS). Moving a few km changes
  hourly flux by well under 1 %.
"""

from __future__ import annotations

import datetime as dt
from functools import lru_cache
from typing import Iterable

import numpy as np
import pandas as pd
import polars as pl
import pvlib

TZ = "Europe/Oslo"
AVOGADRO = 6.02214076e23
H_PLANCK = 6.62607015e-34
C_LIGHT = 2.99792458e8

# lat, lon (deg), altitude (m), region, weather station used by iFlex for that region
LOCATIONS: dict[str, dict] = {
    "Oslo":       dict(lat=59.9139, lon=10.7522, alt=23,  region="Oslo",      station="Oslo-Blindern"),
    "Asker":      dict(lat=59.8333, lon=10.4392, alt=100, region="Oslo",      station="Oslo-Blindern"),
    "Bærum":      dict(lat=59.8940, lon=10.5463, alt=20,  region="Oslo",      station="Oslo-Blindern"),
    "Drammen":    dict(lat=59.7439, lon=10.2045, alt=5,   region="Oslo",      station="Oslo-Blindern"),
    "Lillestrøm": dict(lat=59.9560, lon=11.0492, alt=105, region="Oslo",      station="Oslo-Blindern"),
    "Bergen":     dict(lat=60.3913, lon=5.3221,  alt=12,  region="Bergen",    station="Bergen-Florida"),
    "Stavanger":  dict(lat=58.9700, lon=5.7331,  alt=10,  region="Stavanger", station="Stavanger-Våland"),
    "Trondheim":  dict(lat=63.4305, lon=10.3951, alt=20,  region="Trondheim", station="Trondheim-Risvollan"),
    "Bodø":       dict(lat=67.2804, lon=14.4049, alt=10,  region="Bodø",      station="Bodø-Skivika"),
    "Tromsø":     dict(lat=69.6492, lon=18.9553, alt=10,  region="Tromsø",    station="Tromsø"),
}


@lru_cache(maxsize=None)
def photons_per_joule() -> dict[str, float]:
    """Photon-per-joule factors from the ASTM G173-03 global spectrum."""
    s = pvlib.spectrum.get_reference_spectra(standard="ASTM G173-03")
    wl = s.index.to_numpy(dtype=float)            # nm
    e = s["global"].to_numpy(dtype=float)         # W m^-2 nm^-1
    n = e * (wl * 1e-9) / (H_PLANCK * C_LIGHT)    # photons s^-1 m^-2 nm^-1
    par = (wl >= 400) & (wl <= 700)
    total_e = np.trapezoid(e, wl)
    return {
        "full": np.trapezoid(n, wl) / total_e,
        "par": np.trapezoid(n[par], wl[par]) / total_e,
        "par_energy_fraction": np.trapezoid(e[par], wl[par]) / total_e,
    }


def _date_list(dates) -> list[dt.date]:
    if isinstance(dates, tuple) and len(dates) == 2:
        start, end = (pd.Timestamp(d).date() for d in dates)
        return list(pd.date_range(start, end, freq="D").date)
    if isinstance(dates, (str, dt.date, pd.Timestamp)):
        return [pd.Timestamp(dates).date()]
    return [pd.Timestamp(d).date() for d in dates]


def photon_flux(
    lat: float | None = None,
    lon: float | None = None,
    dates=None,
    hours: Iterable[int] = range(1, 25),
    altitude: float = 0.0,
    location: str | None = None,
    tz: str = TZ,
    step_minutes: int = 1,
) -> pl.DataFrame:
    """Hourly clear-sky photon flux on a horizontal surface.

    lat, lon   : decimal degrees (N, E positive). Or give `location` = one of LOCATIONS.
    dates      : a date, a list of dates, or a (start, end) tuple (inclusive).
    hours      : iFlex Hour numbers 1-24 (Hour h = local [h-1, h)). Default all.
    altitude   : metres above sea level.
    Returns one row per Date x Hour with:
      ghi_Wh_m2        clear-sky energy in the hour (Wh/m^2)
      photons_m2       full-spectrum (280-4000 nm) photons per m^2 in the hour
      par_photons_m2   PAR (400-700 nm) photons per m^2 in the hour
      par_mol_m2       PAR in mol photons per m^2 in the hour
      sun_minutes      minutes with the sun above the horizon
    """
    if location is not None:
        loc = LOCATIONS[location]
        lat, lon, altitude = loc["lat"], loc["lon"], loc["alt"]
    if lat is None or lon is None or dates is None:
        raise ValueError("Need lat/lon (or location) and dates.")

    days = _date_list(dates)
    hours = sorted(set(int(h) for h in hours))
    step = pd.Timedelta(minutes=step_minutes)

    # Minute grid covering every local day, built in UTC then labelled locally.
    start = pd.Timestamp(min(days)).tz_localize(tz) - pd.Timedelta(hours=1)
    end = pd.Timestamp(max(days) + dt.timedelta(days=1)).tz_localize(tz) + pd.Timedelta(hours=1)
    edges = pd.date_range(start.tz_convert("UTC"), end.tz_convert("UTC"), freq=step)
    mids = edges + step / 2                       # sample at bin midpoints

    site = pvlib.location.Location(lat, lon, tz="UTC", altitude=altitude)
    cs = site.get_clearsky(mids, model="ineichen")
    zen = site.get_solarposition(mids)["apparent_zenith"].to_numpy()

    local = edges.tz_convert(tz)                  # bin start in local time
    f = photons_per_joule()
    wall = pl.Series("wall", local.tz_localize(None).to_numpy())   # naive local wall-clock
    df = pl.DataFrame({
        "Date": wall.dt.date(),
        "Hour": (wall.dt.hour() + 1).cast(pl.Int32),
        "ghi": cs["ghi"].clip(lower=0).to_numpy(),
        "up": (zen < 90).astype(np.int32),
    })
    sec = step.total_seconds()
    out = (
        df.filter(pl.col("Date").is_in(days) & pl.col("Hour").is_in(hours))
        .group_by("Date", "Hour")
        .agg(
            (pl.col("ghi").sum() * sec).alias("J_m2"),
            (pl.col("up").sum() * step_minutes).alias("sun_minutes"),
        )
        .with_columns(
            (pl.col("J_m2") / 3600).alias("ghi_Wh_m2"),
            (pl.col("J_m2") * f["full"]).alias("photons_m2"),
            (pl.col("J_m2") * f["par"]).alias("par_photons_m2"),
            (pl.col("J_m2") * f["par"] / AVOGADRO).alias("par_mol_m2"),
        )
        .drop("J_m2")
        .with_columns(pl.col("Hour").cast(pl.Int32))
        .sort("Date", "Hour")
        .select("Date", "Hour", "ghi_Wh_m2", "photons_m2", "par_photons_m2", "par_mol_m2", "sun_minutes")
    )
    return out


def total_photons(lat=None, lon=None, date=None, hours=range(1, 25), **kw) -> float:
    """Total full-spectrum photons per m^2 over the chosen hours of one or more dates."""
    return float(photon_flux(lat, lon, date, hours=hours, **kw)["photons_m2"].sum())


def municipality_flux_table(start="2020-01-06", end="2021-03-26", dates=None) -> pl.DataFrame:
    """Flux for every iFlex municipality. Keys: Municipality, Region, Date, Hour."""
    frames = []
    for name, loc in LOCATIONS.items():
        frames.append(
            photon_flux(location=name, dates=dates if dates is not None else (start, end))
            .with_columns(pl.lit(name).alias("Municipality"), pl.lit(loc["region"]).alias("Region"))
        )
    return pl.concat(frames).select("Municipality", "Region", pl.exclude("Municipality", "Region"))


if __name__ == "__main__":
    import sys
    from pathlib import Path

    data = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "Data"
    days = (
        pl.scan_parquet(data / "combined_data.parquet").select("Date").unique().collect()["Date"].to_list()
    )
    tbl = municipality_flux_table(dates=sorted(days))
    out = data / "solar_photon_flux_hourly.parquet"
    tbl.write_parquet(out, compression="zstd")
    print(f"wrote {out}  rows={tbl.height}")

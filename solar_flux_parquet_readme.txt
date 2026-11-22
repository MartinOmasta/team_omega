The solar flux parquet file has 9 columns:

Municipality (text): one of the 10 cities.
Region (text): the iFlex region the city belongs to.
Date (date): the experiment day.
Hour (integer, 1 to 24): the hour of the day in Oslo local time. Hour 1 is 00:00 to 01:00.
ghi_Wh_m2 (decimal): clear-sky solar energy in that hour, in Wh per m².
photons_m2 (decimal): full-spectrum photons per m² in that hour.
par_photons_m2 (decimal): visible-light (PAR, 400 to 700 nm) photons per m² in that hour.
par_mol_m2 (decimal): the same visible light, in mol per m².
sun_minutes (integer, 0 to 60): the minutes in that hour when the sun was above the horizon.

Join it to combined_data.parquet on Municipality, Date and Hour.
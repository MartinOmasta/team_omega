import os
import polars as pl
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set plotting style
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 11, 'figure.autolayout': True})

# ==========================================
# 1. ENVIRONMENT & DATA LOADING (POLARS)
# ==========================================
# Get current working directory (.\\notebooks or similar)
cwd = os.getcwd()

# Get parent folder to access (.\\Data)
parent = os.path.dirname(cwd)

# Get file path to load into environment
file_path_combined_data = os.path.join(parent, "Data", "combined_data.parquet")

print(f"Loading dataset from: {file_path_combined_data}")
df = pl.read_parquet(file_path_combined_data)

# ==========================================
# 2. FEATURE CLEANING & COLLINEARITY RESOLUTION
# ==========================================
# Drop 'Price_signal' to eliminate string concatenation redundancy & collinearity with Profile/Level.
# Keep 'Price_profile' (categorical shape) and 'Price_level' (numeric/ordinal magnitude).
if "Price_signal" in df.columns:
    df = df.drop("Price_signal")
    print("Dropped 'Price_signal' to prevent multicollinearity and parsing overhead.")

# Filter to Phase 2 for modeling and analysis (excluding Phase 1 COVID/selection bias)
df_phase2 = df.filter(
    (pl.col("Participation_Phase") == "Phase_2") & 
    (pl.col("Participation_status_Phase2") == "OK")
)

print(f"Loaded Phase 2 active rows: {df_phase2.height:,}")


# ==========================================
# 3. TARGET ENGINEERING: FLEXIBILITY PROPENSITY INDEX (FPI)
# ==========================================
print("Engineering Flexibility Propensity Index (FPI)...")

# Define peak hours (e.g., hours 17-20 / 5 PM to 9 PM when price signals are active)
# Step A: Estimate household baseline consumption on non-experiment weekdays by hour & temperature bin
df_baselines = (
    df_phase2
    .filter(pl.col("Experiment_price_NOK_kWh").is_null())
    .with_columns(
        Temp_Bin = (pl.col("Temperature24") / 5).round(0) * 5 # Bin temperature by 5°C increments
    )
    .group_by(["ID", "Hour", "Temp_Bin"])
    .agg(
        Baseline_kWh = pl.col("Demand_kWh").mean()
    )
)

# Step B: Join baseline back to experiment days and compute FPI
df_experiment_days = (
    df_phase2
    .filter(pl.col("Experiment_price_NOK_kWh").is_not_null())
    .with_columns(
        Temp_Bin = (pl.col("Temperature24") / 5).round(0) * 5
    )
    .join(df_baselines, on=["ID", "Hour", "Temp_Bin"], how="left")
    # Fallback fill if exact temp bin baseline is missing
    .with_columns(
        Baseline_kWh = pl.col("Baseline_kWh").fill_null(pl.col("Demand_kWh").mean())
    )
)

# Step C: Aggregate to Household x Experiment-Day Level FPI
df_fpi_daily = (
    df_experiment_days
    .group_by(["ID", "Date", "Region", "Price_profile", "Price_level"])
    .agg(
        Actual_Peak_Demand = pl.col("Demand_kWh").sum(),
        Base_Peak_Demand = pl.col("Baseline_kWh").sum(),
        Mean_Temp = pl.col("Temperature").mean()
    )
    .with_columns(
        # FPI formula: Percentage reduction relative to baseline (winsorized)
        Flexibility_Propensity_Index = (
            (pl.col("Base_Peak_Demand") - pl.col("Actual_Peak_Demand")) / (pl.col("Base_Peak_Demand") + 1e-6) * 100
        ).clip(-50.0, 50.0),
        High_Flexibility_Flag = (
            ((pl.col("Base_Peak_Demand") - pl.col("Actual_Peak_Demand")) / (pl.col("Base_Peak_Demand") + 1e-6) * 100) >= 5.0
        ).cast(pl.Int32)
    )
)

print(f"Computed FPI across {df_fpi_daily.height:,} household-experiment days.")


# ==========================================
# 4. APPENDIX B: GENERATING TABLES & FIGURES
# ==========================================

# --- TABLE B1: Dataset Dimensionality & Observation Breakdown ---
table_b1 = (
    df
    .group_by(["Participation_Phase", "Participation_Experiment", "Control_Price_Phase2"])
    .agg(
        Total_Rows = pl.len(),
        Unique_Households = pl.col("ID").n_unique()
    )
    .sort(["Participation_Phase", "Participation_Experiment"])
)

print("\n=== Table B1: Dataset Dimensionality & Observation Breakdown ===")
print(table_b1)


# --- FIGURE B1: Distribution of Hourly Demand & Outdoor Temperature by Region ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Convert sample to pandas for plotting with seaborn
pdf_sample = df_phase2.select(["Region", "Demand_kWh", "Temperature24"]).sample(n=50000, seed=42).to_pandas()

sns.boxplot(data=pdf_sample, x="Region", y="Demand_kWh", ax=axes[0], palette="Blues")
axes[0].set_title("Hourly Electricity Demand by Region (Phase 2)")
axes[0].set_xlabel("Region")
axes[0].set_ylabel("Demand (kWh)")
axes[0].tick_params(axis='x', rotation=30)

sns.boxplot(data=pdf_sample, x="Region", y="Temperature24", ax=axes[1], palette="coolwarm")
axes[1].set_title("24-Hour Rolling Temperature by Region (°C)")
axes[1].set_xlabel("Region")
axes[1].set_ylabel("Temperature (°C)")
axes[1].tick_params(axis='x', rotation=30)

fig_path_b1 = os.path.join(parent, "Data", "Figure_B1_Demand_Temperature_Distribution.png")
plt.savefig(fig_path_b1, dpi=300, bbox_inches="tight")
print(f"\nSaved Figure B1 to: {fig_path_b1}")
plt.close()


# --- FIGURE B2: Mean Diurnal Load Profiles (Experiment vs. Non-Experiment Days) ---
df_diurnal = (
    df_phase2
    .with_columns(
        Is_Experiment = pl.col("Experiment_price_NOK_kWh").is_not_null()
    )
    .group_by(["Hour", "Is_Experiment"])
    .agg(
        Mean_Demand = pl.col("Demand_kWh").mean()
    )
    .sort(["Hour", "Is_Experiment"])
    .to_pandas()
)

plt.figure(figsize=(10, 5))
sns.lineplot(
    data=df_diurnal, 
    x="Hour", 
    y="Mean_Demand", 
    hue="Is_Experiment", 
    marker="o", 
    linewidth=2.5,
    palette={True: "#d95f02", False: "#1b9e77"}
)
plt.title("Mean Diurnal Load Profile: Experiment Days vs. Non-Experiment Days")
plt.xlabel("Hour of Day (1–24)")
plt.ylabel("Mean Hourly Electricity Demand (kWh)")
plt.legend(title="Condition", labels=["Non-Experiment Baseline", "Active Price Experiment Day"])
plt.xticks(range(1, 25))

fig_path_b2 = os.path.join(parent, "Data", "Figure_B2_Diurnal_Load_Profiles.png")
plt.savefig(fig_path_b2, dpi=300, bbox_inches="tight")
print(f"Saved Figure B2 to: {fig_path_b2}")
plt.close()

print("\nAppendix B data processing and artifact generation complete!")
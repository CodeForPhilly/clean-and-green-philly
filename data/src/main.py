import sys
import time

from classes.backup_archive_database import BackupArchiveDatabase
from config.config import FORCE_RELOAD
from config.psql import conn
from data_utils.access_process import access_process
from data_utils.contig_neighbors import contig_neighbors
from data_utils.dev_probability import dev_probability
from data_utils.negligent_devs import negligent_devs
from data_utils.opa_properties import opa_properties
from data_utils.priority_level import priority_level
from data_utils.vacant_properties import vacant_properties
from data_utils.pwd_parcels import pwd_parcels
from data_utils.city_owned_properties import city_owned_properties
from data_utils.phs_properties import phs_properties
from data_utils.li_violations import li_violations
from data_utils.li_complaints import li_complaints
from data_utils.rco_geoms import rco_geoms
from data_utils.council_dists import council_dists
from data_utils.tree_canopy import tree_canopy
from data_utils.nbhoods import nbhoods
from data_utils.gun_crimes import gun_crimes
from data_utils.drug_crimes import drug_crimes
from data_utils.delinquencies import delinquencies
from data_utils.unsafe_buildings import unsafe_buildings
from data_utils.imm_dang_buildings import imm_dang_buildings
from data_utils.tactical_urbanism import tactical_urbanism
from data_utils.conservatorship import conservatorship
from data_utils.owner_type import owner_type
from data_utils.community_gardens import community_gardens
from data_utils.park_priority import park_priority
from data_utils.ppr_properties import ppr_properties

import pandas as pd
import geopandas as gpd


# Ensure the directory containing awkde is in the Python path
awkde_path = "/usr/src/app"
if awkde_path not in sys.path:
    sys.path.append(awkde_path)

services = [
    # vacant designation
    vacant_properties, # needs to run early so that other utils can make use of the `vacant` designation

    # geometries/areas
    pwd_parcels,
    council_dists,
    nbhoods,
    rco_geoms,

    # ownership
    city_owned_properties,
    phs_properties,
    community_gardens, 
    ppr_properties,
    owner_type,

    # quality of life
    li_violations,
    li_complaints,
    tree_canopy,
    gun_crimes,
    drug_crimes,
    delinquencies,
    unsafe_buildings,
    imm_dang_buildings,

    # development
    contig_neighbors,
    dev_probability,
    negligent_devs,

    # access/interventions
    tactical_urbanism,
    conservatorship,
    park_priority,


]

# backup sql schema if we are reloading data
backup: BackupArchiveDatabase = None
if FORCE_RELOAD:
    # first archive any remaining backup that may exist from a previous run that errored
    backup = BackupArchiveDatabase()
    if backup.is_backup_schema_exists():
        backup.archive_backup_schema()
        conn.commit()
        time.sleep(1)  # make sure we get a different timestamp
        backup = BackupArchiveDatabase()  # create a new one so we get a new timestamp

    backup.backup_schema()
    conn.commit()

dataset = opa_properties()

print("Initial Dataset:")
print("Shape:", dataset.gdf.shape)
print("Head:\n", dataset.gdf.head())
print("NA Counts:\n", dataset.gdf.isna().sum())

for service in services:
    dataset = service(dataset)
    print(f"After {service.__name__}:")
    print("Dataset type:", type(dataset.gdf).__name__)
    print("Shape:", dataset.gdf.shape)
    print("Head:\n", dataset.gdf.head())
    print("NA Counts:\n", dataset.gdf.isna().sum())

before_drop = dataset.gdf.shape[0]
dataset.gdf = dataset.gdf.drop_duplicates(subset="opa_id")
after_drop = dataset.gdf.shape[0]
print(
    f"Duplicate dataset rows dropped after initial services: {before_drop - after_drop}"
)

# Add Priority Level
dataset = priority_level(dataset)

# Print the distribution of "priority_level"
distribution = dataset.gdf["priority_level"].value_counts()
print("Distribution of priority level:")
print(distribution)

# Add Access Process
dataset = access_process(dataset)

# Print the distribution of "access_process"
distribution = dataset.gdf["access_process"].value_counts()
print("Distribution of access process:")
print(distribution)

before_drop = dataset.gdf.shape[0]
dataset.gdf = dataset.gdf.drop_duplicates(subset="opa_id")
after_drop = dataset.gdf.shape[0]
print(f"Duplicate final dataset rows droppeds: {before_drop - after_drop}")

# Convert problematic columns to numeric
numeric_columns = [
    "market_value",
    "sale_price",
    "total_assessment",
    "total_due",
    "num_years_owed",
    "permit_count",
]
for col in numeric_columns:
    dataset.gdf[col] = pd.to_numeric(dataset.gdf[col], errors="coerce")

dataset.gdf["most_recent_year_owed"] = dataset.gdf["most_recent_year_owed"].astype(str)

print("Column data types before exporting to Parquet:")
print(dataset.gdf.dtypes)

# Quick dataset profiling
print("\nQuick dataset profile:")

# 1) Number of NA values per column
print("\nNumber of NA values per column:")
print(dataset.gdf.isna().sum())

# 2) Mean, median, and std of numeric columns
print("\nMean, Median, and Standard Deviation of numeric columns:")
numeric_columns = dataset.gdf.select_dtypes(include=["float", "int"]).columns
numeric_summary = dataset.gdf[numeric_columns].describe().loc[["mean", "50%", "std"]]
numeric_summary.rename(index={"50%": "median"}, inplace=True)
print(numeric_summary)

# 3) Number of unique values in string columns
print("\nNumber of unique values in string columns:")
string_columns = dataset.gdf.select_dtypes(include=["object", "string"]).columns
unique_values = dataset.gdf[string_columns].nunique()
print(unique_values)

dataset.gdf.to_parquet("tmp/test_output.parquet")

import sys
import pandas as pd
from config.psql import conn
from sqlalchemy import text
import traceback

from new_etl.classes.slack_pg_reporter import send_pg_stats_to_slack

from new_etl.data_utils.access_process import access_process
from new_etl.data_utils.contig_neighbors import contig_neighbors
from new_etl.data_utils.dev_probability import dev_probability
from new_etl.data_utils.negligent_devs import negligent_devs
from new_etl.data_utils.opa_properties import opa_properties
from new_etl.data_utils.priority_level import priority_level
from new_etl.data_utils.vacant_properties import vacant_properties
from new_etl.data_utils.pwd_parcels import pwd_parcels
from new_etl.data_utils.city_owned_properties import city_owned_properties
from new_etl.data_utils.phs_properties import phs_properties
from new_etl.data_utils.li_violations import li_violations
from new_etl.data_utils.li_complaints import li_complaints
from new_etl.data_utils.rco_geoms import rco_geoms
from new_etl.data_utils.council_dists import council_dists
from new_etl.data_utils.tree_canopy import tree_canopy
from new_etl.data_utils.nbhoods import nbhoods
from new_etl.data_utils.gun_crimes import gun_crimes
from new_etl.data_utils.drug_crimes import drug_crimes
from new_etl.data_utils.delinquencies import delinquencies
from new_etl.data_utils.unsafe_buildings import unsafe_buildings
from new_etl.data_utils.imm_dang_buildings import imm_dang_buildings
from new_etl.data_utils.tactical_urbanism import tactical_urbanism
from new_etl.data_utils.conservatorship import conservatorship
from new_etl.data_utils.owner_type import owner_type
from new_etl.data_utils.community_gardens import community_gardens
from new_etl.data_utils.park_priority import park_priority
from new_etl.data_utils.ppr_properties import ppr_properties


send_pg_stats_to_slack(conn)  # Send PostgreSQL stats to Slack

# Ensure the directory containing awkde is in the Python path
awkde_path = "/usr/src/app"
if awkde_path not in sys.path:
    sys.path.append(awkde_path)

services = [
    # vacant designation
    vacant_properties,  # needs to run early so that other utils can make use of the `vacant` designation
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

dataset = opa_properties()

for service in services:
    dataset = service(dataset)

# Add Priority Level
dataset = priority_level(dataset)

# Add Access Process
dataset = access_process(dataset)

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

for column in numeric_columns:
    mean = dataset.gdf[column].mean()
    median = dataset.gdf[column].median()
    std = dataset.gdf[column].std()
    print(f"{column}:\n  Mean: {mean:.2f}\n  Median: {median:.2f}\n  Std: {std:.2f}")

# 3) Number of unique values in string columns
print("\nNumber of unique values in string columns:")
string_columns = dataset.gdf.select_dtypes(include=["object", "string"]).columns
unique_values = dataset.gdf[string_columns].nunique()
print(unique_values)


dataset.gdf.to_parquet("tmp/test_output.parquet")
print("Final dataset saved to tmp/ folder.")

try:
    # Save GeoDataFrame to PostgreSQL
    dataset.gdf.to_postgis(
        "vacant_properties_end",
        conn,
        if_exists="replace",  # Replace the table if it already exists
    )

    # Ensure the `create_date` column exists
    conn.execute(
        text("""
        DO $$
        BEGIN
        IF NOT EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_name = 'vacant_properties_end' AND column_name = 'create_date'
        ) THEN
            ALTER TABLE vacant_properties_end ADD COLUMN create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
        END IF;
        END $$;
        """)
    )

    # Convert the table to a hypertable
    try:
        conn.execute(
            text("""
            SELECT create_hypertable('vacant_properties_end', 'create_date', migrate_data => true);
            """)
        )
        print("Table successfully converted to a hypertable.")
    except Exception as e:
        if "already a hypertable" in str(e):
            print("Table is already a hypertable.")
        else:
            raise

    # Set chunk interval to 1 month
    try:
        conn.execute(
            text("""
            SELECT set_chunk_time_interval('vacant_properties_end', INTERVAL '1 month');
            """)
        )
        print("Chunk time interval set to 1 month.")
    except Exception as e:
        print(f"Error setting chunk interval: {e}")
        traceback.print_exc()

    # Enable compression on the hypertable
    try:
        conn.execute(
            text("""
            ALTER TABLE vacant_properties_end SET (
                timescaledb.compress,
                timescaledb.compress_segmentby = 'opa_id'
            );
            """)
        )
        print("Compression enabled on table vacant_properties_end.")
    except Exception as e:
        print(f"Error enabling compression on table vacant_properties_end: {e}")

    # Set up compression policy for chunks older than 3 months
    try:
        conn.execute(
            text("""
            SELECT add_compression_policy('vacant_properties_end', INTERVAL '6 months');
            """)
        )
        print("Compression policy added for chunks older than 6 months.")
    except Exception as e:
        print(f"Error adding compression policy: {e}")
        traceback.print_exc()

    # Commit the transaction
    conn.commit()
    print(
        "Data successfully saved and table prepared with partitioning and compression."
    )

except Exception as e:
    print(f"Error during the table operation: {e}")
    traceback.print_exc()
    conn.rollback()  # Rollback the transaction in case of failure
finally:
    conn.close()

import sys
import pandas as pd
from config.psql import conn
from sqlalchemy import text

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

from sqlalchemy.types import DateTime

# Convert to PostgreSQL-friendly timestamp
dataset.gdf['create_date'] = pd.Timestamp.now().normalize()
dataset.gdf['create_date'] = dataset.gdf['create_date'].astype('datetime64[ns]')


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


import traceback
from sqlalchemy.types import DateTime

def table_exists_and_valid(conn, table_name, required_columns, date_column="create_date"):
    try:
        # Check if the table exists
        result = conn.execute(
            text("""
            SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = :table_name
            )
            """),
            {"table_name": table_name}
        )
        exists = result.scalar()
        if not exists:
            return False

        # Check if the required columns exist
        result = conn.execute(
            text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = :table_name
            """),
            {"table_name": table_name}
        )
        columns = {row[0] for row in result}
        if not set(required_columns).issubset(columns):
            return False

        # Ensure create_date column is compatible
        result = conn.execute(
            text("""
            SELECT data_type
            FROM information_schema.columns
            WHERE table_name = :table_name AND column_name = :column_name
            """),
            {"table_name": table_name, "column_name": date_column}
        )
        actual_type = result.scalar()

        if actual_type not in ["timestamp without time zone", "timestamp with time zone", "date"]:
            print(f"Column {date_column} is {actual_type}, which is incompatible. Converting to TIMESTAMP...")
            conn.execute(
                text(f"""
                ALTER TABLE {table_name} 
                ALTER COLUMN {date_column} 
                TYPE timestamp without time zone 
                USING {date_column}::timestamp;
                """)
            )
            print(f"Column {date_column} converted to TIMESTAMP.")

        return True
    except Exception as e:
        print(f"Error during table validation: {e}")
        traceback.print_exc()
        return False

def table_is_hypertable(conn, table_name):
    try:
        result = conn.execute(
            text("""
            SELECT 1
            FROM timescaledb_information.hypertables
            WHERE hypertable_name = :table_name
            """),
            {"table_name": table_name}
        )
        return result.rowcount > 0
    except Exception as e:
        print(f"Error checking hypertable status: {e}")
        traceback.print_exc()
        return False

# Diagnostic prints
print("Columns and their dtypes:")
print(dataset.gdf.dtypes)

print("\nCreate date column details:")
print("dtype:", dataset.gdf['create_date'].dtype)
print("Sample value:", dataset.gdf['create_date'].iloc[0])

required_columns = list(dataset.gdf.columns)
if dataset.gdf.geometry.name not in required_columns:
    required_columns.append(dataset.gdf.geometry.name)

try:
    if table_exists_and_valid(conn, "vacant_properties_end", required_columns):
        print("Table exists and schema is valid. Checking if it's a hypertable...")
        if not table_is_hypertable(conn, "vacant_properties_end"):
            print("Table is not a hypertable. Converting now...")
            try:
                conn.execute(
                    text(
                        "SELECT create_hypertable('vacant_properties_end', 'create_date', migrate_data => true);"
                    )
                )
                print("Table converted to a TimescaleDB hypertable with data migration.")
            except Exception as e:
                print("Error converting to hypertable:")
                traceback.print_exc()
        else:
            print("Table is already a TimescaleDB hypertable. Appending data.")
        
        dataset.gdf.to_postgis("vacant_properties_end", conn, if_exists="append", dtype={'create_date': DateTime}, index=False)
    else:
        print("Table does not exist or schema is invalid. Replacing table.")
        dataset.gdf.to_postgis("vacant_properties_end", conn, if_exists="replace", dtype={'create_date': DateTime}, index=False)
        conn.commit()
        print("Data committed to PostgreSQL.")

        try:
            conn.execute(
                text(
                    "SELECT create_hypertable('vacant_properties_end', 'create_date', migrate_data => true);"
                )
            )
            print("Table converted to a TimescaleDB hypertable.")
        except Exception as e:
            print("Error creating hypertable:")
            traceback.print_exc()

except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    conn.rollback()  # Ensure any open transaction is rolled back on failure
finally:
    conn.close()
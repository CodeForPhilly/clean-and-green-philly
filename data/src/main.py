import sys
import pandas as pd
from config.psql import conn

from new_etl.classes.slack_reporters import (
    send_dataframe_profile_to_slack,
    send_pg_stats_to_slack,
)
from new_etl.classes.data_diff import DiffReport

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
from new_etl.database import to_postgis_with_schema


from config.config import tiles_file_id_prefix

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

# Quick dataset profiling
send_dataframe_profile_to_slack(dataset.gdf, "all_properties_end")

to_postgis_with_schema(dataset.gdf, "all_properties_end", conn)

diff_report = DiffReport()
diff_report.run()

send_pg_stats_to_slack(conn)  # Send PostgreSQL stats to Slack

# write local parquet file
parquet_path = "tmp/test_output.parquet"
dataset.gdf.to_parquet(parquet_path)
print(f"Final dataset saved to Parquet: {parquet_path}")

# Post only vacant properties to GCP
dataset.gdf = dataset.gdf[dataset.gdf["vacant"]]
dataset.build_and_publish(tiles_file_id_prefix)
conn.commit()

# Close the connection
conn.close()
print("ETL process completed successfully.")

import sys
import traceback

import pandas as pd

from config.config import tiles_file_id_prefix
from config.psql import conn
from new_etl.classes.data_diff import DiffReport
from new_etl.classes.slack_reporters import (
    send_dataframe_profile_to_slack,
    send_error_to_slack,
    send_pg_stats_to_slack,
)
from new_etl.data_utils import (
    access_process,
    city_owned_properties,
    community_gardens,
    conservatorship,
    contig_neighbors,
    council_dists,
    delinquencies,
    dev_probability,
    drug_crimes,
    gun_crimes,
    imm_dang_buildings,
    li_complaints,
    li_violations,
    nbhoods,
    negligent_devs,
    opa_properties,
    owner_type,
    park_priority,
    phs_properties,
    ppr_properties,
    priority_level,
    pwd_parcels,
    rco_geoms,
    tactical_urbanism,
    tree_canopy,
    unsafe_buildings,
    vacant_properties,
)
from new_etl.database import to_postgis_with_schema

# Ensure the directory containing awkde is in the Python path
awkde_path = "/usr/src/app"
if awkde_path not in sys.path:
    sys.path.append(awkde_path)


try:
    print("Starting ETL process.")

    services = [
        vacant_properties,  # Run early for other utils to use the `vacant` designation
        pwd_parcels,
        council_dists,
        nbhoods,
        rco_geoms,
        city_owned_properties,
        phs_properties,
        community_gardens,
        ppr_properties,
        owner_type,
        li_violations,
        li_complaints,
        tree_canopy,
        gun_crimes,
        drug_crimes,
        delinquencies,
        unsafe_buildings,
        imm_dang_buildings,
        contig_neighbors,
        dev_probability,
        negligent_devs,
        tactical_urbanism,
        conservatorship,
        park_priority,
    ]

    print("Loading OPA properties dataset.")
    dataset = opa_properties()

    for service in services:
        print(f"Running service: {service.__name__}")
        dataset = service(dataset)

    print("Applying final dataset transformations.")
    dataset = priority_level(dataset)
    dataset = access_process(dataset)

    # Save metadata
    try:
        metadata_df = pd.DataFrame(dataset.collected_metadata)
        metadata_df.to_csv("tmp/metadata.csv", index=False)
    except Exception as e:
        print(f"Error saving metadata: {str(e)}")
    # Drop duplicates
    before_drop = dataset.gdf.shape[0]
    dataset.gdf = dataset.gdf.drop_duplicates(subset="opa_id")
    print(f"Duplicate rows dropped: {before_drop - dataset.gdf.shape[0]}")

    # Convert columns to numeric where necessary
    numeric_columns = [
        "market_value",
        "sale_price",
        "total_assessment",
        "total_due",
        "num_years_owed",
        "permit_count",
    ]
    dataset.gdf[numeric_columns] = dataset.gdf[numeric_columns].apply(
        pd.to_numeric, errors="coerce"
    )
    dataset.gdf["most_recent_year_owed"] = dataset.gdf["most_recent_year_owed"].astype(
        str
    )

    # Dataset profiling
    send_dataframe_profile_to_slack(dataset.gdf, "all_properties_end")

    # Save dataset to PostgreSQL
    to_postgis_with_schema(dataset.gdf, "all_properties_end", conn)

    # Generate and send diff report
    diff_report = DiffReport()
    diff_report.run()

    send_pg_stats_to_slack(conn)  # Send PostgreSQL stats to Slack

    # Save local Parquet file
    parquet_path = "tmp/test_output.parquet"
    dataset.gdf.to_parquet(parquet_path)
    print(f"Dataset saved to Parquet: {parquet_path}")

    # Publish only vacant properties
    dataset.gdf = dataset.gdf[dataset.gdf["vacant"]]
    dataset.build_and_publish(tiles_file_id_prefix)

    # Finalize
    conn.commit()
    conn.close()
    print("ETL process completed successfully.")

except Exception as e:
    error_message = f"Error in backend job: {str(e)}\n\n{traceback.format_exc()}"
    send_error_to_slack(error_message)
    raise  # Optionally re-raise the exception

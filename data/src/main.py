import os
import traceback

import pandas as pd

from src.classes.data_diff import DiffReport
from src.classes.file_manager import FileManager, FileType, LoadType
from src.classes.slack_reporters import SlackReporter
from src.data_utils import (
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

file_manager = FileManager()
token = os.getenv("CAGP_SLACK_API_TOKEN")

slack_reporter = SlackReporter(token) if token else None

final_table_names = [
    "city_owned_properties",
    "community_gardens",
    "council_districts",
    "drug_crimes",
    "gun_crimes",
    "imminently_dangerous_buildings",
    "l_and_i_complaints",
    "li_violations",
    "opa_properties",
    "phs_properties",
    "ppr_properties",
    "property_tax_delinquencies",
    "pwd_parcels",
    "rcos",
    "updated_census_block_groups",
    "unsafe_buildings",
    "vacant_properties",
]

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
        priority_level,
        access_process,
    ]

    pipeline_errors = {}

    print("Loading OPA properties dataset.")
    dataset, opa_validation = opa_properties()

    if not opa_validation["input"] or not opa_validation["output"]:
        pipeline_errors["opa_properties"] = opa_validation

    for service in services:
        dataset, validation = service(dataset)

        if ("input" in validation and not validation["input"]) or (
            "output" in validation and not validation["output"]
        ):
            pipeline_errors[service.__name__] = validation

    # Save metadata
    try:
        metadata_df = pd.DataFrame(dataset.collected_metadata)
        metadata_df.to_csv("tmp/metadata.csv", index=False)
    except Exception as e:
        print(f"Error saving metadata: {str(e)}")
    # Drop duplicates
    before_drop = dataset.shape[0]
    dataset = dataset.drop_duplicates(subset="opa_id")
    print(f"Duplicate rows dropped: {before_drop - dataset.shape[0]}")

    # Convert columns to numeric where necessary
    numeric_columns = [
        "market_value",
        "sale_price",
        "total_assessment",
        "total_due",
        "num_years_owed",
        "permit_count",
    ]

    # Convert columns where necessary
    for col in numeric_columns:
        dataset[col] = pd.to_numeric(dataset[col], errors="coerce")
    dataset["most_recent_year_owed"] = dataset["most_recent_year_owed"].astype(str)

    if slack_reporter:
        # Dataset profiling
        slack_reporter.send_dataframe_profile_to_slack(dataset, "all_properties_end")

        # Generate and send diff report
        diff_report = DiffReport().generate_diff()
        slack_reporter.send_diff_report_to_slack(diff_report.summary_text)
    else:
        print(
            "No slack token found in environment variables - skipping slack reporting and data diffing"
        )

    # Save local Parquet file
    file_label = file_manager.generate_file_label("all_properties_end")
    file_manager.save_gdf(
        dataset, file_label, LoadType.PIPELINE_CACHE, FileType.PARQUET
    )
    print(f"Dataset saved to Parquet in storage/pipeline_cache/{file_label}.parquet")

    # Publish only vacant properties
    dataset = dataset[dataset["vacant"]]

    # Finalize
    print("ETL process completed successfully.")

except Exception as e:
    error_message = f"Error in backend job: {str(e)}\n\n{traceback.format_exc()}"
    if slack_reporter:
        slack_reporter.send_error_to_slack(error_message)
    raise  # Optionally re-raise the exception

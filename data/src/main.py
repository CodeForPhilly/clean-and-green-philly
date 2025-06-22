import logging
import os
import sys
import traceback

import pandas as pd

from src.classes.data_diff import DiffReport
from src.classes.file_manager import FileManager, FileType, LoadType
from src.classes.slack_reporters import SlackReporter
from src.config.config import (
    enable_statistical_summaries,
    get_logger,
    log_level,
)
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


def main():
    """
    Main function to run the data pipeline.
    """
    pipeline_logger = get_logger("pipeline")

    # Set up logging
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    try:
        pipeline_logger.info("Starting ETL process.")

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

        pipeline_logger.info("Loading OPA properties dataset.")
        dataset, opa_validation = opa_properties()
        pipeline_logger.info("OPA properties loaded.")

        # Check for missing zoning values after OPA properties
        if "zoning" in dataset.columns:
            missing_zoning = dataset["zoning"].isna().sum()
            total_properties = len(dataset)
            zoning_coverage = (
                (total_properties - missing_zoning) / total_properties
            ) * 100
            print(
                f"[OPA_PROPERTIES] Zoning coverage: {zoning_coverage:.2f}% ({missing_zoning}/{total_properties} missing)"
            )
        else:
            print("[OPA_PROPERTIES] Warning: 'zoning' column not found in dataset")

        # Check opa_id type after OPA properties
        if "opa_id" in dataset.columns:
            opa_id_type = dataset["opa_id"].dtype
            print(f"[OPA_PROPERTIES] opa_id type: {opa_id_type}")
        else:
            print("[OPA_PROPERTIES] Warning: 'opa_id' column not found in dataset")

        if not opa_validation["input"] or not opa_validation["output"]:
            pipeline_errors["opa_properties"] = opa_validation

        for i, service in enumerate(services, 1):
            service_name = service.__name__
            pipeline_logger.info(f"{'=' * 60}")
            pipeline_logger.info(f"{i}/{len(services)}: {service_name}")
            pipeline_logger.info(f"{'=' * 60}")

            # Call the service function (with validation decorator)
            # Apply context manager specifically for phs_properties to enable statistical summaries
            if service_name == "phs_properties":
                with enable_statistical_summaries():
                    dataset, validation = service(dataset)
            else:
                dataset, validation = service(dataset)

            pipeline_logger.info(f"{service_name} completed.")
            pipeline_logger.info(f"Dataset shape: {dataset.shape}")

            # Check opa_id type after each service
            if "opa_id" in dataset.columns:
                opa_id_type = dataset["opa_id"].dtype
                print(f"[SERVICE] {service_name} - opa_id type: {opa_id_type}")
            else:
                print(
                    f"[SERVICE] {service_name} - Warning: 'opa_id' column not found in dataset"
                )

            # Error checking - all services should return dict with input/output keys
            if not validation["input"] or not validation["output"]:
                pipeline_errors[service.__name__] = validation

            # Memory check
            try:
                import psutil

                process = psutil.Process(os.getpid())
                memory_mb = process.memory_info().rss / 1024 / 1024
                performance_logger = get_logger("performance")
                performance_logger.info(f"Memory: {memory_mb:.1f} MB")
            except ImportError:
                pass

        # Save metadata
        try:
            # Initialize collected_metadata if it doesn't exist (since services return GeoDataFrame, not FeatureLayer)
            if not hasattr(dataset, "collected_metadata"):
                dataset.collected_metadata = []

            if dataset.collected_metadata:
                # Create tmp directory if it doesn't exist
                os.makedirs("tmp", exist_ok=True)
                metadata_df = pd.DataFrame(dataset.collected_metadata)
                metadata_df.to_csv("tmp/metadata.csv", index=False)
            else:
                print("No collected_metadata found in dataset - skipping metadata save")
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
            if col in dataset.columns and not dataset[col].empty:
                dataset[col] = pd.to_numeric(dataset[col], errors="coerce")
        if "most_recent_year_owed" in dataset.columns:
            dataset["most_recent_year_owed"] = dataset["most_recent_year_owed"].astype(
                str
            )

        if slack_reporter:
            try:
                # Dataset profiling
                slack_reporter.send_dataframe_profile_to_slack(
                    dataset, "all_properties_end"
                )
            except Exception as e:
                print(
                    f"Warning: Failed to send QC profile for `all_properties_end` to Slack: {str(e)}"
                )

            try:
                # Generate and send diff report
                diff_report = DiffReport().generate_diff()
                if diff_report.summary_text:
                    slack_reporter.send_diff_report_to_slack(diff_report.summary_text)
            except Exception as e:
                print(f"Warning: Failed to send diff report to Slack: {str(e)}")
        else:
            print(
                "No slack token found in environment variables - skipping slack reporting and data diffing"
            )

        # Save local Parquet file
        file_label = file_manager.generate_file_label("all_properties_end")
        file_manager.save_gdf(
            dataset, file_label, LoadType.PIPELINE_CACHE, FileType.PARQUET
        )
        print(
            f"Dataset saved to Parquet in storage/pipeline_cache/{file_label}.parquet"
        )

        # Publish only vacant properties
        dataset = dataset[dataset["vacant"]]

        # Finalize
        pipeline_logger.info("ETL process completed successfully.")

    except Exception as e:
        error_message = f"Error in backend job: {str(e)}\n\n{traceback.format_exc()}"
        if slack_reporter:
            try:
                slack_reporter.send_error_to_slack(error_message)
            except Exception as slack_error:
                print(
                    f"Warning: Failed to send error report to Slack: {str(slack_error)}"
                )
        raise  # Optionally re-raise the exception


if __name__ == "__main__":
    main()

import os
import traceback

import pandas as pd

from new_etl.classes.file_manager import FileManager, FileType, LoadType
from new_etl.classes.data_diff import DiffReport
from new_etl.classes.slack_reporters import (
    SlackReporter,
    send_error_to_slack,
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
from new_etl.validation import (
    CommunityGardensValidator,
    KDEValidator,
    LIViolationsValidator,
    OwnerTypeValidator,
    TreeCanopyValidator,
    VacantValidator,
)
from new_etl.validation.access_process import AccessProcessValidator
from new_etl.validation.city_owned_properties import CityOwnedPropertiesValidator
from new_etl.validation.council_dists import CouncilDistrictsValidator
from new_etl.validation.nbhoods import NeighborhoodsValidator
from new_etl.validation.phs_properties import PHSPropertiesValidator
from new_etl.validation.ppr_properties import PPRPropertiesValidator
from new_etl.validation.rco_geoms import RCOGeomsValidator

file_manager = FileManager.get_instance()
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

# Map services to their validators
SERVICE_VALIDATORS = {
    "community_gardens": CommunityGardensValidator(),
    "drug_crime": KDEValidator().configure(
        density_column="drug_crimes_density",
        zscore_column="drug_crimes_density_zscore",
        label_column="drug_crimes_density_label",
        percentile_column="drug_crimes_density_percentile",
    ),
    "gun_crime": KDEValidator().configure(
        density_column="gun_crimes_density",
        zscore_column="gun_crimes_density_zscore",
        label_column="gun_crimes_density_label",
        percentile_column="gun_crimes_density_percentile",
    ),
    "li_complaints": KDEValidator().configure(
        density_column="l_and_i_complaints_density",
        zscore_column="l_and_i_complaints_density_zscore",
        label_column="l_and_i_complaints_density_label",
        percentile_column="l_and_i_complaints_density_percentile",
    ),
    "li_violations": LIViolationsValidator(),
    "owner_type": OwnerTypeValidator(),
    "vacant": VacantValidator(),
    "council_dists": CouncilDistrictsValidator(),
    "nbhoods": NeighborhoodsValidator(),
    "rco_geoms": RCOGeomsValidator(),
    "city_owned_properties": CityOwnedPropertiesValidator(),
    "phs_properties": PHSPropertiesValidator(),
    "ppr_properties": PPRPropertiesValidator(),
    "tree_canopy": TreeCanopyValidator(),
    "access_process": AccessProcessValidator(),
    # Add other service validators as they are created
}

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

        # Run validation if a validator exists for this service
        if service.__name__ in SERVICE_VALIDATORS:
            validator = SERVICE_VALIDATORS[service.__name__]
            is_valid, errors = validator.validate(dataset.gdf)

            if not is_valid:
                error_message = (
                    f"Data validation failed for {service.__name__}:\n"
                    + "\n".join(errors)
                )
                send_error_to_slack(error_message)
                raise ValueError(error_message)

            print(f"Validation passed for {service.__name__}")

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

    # Convert columns where necessary
    for col in numeric_columns:
        dataset.gdf[col] = pd.to_numeric(dataset.gdf[col], errors="coerce")
    dataset.gdf["most_recent_year_owed"] = dataset.gdf["most_recent_year_owed"].astype(
        str
    )

    if slack_reporter:
        # Dataset profiling
        slack_reporter.send_dataframe_profile_to_slack(
            dataset.gdf, "all_properties_end"
        )

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
        dataset.gdf, file_label, LoadType.PIPELINE_CACHE, FileType.PARQUET
    )
    print(f"Dataset saved to Parquet in storage/pipeline_cache/{file_label}.parquet")

    # Publish only vacant properties
    dataset.gdf = dataset.gdf[dataset.gdf["vacant"]]
    # dataset.build_and_publish(tiles_file_id_prefix)

    # Finalize
    print("ETL process completed successfully.")

except Exception as e:
    error_message = f"Error in backend job: {str(e)}\n\n{traceback.format_exc()}"
    if slack_reporter:
        slack_reporter.send_error_to_slack(error_message)
    raise  # Optionally re-raise the exception

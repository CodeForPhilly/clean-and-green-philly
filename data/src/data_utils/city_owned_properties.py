import logging
from typing import Tuple

import geopandas as gpd

from src.validation.base import ValidationResult, validate_output
from src.validation.city_owned_properties import CityOwnedPropertiesOutputValidator

from ..classes.loaders import EsriLoader
from ..constants.services import CITY_OWNED_PROPERTIES_TO_LOAD
from ..utilities import opa_join

logger = logging.getLogger(__name__)


@validate_output(CityOwnedPropertiesOutputValidator)
def city_owned_properties(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Processes city-owned property data by joining it with the primary feature layer,
    renaming columns, and updating access information for properties based on ownership.
    All instances where the "city_owner_agency" is "PLB" are changed to "Land Bank (PHDC)".

    Args:
        primary_featurelayer (FeatureLayer): The primary feature layer to which city-owned
                                             property data will be joined.

    Returns:
        FeatureLayer: The updated primary feature layer with processed city ownership
                      information.

    Columns added:
        city_owner_agency (str): The agency that owns the city property.
        side_yard_eligible (bool): Indicates if the property is eligible for the side yard program.

    Primary Feature Layer Columns Referenced:
        opa_id, owner_1, owner2

    Tagline:
        Categorizes City Owned Properties

    Source:
        https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/LAMAAssets/FeatureServer/0/

    """

    loader = EsriLoader(
        name="City Owned Properties",
        esri_urls=CITY_OWNED_PROPERTIES_TO_LOAD,
        cols=["OPABRT", "AGENCY", "SIDEYARDELIGIBLE"],
        opa_col="opabrt",
    )

    city_owned_properties, input_validation = loader.load_or_fetch()

    logger.info(
        f"[CITY_OWNED_DEBUG] City owned properties loaded: {len(city_owned_properties)} rows"
    )
    logger.info(
        f"[CITY_OWNED_DEBUG] City owned properties columns: {list(city_owned_properties.columns)}"
    )
    logger.info(
        f"[CITY_OWNED_DEBUG] City owned properties OPA column: {loader.opa_col}"
    )

    # HYPOTHESIS 1: Check for duplicates in the raw city owned properties data
    logger.info(
        "[CITY_OWNED_DEBUG] HYPOTHESIS 1: Checking for duplicates in city owned properties data..."
    )
    if loader.opa_col in city_owned_properties.columns:
        # Check for duplicates
        duplicate_mask = city_owned_properties.duplicated(
            subset=[loader.opa_col], keep=False
        )
        opa_duplicates = city_owned_properties[duplicate_mask]

        if len(opa_duplicates) > 0:
            logger.warning(
                f"[CITY_OWNED_DEBUG] HYPOTHESIS 1 CONFIRMED: Found {len(opa_duplicates)} rows with duplicate OPA IDs in raw city owned data"
            )
            logger.warning(
                f"[CITY_OWNED_DEBUG] Duplicate OPA IDs: {city_owned_properties[loader.opa_col].value_counts().head(10)}"
            )

            # Show some examples of the duplicates
            sample_duplicates = opa_duplicates.head(10)
            logger.warning("[CITY_OWNED_DEBUG] Sample duplicate rows:")
            logger.warning(sample_duplicates[[loader.opa_col, "agency"]].to_string())
        else:
            logger.info(
                "[CITY_OWNED_DEBUG] HYPOTHESIS 1 REJECTED: No duplicate OPA IDs in raw city owned data"
            )
    else:
        logger.error(
            f"[CITY_OWNED_DEBUG] ERROR: OPA column '{loader.opa_col}' not found in city owned properties data"
        )

    # Also add a simple print to check for duplicates
    logger.info(
        "[CITY_OWNED_DEBUG] Checking for duplicate OPA IDs in city owned properties..."
    )
    logger.info(
        f"[CITY_OWNED_DEBUG] Available columns: {list(city_owned_properties.columns)}"
    )
    logger.info(f"[CITY_OWNED_DEBUG] OPA column from loader: {loader.opa_col}")

    # Filter out records with null/empty OPA IDs
    original_count = len(city_owned_properties)
    city_owned_properties = city_owned_properties.dropna(subset=["opa_id"])
    city_owned_properties = city_owned_properties[city_owned_properties["opa_id"] != ""]
    filtered_count = len(city_owned_properties)
    removed_count = original_count - filtered_count

    if removed_count > 0:
        logger.warning(
            f"[CITY_OWNED_DEBUG] Removed {removed_count} records with null/empty OPA IDs"
        )
        logger.warning(f"[CITY_OWNED_DEBUG] Remaining records: {filtered_count}")

    if loader.opa_col in city_owned_properties.columns:
        duplicate_count = city_owned_properties.duplicated(
            subset=[loader.opa_col]
        ).sum()
        logger.info(
            f"[CITY_OWNED_DEBUG] Found {duplicate_count} duplicate OPA IDs in city owned properties"
        )
        if duplicate_count > 0:
            logger.warning(
                f"[CITY_OWNED_DEBUG] Duplicate OPA IDs: {city_owned_properties[loader.opa_col].value_counts().head(5)}"
            )

            # Show details of the duplicates
            logger.info("[CITY_OWNED_DEBUG] Analyzing duplicate OPA IDs...")
            duplicate_mask = city_owned_properties.duplicated(
                subset=[loader.opa_col], keep=False
            )
            duplicates = city_owned_properties[duplicate_mask]

            # Check if duplicates are truly identical (same OPA ID AND same geometry)
            logger.info(
                "[CITY_OWNED_DEBUG] Checking if duplicates are truly identical..."
            )
            full_duplicate_mask = city_owned_properties.duplicated(
                subset=["opa_id", "geometry"], keep=False
            )
            full_duplicates = city_owned_properties[full_duplicate_mask]

            logger.warning(
                f"[CITY_OWNED_DEBUG] OPA ID duplicates: {len(duplicates)} rows"
            )
            logger.warning(
                f"[CITY_OWNED_DEBUG] OPA ID + geometry duplicates: {len(full_duplicates)} rows"
            )

            # Group by OPA ID and show details
            for opa_id, group in duplicates.groupby("opa_id"):
                if len(group) > 1:  # Only show actual duplicates
                    logger.warning(
                        f"[CITY_OWNED_DEBUG] OPA ID '{opa_id}' appears {len(group)} times:"
                    )
                    logger.warning(
                        f"[CITY_OWNED_DEBUG] Agencies: {group['agency'].tolist()}"
                    )
                    logger.warning(
                        f"[CITY_OWNED_DEBUG] Side yard eligible: {group['sideyardeligible'].tolist()}"
                    )
                    logger.warning(
                        f"[CITY_OWNED_DEBUG] Geometry types: {group['geometry'].type.unique()}"
                    )

                    # Check if agencies are consistent
                    unique_agencies = group["agency"].nunique()
                    logger.warning(
                        f"[CITY_OWNED_DEBUG] Unique agencies for OPA ID '{opa_id}': {unique_agencies}"
                    )
                    if unique_agencies == 1:
                        logger.info(
                            f"[CITY_OWNED_DEBUG] ✓ All records have consistent agency: {group['agency'].iloc[0]}"
                        )
                    else:
                        logger.warning(
                            f"[CITY_OWNED_DEBUG] ✗ Records have {unique_agencies} different agencies: {group['agency'].unique()}"
                        )

                    # Check if side yard eligible is consistent
                    unique_eligible = group["sideyardeligible"].nunique()
                    logger.warning(
                        f"[CITY_OWNED_DEBUG] Unique side yard eligible values for OPA ID '{opa_id}': {unique_eligible}"
                    )
                    if unique_eligible == 1:
                        logger.info(
                            f"[CITY_OWNED_DEBUG] ✓ All records have consistent side yard eligible: {group['sideyardeligible'].iloc[0]}"
                        )
                    else:
                        logger.warning(
                            f"[CITY_OWNED_DEBUG] ✗ Records have {unique_eligible} different side yard eligible values: {group['sideyardeligible'].unique()}"
                        )

                    # Check if geometries are identical
                    unique_geometries = group["geometry"].nunique()
                    logger.warning(
                        f"[CITY_OWNED_DEBUG] Unique geometries for OPA ID '{opa_id}': {unique_geometries}"
                    )

                    if unique_geometries == 1:
                        logger.warning(
                            f"[CITY_OWNED_DEBUG] All {len(group)} records have identical geometry"
                        )
                    else:
                        logger.warning(
                            f"[CITY_OWNED_DEBUG] Records have {unique_geometries} different geometries"
                        )

                    # Show actual geometry details
                    logger.warning(
                        f"[CITY_OWNED_DEBUG] Sample geometries for OPA ID '{opa_id}':"
                    )
                    for i, geom in enumerate(group["geometry"].head(3)):
                        logger.warning(f"[CITY_OWNED_DEBUG]   Geometry {i + 1}: {geom}")
                        logger.warning(
                            f"[CITY_OWNED_DEBUG]   Geometry {i + 1} bounds: {geom.bounds}"
                        )

                    # Show first few duplicates as examples
                    if (
                        opa_id in ["053162410", "885676920", "322278001"]
                        or len(group) > 10
                    ):
                        logger.warning(
                            f"[CITY_OWNED_DEBUG] Sample rows for OPA ID '{opa_id}':"
                        )
                        logger.warning(
                            group[["opa_id", "agency", "sideyardeligible"]].to_string()
                        )
                    break  # Just show first few examples
    else:
        logger.error(
            f"[CITY_OWNED_DEBUG] ERROR: OPA column '{loader.opa_col}' not found"
        )
        # Check if 'opa_id' column exists (after OPA standardization)
        if "opa_id" in city_owned_properties.columns:
            logger.info("[CITY_OWNED_DEBUG] Found 'opa_id' column instead")
            duplicate_count = city_owned_properties.duplicated(subset=["opa_id"]).sum()
            logger.warning(
                f"[CITY_OWNED_DEBUG] Found {duplicate_count} duplicate OPA IDs in city owned properties"
            )
            if duplicate_count > 0:
                logger.warning(
                    f"[CITY_OWNED_DEBUG] Duplicate OPA IDs: {city_owned_properties['opa_id'].value_counts().head(5)}"
                )

                # Show details of the duplicates
                logger.info("[CITY_OWNED_DEBUG] Analyzing duplicate OPA IDs...")
                duplicate_mask = city_owned_properties.duplicated(
                    subset=["opa_id"], keep=False
                )
                duplicates = city_owned_properties[duplicate_mask]

                # Check if duplicates are truly identical (same OPA ID AND same geometry)
                logger.info(
                    "[CITY_OWNED_DEBUG] Checking if duplicates are truly identical..."
                )
                full_duplicate_mask = city_owned_properties.duplicated(
                    subset=["opa_id", "geometry"], keep=False
                )
                full_duplicates = city_owned_properties[full_duplicate_mask]

                logger.warning(
                    f"[CITY_OWNED_DEBUG] OPA ID duplicates: {len(duplicates)} rows"
                )
                logger.warning(
                    f"[CITY_OWNED_DEBUG] OPA ID + geometry duplicates: {len(full_duplicates)} rows"
                )

                # Group by OPA ID and show details
                for opa_id, group in duplicates.groupby("opa_id"):
                    if len(group) > 1:  # Only show actual duplicates
                        logger.warning(
                            f"[CITY_OWNED_DEBUG] OPA ID '{opa_id}' appears {len(group)} times:"
                        )
                        logger.warning(
                            f"[CITY_OWNED_DEBUG] Agencies: {group['agency'].tolist()}"
                        )
                        logger.warning(
                            f"[CITY_OWNED_DEBUG] Side yard eligible: {group['sideyardeligible'].tolist()}"
                        )
                        logger.warning(
                            f"[CITY_OWNED_DEBUG] Geometry types: {group['geometry'].type.unique()}"
                        )

                        # Check if agencies are consistent
                        unique_agencies = group["agency"].nunique()
                        logger.warning(
                            f"[CITY_OWNED_DEBUG] Unique agencies for OPA ID '{opa_id}': {unique_agencies}"
                        )
                        if unique_agencies == 1:
                            logger.info(
                                f"[CITY_OWNED_DEBUG] ✓ All records have consistent agency: {group['agency'].iloc[0]}"
                            )
                        else:
                            logger.warning(
                                f"[CITY_OWNED_DEBUG] ✗ Records have {unique_agencies} different agencies: {group['agency'].unique()}"
                            )

                        # Check if side yard eligible is consistent
                        unique_eligible = group["sideyardeligible"].nunique()
                        logger.warning(
                            f"[CITY_OWNED_DEBUG] Unique side yard eligible values for OPA ID '{opa_id}': {unique_eligible}"
                        )
                        if unique_eligible == 1:
                            logger.info(
                                f"[CITY_OWNED_DEBUG] ✓ All records have consistent side yard eligible: {group['sideyardeligible'].iloc[0]}"
                            )
                        else:
                            logger.warning(
                                f"[CITY_OWNED_DEBUG] ✗ Records have {unique_eligible} different side yard eligible values: {group['sideyardeligible'].unique()}"
                            )

                        # Check if geometries are identical
                        unique_geometries = group["geometry"].nunique()
                        logger.warning(
                            f"[CITY_OWNED_DEBUG] Unique geometries for OPA ID '{opa_id}': {unique_geometries}"
                        )

                        if unique_geometries == 1:
                            logger.warning(
                                f"[CITY_OWNED_DEBUG] All {len(group)} records have identical geometry"
                            )
                        else:
                            logger.warning(
                                f"[CITY_OWNED_DEBUG] Records have {unique_geometries} different geometries"
                            )

                        # Show actual geometry details
                        logger.warning(
                            f"[CITY_OWNED_DEBUG] Sample geometries for OPA ID '{opa_id}':"
                        )
                        for i, geom in enumerate(group["geometry"].head(3)):
                            logger.warning(
                                f"[CITY_OWNED_DEBUG]   Geometry {i + 1}: {geom}"
                            )
                            logger.warning(
                                f"[CITY_OWNED_DEBUG]   Geometry {i + 1} bounds: {geom.bounds}"
                            )

                        # Show first few duplicates as examples
                        if (
                            opa_id in ["053162410", "885676920", "322278001"]
                            or len(group) > 10
                        ):
                            logger.warning(
                                f"[CITY_OWNED_DEBUG] Sample rows for OPA ID '{opa_id}':"
                            )
                            logger.warning(
                                group[
                                    ["opa_id", "agency", "sideyardeligible"]
                                ].to_string()
                            )
                        break  # Just show first few examples

    # HYPOTHESIS 2: Check if any OPA properties intersect multiple city owned properties
    logger.info(
        "[CITY_OWNED_DEBUG] HYPOTHESIS 2: Checking if OPA properties have duplicate OPA IDs..."
    )
    opa_duplicates = input_gdf[input_gdf.duplicated(subset=["opa_id"], keep=False)]
    if len(opa_duplicates) > 0:
        logger.warning(
            f"[CITY_OWNED_DEBUG] HYPOTHESIS 2 CONFIRMED: Found {len(opa_duplicates)} rows with duplicate OPA IDs in OPA properties data"
        )
        logger.warning(
            f"[CITY_OWNED_DEBUG] OPA duplicate OPA IDs: {input_gdf['opa_id'].value_counts().head(10)}"
        )
    else:
        logger.info(
            "[CITY_OWNED_DEBUG] HYPOTHESIS 2 REJECTED: No duplicate OPA IDs in OPA properties data"
        )

    # DEDUPLICATION: Remove duplicates based on OPA ID only - simpler approach for 2 edge cases
    logger.info(
        "[CITY_OWNED_DEBUG] DEDUPLICATION: Removing duplicate OPA IDs based on OPA ID only..."
    )
    original_count = len(city_owned_properties)

    # Deduplicate based on OPA ID only, keeping the first occurrence
    city_owned_properties = city_owned_properties.drop_duplicates(
        subset=["opa_id"], keep="first"
    )

    deduplicated_count = len(city_owned_properties)
    removed_count = original_count - deduplicated_count

    logger.info(
        f"[CITY_OWNED_DEBUG] DEDUPLICATION: Removed {removed_count} duplicate rows"
    )
    logger.info(
        f"[CITY_OWNED_DEBUG] DEDUPLICATION: Before: {original_count} rows, After: {deduplicated_count} rows"
    )

    # Verify no more duplicates exist
    remaining_duplicates = city_owned_properties.duplicated(
        subset=["opa_id"], keep=False
    ).sum()
    logger.info(
        f"[CITY_OWNED_DEBUG] DEDUPLICATION: Remaining duplicate OPA IDs: {remaining_duplicates}"
    )

    merged_gdf = opa_join(input_gdf, city_owned_properties)

    logger.info(f"[CITY_OWNED_DEBUG] After opa_join: {len(merged_gdf)} rows")

    # Check for duplicates after the join
    opa_duplicates_after = merged_gdf[
        merged_gdf.duplicated(subset=["opa_id"], keep=False)
    ]
    if len(opa_duplicates_after) > 0:
        logger.warning(
            f"[CITY_OWNED_DEBUG] WARNING: Found {len(opa_duplicates_after)} rows with duplicate OPA IDs after join"
        )
        logger.warning(
            f"[CITY_OWNED_DEBUG] Duplicate OPA IDs after join: {merged_gdf['opa_id'].value_counts().head(10)}"
        )

        # Show sample of duplicates to understand the pattern
        sample_duplicates = opa_duplicates_after.head(20)
        logger.warning("[CITY_OWNED_DEBUG] Sample duplicate rows:")
        # Use available columns before rename
        available_cols = ["opa_id", "parcel_type"]
        if "agency" in sample_duplicates.columns:
            available_cols.append("agency")
        logger.warning(sample_duplicates[available_cols].to_string())
    else:
        logger.info("[CITY_OWNED_DEBUG] No duplicate OPA IDs after join")

    rename_columns = {
        "agency": "city_owner_agency",
        "sideyardeligible": "side_yard_eligible",
    }
    merged_gdf.rename(columns=rename_columns, inplace=True)

    # Include additional properties as city-owned based on owner names and addresses
    # Add properties with specific owner names and addresses to city-owned category
    include_mask = (
        merged_gdf["owner_1"].isin(["CITY OF PHILA", "CITY OF PHILADELPHIA"])
        | merged_gdf["owner_1"].isin(["PHILADELPHIA HOUSING"])
        | merged_gdf["owner_1"].isin(["REDEVELOPMENT AUTHORITY"])
        | merged_gdf["standardized_mailing_address"].str.contains(
            "municipal services bldg", case=False, na=False
        )
        | merged_gdf["standardized_mailing_address"].str.contains(
            "1234 market st", case=False, na=False
        )
        | merged_gdf["standardized_mailing_address"].str.contains(
            "office of general counsel", case=False, na=False
        )
        | merged_gdf["standardized_mailing_address"].str.contains(
            "1401 john f. kennedy blvd", case=False, na=False
        )
        | merged_gdf["standardized_mailing_address"].str.contains(
            "1600 arch st", case=False, na=False
        )
        | merged_gdf["standardized_mailing_address"].str.contains(
            "12 s 23rd st",
            case=False,
            na=False,  # Philadelphia Housing Authority
        )
        | merged_gdf["standardized_mailing_address"].str.contains(
            "440 n broad st",
            case=False,
            na=False,  # school district of philadelphia
        )
    )

    # Set city_owner_agency for included properties that don't already have it
    merged_gdf.loc[
        include_mask & merged_gdf["city_owner_agency"].isna(), "city_owner_agency"
    ] = "City of Philadelphia"

    merged_gdf.loc[
        merged_gdf["owner_1"].isin(
            [
                "PHILADELPHIA HOUSING AUTH",
                "PHILADELPHIA LAND BANK",
                "REDEVELOPMENT AUTHORITY",
                "PHILA REDEVELOPMENT AUTH",
            ]
        ),
        "city_owner_agency",
    ] = merged_gdf["owner_1"].replace(
        {
            "PHILADELPHIA HOUSING AUTH": "PHA",
            "PHILADELPHIA LAND BANK": "Land Bank (PHDC)",
            "REDEVELOPMENT AUTHORITY": "PRA",
            "PHILA REDEVELOPMENT AUTH": "PRA",
        }
    )

    merged_gdf.loc[
        (merged_gdf["owner_1"] == "CITY OF PHILA")
        & (merged_gdf["owner_2"].str.contains("PUBLIC PROP|PUBLC PROP", na=False)),
        "city_owner_agency",
    ] = "DPP"

    merged_gdf.loc[
        merged_gdf["owner_1"].isin(["CITY OF PHILADELPHIA", "CITY OF PHILA"])
        & merged_gdf["owner_2"].isna(),
        "city_owner_agency",
    ] = "City of Philadelphia"

    # Assign specific agencies based on addresses
    merged_gdf.loc[
        merged_gdf["standardized_mailing_address"].str.contains(
            "12 s 23rd st", case=False, na=False
        ),
        "city_owner_agency",
    ] = "PHA"

    merged_gdf.loc[
        merged_gdf["standardized_mailing_address"].str.contains(
            "440 n broad st", case=False, na=False
        ),
        "city_owner_agency",
    ] = "School District of Philadelphia"

    merged_gdf.loc[:, "side_yard_eligible"] = (
        merged_gdf["side_yard_eligible"].map({"Yes": True, "No": False}).fillna(False)
    )

    # Update all instances where city_owner_agency is "PLB" to "Land Bank (PHDC)"
    merged_gdf.loc[merged_gdf["city_owner_agency"] == "PLB", "city_owner_agency"] = (
        "Land Bank (PHDC)"
    )

    return merged_gdf, input_validation

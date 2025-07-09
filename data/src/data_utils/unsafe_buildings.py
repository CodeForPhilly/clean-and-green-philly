import logging
from typing import Tuple

import geopandas as gpd

from src.metadata.metadata_utils import current_metadata, provide_metadata
from src.validation.base import ValidationResult, validate_output
from src.validation.unsafe_buildings import (
    UnsafeBuildingsOutputValidator,
    UnsafeBuildingsInputValidator,
)

from ..classes.loaders import CartoLoader
from ..constants.services import UNSAFE_BUILDINGS_QUERY
from ..utilities import opa_join

logger = logging.getLogger(__name__)


@validate_output(UnsafeBuildingsOutputValidator)
@provide_metadata(current_metadata=current_metadata)
def unsafe_buildings(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Adds unsafe building information to the input GeoDataFrame by joining with a dataset
    of unsafe buildings.

    Args:
        input_gdf (GeoDataFrame): The GeoDataFrame containing property data.

    Returns:
        GeoDataFrame: The input GeoDataFrame with an added "unsafe_building" column,
        indicating whether each property is categorized as an unsafe building ("Y" or "N").

    Tagline:
        Identify unsafe buildings

    Columns Added:
        unsafe_building (bool): Indicates whether each property is categorized as an unsafe building (True or False).

    Columns referenced:
        opa_id

    Source:
        https://phl.carto.com/api/v2/sql
    """
    loader = CartoLoader(
        name="Unsafe Buildings",
        carto_queries=UNSAFE_BUILDINGS_QUERY,
        opa_col="opa_account_num",
        validator=UnsafeBuildingsInputValidator(),
    )

    unsafe_buildings, input_validation = loader.load_or_fetch()

    # Log initial state
    logger.info(f"Loaded {len(unsafe_buildings)} unsafe buildings records")
    logger.info(f"Unsafe buildings columns: {list(unsafe_buildings.columns)}")

    # Check for duplicate OPA IDs before processing
    if "opa_id" in unsafe_buildings.columns:
        duplicate_mask = unsafe_buildings.duplicated(subset=["opa_id"], keep=False)
        duplicate_count = duplicate_mask.sum()

        if duplicate_count > 0:
            logger.warning(
                f"Found {duplicate_count} duplicate OPA IDs in unsafe buildings data"
            )

            # Show sample of duplicates
            duplicate_opa_ids = unsafe_buildings[duplicate_mask]["opa_id"].unique()
            logger.info(f"Sample duplicate OPA IDs: {duplicate_opa_ids[:10]}")

            # Show details of first few duplicate groups
            duplicate_groups = unsafe_buildings[duplicate_mask].groupby("opa_id")
            logger.info("Sample duplicate groups:")
            for i, (opa_id, group) in enumerate(duplicate_groups):
                if i >= 5:  # Show first 5 duplicate groups
                    break
                logger.info(f"OPA ID '{opa_id}' appears {len(group)} times")
                logger.info(
                    f"  Columns with different values: {group.nunique().to_dict()}"
                )
        else:
            logger.info("No duplicate OPA IDs found in unsafe buildings data")

    # Mark unsafe buildings
    unsafe_buildings.loc[:, "unsafe_building"] = True

    # Keep only necessary columns: opa_id, unsafe_building, and geometry
    columns_to_keep = ["opa_id", "unsafe_building", "geometry"]
    available_columns = [
        col for col in columns_to_keep if col in unsafe_buildings.columns
    ]

    logger.info(f"Keeping columns: {available_columns}")
    unsafe_buildings = unsafe_buildings[available_columns]

    # Deduplicate based on OPA ID, keeping the first occurrence
    before_dedup = len(unsafe_buildings)
    unsafe_buildings = unsafe_buildings.drop_duplicates(subset=["opa_id"], keep="first")
    after_dedup = len(unsafe_buildings)

    if before_dedup != after_dedup:
        logger.info(
            f"Deduplicated unsafe buildings: {before_dedup} -> {after_dedup} records (removed {before_dedup - after_dedup} duplicates)"
        )

    # Join unsafe buildings data with input GeoDataFrame
    merged_gdf = opa_join(input_gdf, unsafe_buildings)

    # Fill missing values with False for non-unsafe buildings and convert to boolean
    merged_gdf.loc[:, "unsafe_building"] = (
        merged_gdf["unsafe_building"].fillna(False).astype(bool)
    )

    logger.info(f"Final output: {len(merged_gdf)} records with unsafe_building column")
    logger.info(f"Unsafe buildings count: {merged_gdf['unsafe_building'].sum()}")

    return merged_gdf, input_validation

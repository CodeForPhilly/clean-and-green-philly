import logging
from typing import Tuple

import geopandas as gpd

from src.metadata.metadata_utils import current_metadata, provide_metadata
from src.validation.base import ValidationResult, validate_output
from src.validation.imm_dang_buildings import (
    ImmDangerInputValidator,
    ImmDangerOutputValidator,
)

from ..classes.loaders import CartoLoader
from ..constants.services import IMMINENT_DANGER_BUILDINGS_QUERY
from ..utilities import opa_join

logger = logging.getLogger(__name__)


@validate_output(ImmDangerOutputValidator)
@provide_metadata(current_metadata=current_metadata)
def imm_dang_buildings(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Adds information about imminently dangerous buildings to the input GeoDataFrame
    by joining with a dataset of dangerous buildings.

    Args:
        input_gdf (GeoDataFrame): The GeoDataFrame containing property data.

    Returns:
        GeoDataFrame: The input GeoDataFrame with an added "imm_dang_building" column,
        indicating whether each property is categorized as imminently dangerous ("Y" or "N").

    Tagline:
        Identify imminently dangerous buildings

    Columns Added:
        imm_dang_building (bool): Indicates whether each property is categorized as imminently dangerous (True or False).

    Columns referenced:
        opa_id

    Source:
        https://phl.carto.com/api/v2/sql
    """

    loader = CartoLoader(
        name="Imminently Dangerous Buildings",
        carto_queries=IMMINENT_DANGER_BUILDINGS_QUERY,
        opa_col="opa_account_num",
        validator=ImmDangerInputValidator(),
    )

    imm_dang_buildings, input_validation = loader.load_or_fetch()

    # Log initial state
    logger.info(
        f"Loaded {len(imm_dang_buildings)} imminently dangerous buildings records"
    )
    logger.info(
        f"Imminently dangerous buildings columns: {list(imm_dang_buildings.columns)}"
    )

    # Check for duplicate OPA IDs before processing
    if "opa_id" in imm_dang_buildings.columns:
        duplicate_mask = imm_dang_buildings.duplicated(subset=["opa_id"], keep=False)
        duplicate_count = duplicate_mask.sum()

        if duplicate_count > 0:
            logger.warning(
                f"Found {duplicate_count} duplicate OPA IDs in imminently dangerous buildings data"
            )

            # Show sample of duplicates
            duplicate_opa_ids = imm_dang_buildings[duplicate_mask]["opa_id"].unique()
            logger.info(f"Sample duplicate OPA IDs: {duplicate_opa_ids[:10]}")

            # Show details of first few duplicate groups
            duplicate_groups = imm_dang_buildings[duplicate_mask].groupby("opa_id")
            logger.info("Sample duplicate groups:")
            for i, (opa_id, group) in enumerate(duplicate_groups):
                if i >= 5:  # Show first 5 duplicate groups
                    break
                logger.info(f"OPA ID '{opa_id}' appears {len(group)} times")
                logger.info(
                    f"  Columns with different values: {group.nunique().to_dict()}"
                )
        else:
            logger.info(
                "No duplicate OPA IDs found in imminently dangerous buildings data"
            )

    # Mark imminently dangerous buildings
    imm_dang_buildings.loc[:, "imm_dang_building"] = True

    # Keep only necessary columns: opa_id, imm_dang_building, and geometry
    columns_to_keep = ["opa_id", "imm_dang_building", "geometry"]
    available_columns = [
        col for col in columns_to_keep if col in imm_dang_buildings.columns
    ]

    logger.info(f"Keeping columns: {available_columns}")
    imm_dang_buildings = imm_dang_buildings[available_columns]

    # Deduplicate based on OPA ID, keeping the first occurrence
    before_dedup = len(imm_dang_buildings)
    imm_dang_buildings = imm_dang_buildings.drop_duplicates(
        subset=["opa_id"], keep="first"
    )
    after_dedup = len(imm_dang_buildings)

    if before_dedup != after_dedup:
        logger.info(
            f"Deduplicated imminently dangerous buildings: {before_dedup} -> {after_dedup} records (removed {before_dedup - after_dedup} duplicates)"
        )

    # Join imminently dangerous buildings data with input GeoDataFrame
    merged_gdf = opa_join(
        input_gdf,
        imm_dang_buildings,
    )

    # Fill missing values with False for non-imminently dangerous buildings and convert to boolean
    merged_gdf.loc[:, "imm_dang_building"] = (
        merged_gdf["imm_dang_building"].fillna(False).astype(bool)
    )

    logger.info(
        f"Final output: {len(merged_gdf)} records with imm_dang_building column"
    )
    logger.info(
        f"Imminently dangerous buildings count: {merged_gdf['imm_dang_building'].sum()}"
    )

    return merged_gdf, input_validation

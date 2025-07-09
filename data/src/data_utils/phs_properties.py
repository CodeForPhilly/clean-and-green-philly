from typing import Tuple

import geopandas as gpd

from src.metadata.metadata_utils import current_metadata, provide_metadata
from src.validation.base import ValidationResult, validate_output
from src.validation.phs_properties import (
    PHSPropertiesInputValidator,
    PHSPropertiesOutputValidator,
)

from ..classes.loaders import EsriLoader
from ..constants.services import PHS_LAYERS_TO_LOAD
from ..utilities import spatial_join


@validate_output(PHSPropertiesOutputValidator)
@provide_metadata(current_metadata=current_metadata)
def phs_properties(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Perform a spatial join between the input GeoDataFrame and the PHS properties layer,
    then update the input GeoDataFrame with a new column 'phs_care_program' indicating
    if the property is part of the PHS care program.

    Args:
        merged_gdf (GeoDataFrame): The input GeoDataFrame to join with the PHS properties layer.

    Returns:
        GeoDataFrame: The updated input GeoDataFrame with the 'phs_care_program' column.

    Tagline:
        Identifies PHS Care properties

    Columns added:
        phs_care_program (str): The PHS care program associated with the property.

    Columns referenced:
        opa_id, geometry
    """

    print("=== PHS Properties Service Debug ===")
    print(f"Input data shape: {input_gdf.shape}")
    print(f"Input data columns: {list(input_gdf.columns)}")
    print("Input data head:")
    print(input_gdf.head())

    loader = EsriLoader(
        name="PHS Properties",
        esri_urls=PHS_LAYERS_TO_LOAD,
        cols=["program"],
        validator=PHSPropertiesInputValidator(),
    )

    phs_properties, input_validation = loader.load_or_fetch()

    print(f"PHS properties loaded: {len(phs_properties)} records")
    print(f"PHS properties columns: {list(phs_properties.columns)}")
    print("PHS properties head:")
    print(phs_properties.head())

    # Remove duplicate OPA IDs in PHS properties before spatial join
    if "opa_id" in phs_properties.columns:
        before_dedup = len(phs_properties)
        phs_properties = phs_properties.drop_duplicates(subset=["opa_id"], keep="first")
        after_dedup = len(phs_properties)
        if before_dedup != after_dedup:
            print(
                f"Removed {before_dedup - after_dedup} duplicate OPA IDs from PHS properties"
            )
            print(f"PHS properties after deduplication: {len(phs_properties)} records")

    # Perform spatial join between input GeoDataFrame and PHS properties
    merged_gdf = spatial_join(input_gdf, phs_properties)

    print(f"After spatial join: {len(merged_gdf)} records")
    print("Merged data head:")
    print(merged_gdf.head())

    # Remove duplicate OPA IDs in the main dataset after spatial join
    before_dedup = len(merged_gdf)
    merged_gdf = merged_gdf.drop_duplicates(subset=["opa_id"], keep="first")
    after_dedup = len(merged_gdf)
    if before_dedup != after_dedup:
        print(
            f"Removed {before_dedup - after_dedup} duplicate OPA IDs from main dataset after spatial join"
        )
        print(f"Main dataset after deduplication: {len(merged_gdf)} records")

    # Create 'phs_care_program' column with values from 'program', drop 'program'
    merged_gdf["phs_care_program"] = merged_gdf.pop("program")

    return merged_gdf, input_validation

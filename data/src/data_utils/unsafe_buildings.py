from typing import Tuple

import geopandas as gpd

from src.validation.base import ValidationResult, validate_output
from src.validation.unsafe_buildings import UnsafeBuildingsOutputValidator

from ..classes.loaders import CartoLoader
from ..constants.services import UNSAFE_BUILDINGS_QUERY
from ..utilities import opa_join


@validate_output(UnsafeBuildingsOutputValidator)
def unsafe_buildings(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Adds unsafe building information to the primary feature layer by joining with a dataset
    of unsafe buildings.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.

    Returns:
        FeatureLayer: The input feature layer with an added "unsafe_building" column,
        indicating whether each property is categorized as an unsafe building ("Y" or "N").

    Tagline:
        Identify unsafe buildings

    Columns Added:
        unsafe_building (str): Indicates whether each property is categorized as an unsafe building ("Y" or "N").

    Primary Feature Layer Columns Referenced:
        opa_id

    Source:
        https://phl.carto.com/api/v2/sql
    """
    loader = CartoLoader(
        name="Unsafe Buildings",
        carto_queries=UNSAFE_BUILDINGS_QUERY,
        opa_col="opa_account_num",
    )

    unsafe_buildings, input_validation = loader.load_or_fetch()

    # Mark unsafe buildings
    unsafe_buildings.loc[:, "unsafe_building"] = "Y"

    # Join unsafe buildings data with primary feature layer
    merged_gdf = opa_join(input_gdf, unsafe_buildings)

    # Fill missing values with "N" for non-unsafe buildings
    merged_gdf.loc[:, "unsafe_building"] = merged_gdf["unsafe_building"].fillna("N")

    return merged_gdf, input_validation

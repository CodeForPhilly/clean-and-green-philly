from typing import Tuple

import geopandas as gpd

from src.validation.base import ValidationResult, validate_output
from src.validation.imm_dang_buildings import ImmDangerOutputValidator

from ..classes.loaders import CartoLoader
from ..constants.services import IMMINENT_DANGER_BUILDINGS_QUERY
from ..utilities import opa_join


@validate_output(ImmDangerOutputValidator)
def imm_dang_buildings(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Adds information about imminently dangerous buildings to the primary feature layer
    by joining with a dataset of dangerous buildings.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.

    Returns:
        FeatureLayer: The input feature layer with an added "imm_dang_building" column,
        indicating whether each property is categorized as imminently dangerous ("Y" or "N").

    Tagline:
        Identify imminently dangerous buildings

    Columns Added:
        imm_dang_building (str): Indicates whether each property is categorized as imminently dangerous ("Y" or "N").

    Primary Feature Layer Columns Referenced:
        opa_id

    Source:
        https://phl.carto.com/api/v2/sql
    """

    loader = CartoLoader(
        name="Imminently Dangerous Buildings",
        carto_queries=IMMINENT_DANGER_BUILDINGS_QUERY,
        opa_col="opa_account_num",
    )

    imm_dang_buildings, input_validation = loader.load_or_fetch()

    imm_dang_buildings.loc[:, "imm_dang_building"] = "Y"

    merged_gdf = opa_join(
        input_gdf,
        imm_dang_buildings,
    )

    merged_gdf.loc[:, "imm_dang_building"] = merged_gdf["imm_dang_building"].fillna("N")

    return merged_gdf, input_validation

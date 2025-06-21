from typing import Tuple

import geopandas as gpd
import pandas as pd

from src.validation.base import ValidationResult, validate_output
from src.validation.council_dists import CouncilDistrictsOutputValidator

from ..classes.loaders import EsriLoader
from ..constants.services import COUNCIL_DISTRICTS_TO_LOAD
from ..utilities import spatial_join

pd.set_option("future.no_silent_downcasting", True)


@validate_output(CouncilDistrictsOutputValidator)
def council_dists(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Associates properties in the primary feature layer with council districts
    using a spatial join.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.

    Returns:
        FeatureLayer: The input feature layer with properties spatially joined
        to council districts, ensuring no duplicate entries.

    Tagline:
        Assigns council districts

    Columns added:
        district (str): The council district associated with the property.

    Primary Feature Layer Columns Referenced:
        opa_id, geometry
    """

    loader = EsriLoader(
        name="Council Districts",
        esri_urls=COUNCIL_DISTRICTS_TO_LOAD,
        cols=["district"],
        input_crs="EPSG:4326",  # Load in geographic coordinates since the data appears to be lat/lon
    )

    council_dists, input_validation = loader.load_or_fetch()

    # Check that the required columns exist in the DataFrame
    required_columns = ["district", "geometry"]
    missing_columns = [
        col for col in required_columns if col not in council_dists.columns
    ]
    if missing_columns:
        raise KeyError(
            f"Missing required columns in council districts data: {', '.join(missing_columns)}"
        )

    # Check if CRS match before spatial join
    if input_gdf.crs != council_dists.crs:
        print(
            f"CRS MISMATCH: Input properties CRS ({input_gdf.crs}) != Council districts CRS ({council_dists.crs})"
        )
        print("Converting council districts to match input properties CRS...")
        council_dists = council_dists.to_crs(input_gdf.crs)
        print(f"Council districts CRS after conversion: {council_dists.crs}")
    else:
        print("CRS match confirmed")

    merged_gdf = spatial_join(input_gdf, council_dists)

    # Drop duplicates in the primary feature layer
    merged_gdf.drop_duplicates(inplace=True)

    return merged_gdf, input_validation

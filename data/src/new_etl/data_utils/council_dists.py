import pandas as pd
import geopandas as gpd

from new_etl.utilities import spatial_join

from ..classes.featurelayer import EsriLoader
from ..constants.services import COUNCIL_DISTRICTS_TO_LOAD
from ..metadata.metadata_utils import provide_metadata

pd.set_option("future.no_silent_downcasting", True)


@provide_metadata()
def council_dists(input_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
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
        name="Council Districts", esri_urls=COUNCIL_DISTRICTS_TO_LOAD, cols=["district"]
    )

    council_dists = loader.load_or_fetch()

    # Check that the required columns exist in the DataFrame
    required_columns = ["district", "geometry"]
    missing_columns = [
        col for col in required_columns if col not in council_dists.columns
    ]
    if missing_columns:
        raise KeyError(
            f"Missing required columns in council districts data: {', '.join(missing_columns)}"
        )

    # Use only the required columns
    # council_dists = council_dists[required_columns].copy()

    # Perform spatial join
    merged_gdf = spatial_join(input_gdf, council_dists)

    # Drop duplicates in the primary feature layer
    merged_gdf.drop_duplicates(inplace=True)

    return merged_gdf

import pandas as pd

from ..classes.featurelayer import FeatureLayer
from ..constants.services import COUNCIL_DISTRICTS_TO_LOAD
from ..metadata.metadata_utils import provide_metadata

pd.set_option("future.no_silent_downcasting", True)


# def merge_council_dists(
#     primary_featurelya, council_dists_gdf: pd.DataFrame
# ) -> pd.DataFrame:
#     """
#     Merges the council districts GeoDataFrame with the primary feature layer GeoDataFrame.

#     Args:
#         primary_featurelayer_gdf (pd.DataFrame): The primary feature layer GeoDataFrame.
#         council_dists_gdf (pd.DataFrame): The council districts GeoDataFrame.

#     Returns:
#         pd.DataFrame: The updated primary feature layer GeoDataFrame with council district information.
#     """
#     required_columns = ["district", "geometry"]

#     council_dists.gdf = council_dists.gdf[required_columns].copy()

#     # Perform spatial join
#     primary_featurelayer.spatial_join(council_dists)

#     # Drop duplicates in the primary feature layer
#     primary_featurelayer.gdf.drop_duplicates(inplace=True)
#     primary_featurelayer.rebuild_gdf()


@provide_metadata()
def council_dists(primary_featurelayer: FeatureLayer) -> FeatureLayer:
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
    # Load council districts
    council_dists = FeatureLayer(
        name="Council Districts", esri_rest_urls=COUNCIL_DISTRICTS_TO_LOAD
    )

    # Check that the required columns exist in the DataFrame
    required_columns = ["district", "geometry"]
    missing_columns = [
        col for col in required_columns if col not in council_dists.gdf.columns
    ]
    if missing_columns:
        raise KeyError(
            f"Missing required columns in council districts data: {', '.join(missing_columns)}"
        )

    # Use only the required columns
    council_dists.gdf = council_dists.gdf[required_columns].copy()
    council_dists.rebuild_gdf()

    # Perform spatial join
    primary_featurelayer.spatial_join(council_dists)

    # Drop duplicates in the primary feature layer
    primary_featurelayer.gdf.drop_duplicates(inplace=True)
    primary_featurelayer.rebuild_gdf()

    return primary_featurelayer

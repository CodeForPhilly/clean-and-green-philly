from classes.featurelayer import FeatureLayer
from constants.services import COUNCIL_DISTRICTS_TO_LOAD
import pandas as pd


pd.set_option("future.no_silent_downcasting", True)


def council_dists(primary_featurelayer):
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

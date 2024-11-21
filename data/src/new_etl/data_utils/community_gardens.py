from ..classes.featurelayer import FeatureLayer
from ..constants.services import COMMUNITY_GARDENS_TO_LOAD


def community_gardens(primary_featurelayer):
    # this script *removes* (rather than adds) known community gardens from the dataset in order to protect them from potential predatory developers
    community_gardens = FeatureLayer(
        name="Community Gardens", esri_rest_urls=COMMUNITY_GARDENS_TO_LOAD
    )

    community_gardens.gdf = community_gardens.gdf[["site_name", "geometry"]]

    primary_featurelayer.spatial_join(community_gardens)

    # Print the columns to debug and confirm that "site_name" exists
    print("Columns in primary_featurelayer.gdf:", primary_featurelayer.gdf.columns)

    # Create a boolean mask where 'site_name' is not null
    mask = primary_featurelayer.gdf["site_name"].notnull()

    count_dropped = mask.sum()
    print(f"Number of community gardens being dropped: {count_dropped}")

    # Use this mask to drop rows where 'site_name' is not null
    primary_featurelayer.gdf = primary_featurelayer.gdf.drop(
        primary_featurelayer.gdf[mask].index
    )

    # Ensure 'site_name' exists before attempting to drop it
    if "site_name" in primary_featurelayer.gdf.columns:
        primary_featurelayer.gdf = primary_featurelayer.gdf.drop(columns=["site_name"])
    else:
        print("'site_name' column is missing, cannot drop.")

    return primary_featurelayer

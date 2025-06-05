from src.classes.featurelayer import FeatureLayer
from src.constants.services import COMMUNITY_GARDENS_TO_LOAD


def community_gardens(primary_featurelayer):
    # this script *removes* (rather than adds) known community gardens from the dataset in order to protect them from potential predatory developers
    community_gardens = FeatureLayer(
        name="Community Gardens", esri_rest_urls=COMMUNITY_GARDENS_TO_LOAD
    )

    community_gardens.gdf = community_gardens.gdf[["Site_Name", "geometry"]]

    primary_featurelayer.spatial_join(community_gardens)

    # Create a boolean mask where 'site_Name' is not null
    mask = primary_featurelayer.gdf["Site_Name"].notnull()

    count_dropped = mask.sum()
    print(f"Number of community gardens being dropped: {count_dropped}")

    # Use this mask to drop rows where 'site_Name' is not null
    primary_featurelayer.gdf = primary_featurelayer.gdf.drop(
        primary_featurelayer.gdf[mask].index
    )

    primary_featurelayer.gdf = primary_featurelayer.gdf.drop(columns=["Site_Name"])

    return primary_featurelayer

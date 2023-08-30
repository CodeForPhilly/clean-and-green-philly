from classes.featurelayer import FeatureLayer
from constants.services import RCOS_LAYERS_TO_LOAD


def rco_geoms(primary_featurelayer):
    rco_geoms = FeatureLayer(name="RCOs", esri_rest_urls=RCOS_LAYERS_TO_LOAD)

    rco_aggregate_cols = [
        "ORGANIZATION_NAME",
        "ORGANIZATION_ADDRESS",
        "PRIMARY_EMAIL",
        "PRIMARY_PHONE",
    ]

    rco_geoms.gdf["rco_info"] = rco_geoms.gdf[rco_aggregate_cols].apply(
        lambda x: "; ".join(map(str, x)), axis=1
    )

    rco_geoms.gdf = rco_geoms.gdf[["rco_info", "geometry"]]
    rco_geoms.rebuild_gdf()

    primary_featurelayer.spatial_join(rco_geoms)

    return primary_featurelayer

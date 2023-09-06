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

    # Collapse columns and aggregate rco_info
    group_columns = [col for col in primary_featurelayer.gdf.columns if col not in ['geometry', 'rco_info']]
    for col in group_columns:
        primary_featurelayer.gdf[col].fillna('', inplace=True)

    primary_featurelayer.gdf = primary_featurelayer.gdf.groupby(group_columns).agg({
        'rco_info': lambda x: '|'.join(map(str, x)),
        'geometry': 'first'
    }).reset_index()
    primary_featurelayer.gdf.drop_duplicates(inplace=True)
    primary_featurelayer.rebuild_gdf()

    return primary_featurelayer

from classes.featurelayer import FeatureLayer
from constants.services import RCOS_LAYERS_TO_LOAD
import pandas as pd

pd.set_option("future.no_silent_downcasting", True)


def rco_geoms(primary_featurelayer):
    rco_geoms = FeatureLayer(name="RCOs", esri_rest_urls=RCOS_LAYERS_TO_LOAD)

    rco_aggregate_cols = [
        "organization_name",
        "organization_address",
        "primary_email",
        "primary_phone",
    ]

    rco_use_cols = ["rco_info", "rco_names", "geometry"]

    rco_geoms.gdf["rco_info"] = rco_geoms.gdf[rco_aggregate_cols].apply(
        lambda x: "; ".join(map(str, x)), axis=1
    )

    rco_geoms.gdf["rco_names"] = rco_geoms.gdf["organization_name"]

    rco_geoms.gdf = rco_geoms.gdf[rco_use_cols].copy()
    rco_geoms.rebuild_gdf()

    primary_featurelayer.spatial_join(rco_geoms)

    group_columns = [
        col for col in primary_featurelayer.gdf.columns if col not in rco_use_cols
    ]

    for col in group_columns:
        primary_featurelayer.gdf[col] = (
            primary_featurelayer.gdf[col].fillna("").infer_objects(copy=False)
        )

    primary_featurelayer.gdf = (
        primary_featurelayer.gdf.groupby(group_columns)
        .agg(
            {
                "rco_info": lambda x: "|".join(map(str, x)),
                "rco_names": lambda x: "|".join(map(str, x)),
                "geometry": "first",
            }
        )
        .reset_index()
    )

    primary_featurelayer.gdf.drop_duplicates(inplace=True)
    primary_featurelayer.rebuild_gdf()

    return primary_featurelayer

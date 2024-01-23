from classes.featurelayer import FeatureLayer
from constants.services import UNSAFE_BUILDINGS_QUERY
import pandas as pd


def unsafe_buildings(primary_featurelayer):
    unsafe_buildings = FeatureLayer(
        name="Unsafe Buildings",
        carto_sql_queries=UNSAFE_BUILDINGS_QUERY,
        use_wkb_geom_field="the_geom",
        cols=["opa_account_num"],
    )

    unsafe_buildings.gdf["unsafe_building"] = "Y"

    unsafe_buildings.gdf.rename(columns={"opa_account_num": "opa_number"}, inplace=True)

    primary_featurelayer.opa_join(
        unsafe_buildings.gdf,
        "opa_number",
    )

    primary_featurelayer.gdf["unsafe_building"].fillna("N", inplace=True)

    return primary_featurelayer

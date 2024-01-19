from classes.featurelayer import FeatureLayer
from constants.services import IMMINENT_DANGER_BUILDINGS_QUERY
import pandas as pd


def imm_dang_buildings(primary_featurelayer):
    imm_dang_buildings = FeatureLayer(
        name="Imminently Dangerous Buildings",
        use_wkb_geom_field="the_geom",
        carto_sql_queries=IMMINENT_DANGER_BUILDINGS_QUERY,
        
        cols=[
            "opa_account_num"
        ]
    )

    imm_dang_buildings.gdf["imm_dang_building"] = "Y"

    imm_dang_buildings.gdf.rename(columns={"opa_account_num": "opa_number"}, inplace=True)

    primary_featurelayer.opa_join(
        imm_dang_buildings.gdf,
        "opa_number",
    )

    primary_featurelayer.gdf["imm_dang_building"].fillna("N", inplace=True)

    return primary_featurelayer

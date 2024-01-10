from classes.featurelayer import FeatureLayer
from constants.services import PHS_LAYERS_TO_LOAD
import pandas as pd
from config.psql import conn


def phs_properties(primary_featurelayer):
    phs_properties = FeatureLayer(
        name="PHS Properties", esri_rest_urls=PHS_LAYERS_TO_LOAD,
        cols=["BRT_ID"]
    )

    phs_properties.gdf["phs_partner_agency"] = "PHS"

    primary_featurelayer.opa_join(
        phs_properties.gdf,
        "BRT_ID",
    )

    primary_featurelayer.gdf["phs_partner_agency"].fillna("None", inplace=True)

    primary_featurelayer.rebuild_gdf()

    return primary_featurelayer

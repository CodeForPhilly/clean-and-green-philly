from classes.featurelayer import FeatureLayer
from constants.services import PHS_LAYERS_TO_LOAD


def phs_properties(primary_featurelayer):
    phs_properties = FeatureLayer(
        name="PHS Properties", esri_rest_urls=PHS_LAYERS_TO_LOAD, cols=["BRT_ID"]
    )

    phs_properties.gdf.loc[:, "phs_partner_agency"] = "PHS"

    primary_featurelayer.opa_join(
        phs_properties.gdf,
        "brt_id",
    )

    primary_featurelayer.gdf.loc[:, "phs_partner_agency"] = primary_featurelayer.gdf[
        "phs_partner_agency"
    ].fillna("None")

    primary_featurelayer.rebuild_gdf()

    return primary_featurelayer

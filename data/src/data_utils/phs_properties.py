from classes.featurelayer import FeatureLayer
from constants.services import PHS_LAYERS_TO_LOAD


def phs_properties(primary_featurelayer):
    phs_properties = FeatureLayer(
        name="PHS Properties", esri_rest_urls=PHS_LAYERS_TO_LOAD
    )

    phs_properties.gdf["COMM_PARTN"] = "PHS"
    phs_properties.gdf = phs_properties.gdf[["COMM_PARTN", "geometry"]]

    primary_featurelayer.spatial_join(phs_properties)
    primary_featurelayer.gdf["COMM_PARTN"].fillna("None", inplace=True)

    red_cols_to_keep = [
        "COMM_PARTN",
        "geometry"
    ]

    primary_featurelayer.gdf = primary_featurelayer.gdf[red_cols_to_keep]

    rename_columns = {
    "COMM_PARTN": "phs_partner_agency",
    }

    primary_featurelayer.gdf.rename(columns=rename_columns, inplace=True)

    return primary_featurelayer

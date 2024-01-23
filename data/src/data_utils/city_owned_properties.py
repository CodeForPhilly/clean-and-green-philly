from classes.featurelayer import FeatureLayer
from constants.services import CITY_OWNED_PROPERTIES_TO_LOAD


def city_owned_properties(primary_featurelayer):
    city_owned_properties = FeatureLayer(
        name="City Owned Properties",
        esri_rest_urls=CITY_OWNED_PROPERTIES_TO_LOAD,
        cols=["OPABRT", "AGENCY", "SIDEYARDELIGIBLE"],
    )

    city_owned_properties.gdf.dropna(subset=["OPABRT"], inplace=True)

    primary_featurelayer.opa_join(
        city_owned_properties.gdf,
        "OPABRT",
    )

    rename_columns = {
        "AGENCY": "city_owner_agency",
        "SIDEYARDELIGIBLE": "side_yard_eligible",
    }

    primary_featurelayer.gdf.rename(columns=rename_columns, inplace=True)

    return primary_featurelayer

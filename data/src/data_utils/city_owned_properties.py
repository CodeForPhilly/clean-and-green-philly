from classes.featurelayer import FeatureLayer
from constants.services import CITY_OWNED_PROPERTIES_TO_LOAD


def city_owned_properties(primary_featurelayer):
    city_owned_properties = FeatureLayer(
        name="City Owned Properties",
        esri_rest_urls=CITY_OWNED_PROPERTIES_TO_LOAD,
        cols=["OPABRT", "AGENCY", "SIDEYARDELIGIBLE"],
    )

    city_owned_properties.gdf.dropna(subset=["opabrt"], inplace=True)

    primary_featurelayer.opa_join(
        city_owned_properties.gdf,
        "opabrt",
    )

    rename_columns = {
        "agency": "city_owner_agency",
        "sideyardeligible": "side_yard_eligible",
    }

    primary_featurelayer.gdf.rename(columns=rename_columns, inplace=True)

    primary_featurelayer.gdf["side_yard_eligible"].fillna("No", inplace=True)

    return primary_featurelayer

from classes.featurelayer import FeatureLayer
from constants.services import CITY_OWNED_PROPERTIES_TO_LOAD


def city_owned_properties(primary_featurelayer):
    city_owned_properties = FeatureLayer(
        name="City Owned Properties",
        esri_rest_urls=CITY_OWNED_PROPERTIES_TO_LOAD,
    )

    # Discover which vacant properties are city owned using a spatial join
    primary_featurelayer.spatial_join(city_owned_properties)

    # There are some matches which aren't valid because of imprecise parcel boundaries. Use a match on OPA_ID and OPABRT to remove these.
    primary_featurelayer.gdf = primary_featurelayer.gdf.loc[
        ~(
            (primary_featurelayer.gdf["OPABRT"].notnull())
            & (primary_featurelayer.gdf["OPA_ID"] != primary_featurelayer.gdf["OPABRT"])
        )
    ]
    return primary_featurelayer

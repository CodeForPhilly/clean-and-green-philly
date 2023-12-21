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

    red_cols_to_keep = [
        "AGENCY",
        "SIDEYARDELIGIBLE",
        "geometry"
    ]

    primary_featurelayer.gdf = primary_featurelayer.gdf[red_cols_to_keep]

    rename_columns = {
    "AGENCY": "city_owner_agency",
    "SIDEYARDELIGIBLE": "side_yard_eligible"
    }

    primary_featurelayer.gdf.rename(columns=rename_columns, inplace=True)

    return primary_featurelayer

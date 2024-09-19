from classes.featurelayer import FeatureLayer
from constants.services import CITY_OWNED_PROPERTIES_TO_LOAD


def city_owned_properties(primary_featurelayer):
    city_owned_properties = FeatureLayer(
        name="City Owned Properties",
        esri_rest_urls=CITY_OWNED_PROPERTIES_TO_LOAD,
        cols=["OPABRT", "AGENCY", "SIDEYARDELIGIBLE"],
    )

    city_owned_properties.gdf.dropna(subset=["opabrt"], inplace=True)

    primary_featurelayer.opa_join(city_owned_properties.gdf, "opabrt")

    rename_columns = {
        "agency": "city_owner_agency",
        "sideyardeligible": "side_yard_eligible",
    }
    primary_featurelayer.gdf.rename(columns=rename_columns, inplace=True)

    primary_featurelayer.gdf.loc[
        primary_featurelayer.gdf["owner_1"].isin(
            [
                "PHILADELPHIA HOUSING AUTH",
                "PHILADELPHIA LAND BANK",
                "REDEVELOPMENT AUTHORITY",
                "PHILA REDEVELOPMENT AUTH",
            ]
        ),
        "city_owner_agency",
    ] = primary_featurelayer.gdf["owner_1"].replace(
        {
            "PHILADELPHIA HOUSING AUTH": "PHA",
            "PHILADELPHIA LAND BANK": "Land Bank (PHDC)",
            "REDEVELOPMENT AUTHORITY": "PRA",
            "PHILA REDEVELOPMENT AUTH": "PRA",
        }
    )

    primary_featurelayer.gdf.loc[
        (primary_featurelayer.gdf["owner_1"] == "CITY OF PHILA")
        & (
            primary_featurelayer.gdf["owner_2"].str.contains(
                "PUBLIC PROP|PUBLC PROP", na=False
            )
        ),
        "city_owner_agency",
    ] = "DPP"

    primary_featurelayer.gdf.loc[
        primary_featurelayer.gdf["owner_1"].isin(
            ["CITY OF PHILADELPHIA", "CITY OF PHILA"]
        )
        & primary_featurelayer.gdf["owner_2"].isna(),
        "city_owner_agency",
    ] = "City of Philadelphia"

    primary_featurelayer.gdf.loc[:, "side_yard_eligible"] = primary_featurelayer.gdf[
        "side_yard_eligible"
    ].fillna("No")

    return primary_featurelayer

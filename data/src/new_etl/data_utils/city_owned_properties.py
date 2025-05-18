from ..classes.featurelayer import FeatureLayer
from ..constants.services import CITY_OWNED_PROPERTIES_TO_LOAD
from ..metadata.metadata_utils import provide_metadata
from ..validators.city_owned_properties_validator import validate_city_owned_properties


@provide_metadata()
@validate_city_owned_properties
def city_owned_properties(primary_featurelayer: FeatureLayer) -> FeatureLayer:
    """
    Processes city-owned property data by joining it with the primary feature layer,
    renaming columns, and updating access information for properties based on ownership.
    All instances where the "city_owner_agency" is "PLB" are changed to "Land Bank (PHDC)".

    Args:
        primary_featurelayer (FeatureLayer): The primary feature layer to which city-owned
                                             property data will be joined.

    Returns:
        FeatureLayer: The updated primary feature layer with processed city ownership
                      information.

    Columns added:
        city_owner_agency (str): The agency that owns the city property.
        side_yard_eligible (str): Indicates if the property is eligible for the side yard program.

    Primary Feature Layer Columns Referenced:
        opa_id, owner_1, owner2

    Tagline:
        Categorizes City Owned Properties

    Source:
        https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/LAMAAssets/FeatureServer/0/

    """
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

    # Convert side_yard_eligible to boolean
    primary_featurelayer.gdf["side_yard_eligible"] = primary_featurelayer.gdf[
        "side_yard_eligible"
    ].map({"Yes": True, "No": False})
    primary_featurelayer.gdf.loc[:, "side_yard_eligible"] = primary_featurelayer.gdf[
        "side_yard_eligible"
    ].fillna(False)

    # Update all instances where city_owner_agency is "PLB" to "Land Bank (PHDC)"
    primary_featurelayer.gdf.loc[
        primary_featurelayer.gdf["city_owner_agency"] == "PLB", "city_owner_agency"
    ] = "Land Bank (PHDC)"

    return primary_featurelayer

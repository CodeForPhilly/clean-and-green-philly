from typing import Tuple

import geopandas as gpd

from src.validation.base import ValidationResult, validate_output
from src.validation.city_owned_properties import CityOwnedPropertiesOutputValidator

from ..classes.loaders import EsriLoader
from ..constants.services import CITY_OWNED_PROPERTIES_TO_LOAD
from ..utilities import opa_join


@validate_output(CityOwnedPropertiesOutputValidator)
def city_owned_properties(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
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

    loader = EsriLoader(
        name="City Owned Properties",
        esri_urls=CITY_OWNED_PROPERTIES_TO_LOAD,
        cols=["OPABRT", "AGENCY", "SIDEYARDELIGIBLE"],
        opa_col="opabrt",
    )

    city_owned_properties, input_validation = loader.load_or_fetch()

    merged_gdf = opa_join(input_gdf, city_owned_properties)

    rename_columns = {
        "agency": "city_owner_agency",
        "sideyardeligible": "side_yard_eligible",
    }
    merged_gdf.rename(columns=rename_columns, inplace=True)

    merged_gdf.loc[
        merged_gdf["owner_1"].isin(
            [
                "PHILADELPHIA HOUSING AUTH",
                "PHILADELPHIA LAND BANK",
                "REDEVELOPMENT AUTHORITY",
                "PHILA REDEVELOPMENT AUTH",
            ]
        ),
        "city_owner_agency",
    ] = merged_gdf["owner_1"].replace(
        {
            "PHILADELPHIA HOUSING AUTH": "PHA",
            "PHILADELPHIA LAND BANK": "Land Bank (PHDC)",
            "REDEVELOPMENT AUTHORITY": "PRA",
            "PHILA REDEVELOPMENT AUTH": "PRA",
        }
    )

    merged_gdf.loc[
        (merged_gdf["owner_1"] == "CITY OF PHILA")
        & (merged_gdf["owner_2"].str.contains("PUBLIC PROP|PUBLC PROP", na=False)),
        "city_owner_agency",
    ] = "DPP"

    merged_gdf.loc[
        merged_gdf["owner_1"].isin(["CITY OF PHILADELPHIA", "CITY OF PHILA"])
        & merged_gdf["owner_2"].isna(),
        "city_owner_agency",
    ] = "City of Philadelphia"

    merged_gdf.loc[:, "side_yard_eligible"] = merged_gdf["side_yard_eligible"].fillna(
        "No"
    )

    # Update all instances where city_owner_agency is "PLB" to "Land Bank (PHDC)"
    merged_gdf.loc[merged_gdf["city_owner_agency"] == "PLB", "city_owner_agency"] = (
        "Land Bank (PHDC)"
    )

    return merged_gdf, input_validation

import logging
from typing import Tuple

import geopandas as gpd

from src.metadata.metadata_utils import current_metadata, provide_metadata
from src.validation.base import ValidationResult, validate_output
from src.validation.city_owned_properties import (
    CityOwnedPropertiesInputValidator,
    CityOwnedPropertiesOutputValidator,
)

from ..classes.loaders import EsriLoader
from ..constants.services import CITY_OWNED_PROPERTIES_TO_LOAD
from ..utilities import opa_join

logger = logging.getLogger(__name__)


@validate_output(CityOwnedPropertiesOutputValidator)
@provide_metadata(current_metadata=current_metadata)
def city_owned_properties(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Processes city-owned property data by joining it with the input dataframe,
    renaming columns, and updating access information for properties based on ownership.
    All instances where the "city_owner_agency" is "PLB" are changed to "Land Bank (PHDC)".

    Args:
        input_gdf (GeoDataFrame): The GeoDataFrame to which city-owned
                                             property data will be joined.

    Returns:
        GeoDataFrame: The updated GeoDataFrame with processed city ownership
                      information.

    Columns added:
        city_owner_agency (str): The agency that owns the city property.
        side_yard_eligible (bool): Indicates if the property is eligible for the side yard program.

    Columns referenced:
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
        validator=CityOwnedPropertiesInputValidator(),
    )

    city_owned_properties, input_validation = loader.load_or_fetch()

    # Filter out records with null/empty OPA IDs
    original_count = len(city_owned_properties)
    city_owned_properties = city_owned_properties.dropna(subset=["opa_id"])
    city_owned_properties = city_owned_properties[city_owned_properties["opa_id"] != ""]
    filtered_count = len(city_owned_properties)
    removed_count = original_count - filtered_count

    if removed_count > 0:
        logger.warning(f"Removed {removed_count} records with null/empty OPA IDs")

    # Deduplicate based on OPA ID only, keeping the first occurrence
    city_owned_properties = city_owned_properties.drop_duplicates(
        subset=["opa_id"], keep="first"
    )

    merged_gdf = opa_join(input_gdf, city_owned_properties)

    rename_columns = {
        "agency": "city_owner_agency",
        "sideyardeligible": "side_yard_eligible",
    }
    merged_gdf.rename(columns=rename_columns, inplace=True)

    # Include additional properties as city-owned based on owner names and addresses
    # Add properties with specific owner names and addresses to city-owned category
    include_mask = (
        merged_gdf["owner_1"].isin(["CITY OF PHILA", "CITY OF PHILADELPHIA"])
        | merged_gdf["owner_1"].isin(["PHILADELPHIA HOUSING"])
        | merged_gdf["owner_1"].isin(["REDEVELOPMENT AUTHORITY"])
        | merged_gdf["standardized_mailing_address"].str.contains(
            "municipal services bldg", case=False, na=False
        )
        | merged_gdf["standardized_mailing_address"].str.contains(
            "1234 market st", case=False, na=False
        )
        | merged_gdf["standardized_mailing_address"].str.contains(
            "office of general counsel", case=False, na=False
        )
        | merged_gdf["standardized_mailing_address"].str.contains(
            "1401 john f. kennedy blvd", case=False, na=False
        )
        | merged_gdf["standardized_mailing_address"].str.contains(
            "1600 arch st", case=False, na=False
        )
        | merged_gdf["standardized_mailing_address"].str.contains(
            "12 s 23rd st",
            case=False,
            na=False,  # Philadelphia Housing Authority
        )
        | merged_gdf["standardized_mailing_address"].str.contains(
            "440 n broad st",
            case=False,
            na=False,  # school district of philadelphia
        )
    )

    # Set city_owner_agency for included properties that don't already have it
    merged_gdf.loc[
        include_mask & merged_gdf["city_owner_agency"].isna(), "city_owner_agency"
    ] = "City of Philadelphia"

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

    # Assign specific agencies based on addresses
    merged_gdf.loc[
        merged_gdf["standardized_mailing_address"].str.contains(
            "12 s 23rd st", case=False, na=False
        ),
        "city_owner_agency",
    ] = "PHA"

    merged_gdf.loc[
        merged_gdf["standardized_mailing_address"].str.contains(
            "440 n broad st", case=False, na=False
        ),
        "city_owner_agency",
    ] = "School District of Philadelphia"

    merged_gdf.loc[:, "side_yard_eligible"] = (
        merged_gdf["side_yard_eligible"].map({"Yes": True, "No": False}).fillna(False)
    )

    # Update all instances where city_owner_agency is "PLB" to "Land Bank (PHDC)"
    merged_gdf.loc[merged_gdf["city_owner_agency"] == "PLB", "city_owner_agency"] = (
        "Land Bank (PHDC)"
    )

    return merged_gdf, input_validation

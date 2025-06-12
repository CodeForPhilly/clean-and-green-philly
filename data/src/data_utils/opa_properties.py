import re

import geopandas as gpd
import pandas as pd

<<<<<<< HEAD
from src.validation.base import validate_output
from src.validation.opa_properties import OPAPropertiesOutputValidator

=======
>>>>>>> cfreedman/feature-layer-refactor
from ..classes.loaders import CartoLoader
from ..constants.services import OPA_PROPERTIES_QUERY

replacements = {
    "STREET": "ST",
    "AVENUE": "AVE",
    "ROAD": "RD",
    "BOULEVARD": "BLVD",
    "PLACE": "PL",
    "FLOOR": "FL",
    "FLR": "FL",
    "FIRST": "1ST",
    "SECOND": "2ND",
    "THIRD": "3RD",
    "FOURTH": "4TH",
    "FIFTH": "5TH",
    "SIXTH": "6TH",
    "SEVENTH": "7TH",
    "EIGHTH": "8TH",
    "NINTH": "9TH",
    "NORTH": "N",
    "SOUTH": "S",
    "EAST": "E",
    "WEST": "W",
    "SUITE": "STE",
    "LA": "LN",
    "LANE": "LN",
    "PARKWAY": "PKY",
}


def standardize_street(street: str) -> str:
    """
    Standardizes street names by replacing common full names with abbreviations.

    Args:
        street (str): The street name to standardize.

    Returns:
        str: The standardized street name.
    """
    if not isinstance(street, str):
        return ""
    for full, abbr in replacements.items():
        street = re.sub(r"\b{}\b".format(full), abbr, street, flags=re.IGNORECASE)
    return street


def create_standardized_address(row: pd.Series) -> str:
    """
    Creates a standardized address from multiple address-related columns in a row.

    Args:
        row (pd.Series): A row of a DataFrame containing address-related fields.

    Returns:
        str: A standardized, lowercased address string.
    """
    parts = [
        row["mailing_address_1"].strip()
        if pd.notnull(row["mailing_address_1"])
        else "",
        row["mailing_address_2"].strip()
        if pd.notnull(row["mailing_address_2"])
        else "",
        row["mailing_street"].strip() if pd.notnull(row["mailing_street"]) else "",
        row["mailing_city_state"].strip()
        if pd.notnull(row["mailing_city_state"])
        else "",
        row["mailing_zip"].strip() if pd.notnull(row["mailing_zip"]) else "",
    ]
    standardized_address = ", ".join([part for part in parts if part])
    return standardized_address.lower()


<<<<<<< HEAD
@validate_output(OPAPropertiesOutputValidator)
def opa_properties(gdf: gpd.GeoDataFrame = None) -> gpd.GeoDataFrame:
=======
def opa_properties() -> gpd.GeoDataFrame:
>>>>>>> cfreedman/feature-layer-refactor
    """
    Loads and processes OPA property data, standardizing addresses and cleaning geometries.

    Returns:
        FeatureLayer: A feature layer containing processed OPA property data.

    Columns Added:
        opa_id (int): the OPA ID of the property
        market_value (float): the market value from the OPA data
        sale_date (str): the date of the last sale
        sale_price (float): the price of the last sale
        parcel_type (str): "Land" or "Building"
        zip_code (str): The zip code of the property
        zoning (str): The zoning of the property
        owner_1 (str): The first owner of the property
        owner_2 (str): The second owner of the property
        building_code_description (str): The building code description
        standardized_address (str): A standardized mailing address
        geometry (geometry): The geometry of the property

    Source:
        https://phl.carto.com/api/v2/sql

    Tagline:
        Load OPA data
    """
    loader = CartoLoader(
        carto_queries=OPA_PROPERTIES_QUERY,
        name="OPA Properties",
        opa_col="parcel_number",
        cols=[
            "market_value",
            "sale_date",
            "sale_price",
            "parcel_number",
            "owner_1",
            "owner_2",
            "mailing_address_1",
            "mailing_address_2",
            "mailing_care_of",
            "mailing_city_state",
            "mailing_street",
            "mailing_zip",
            "building_code_description",
            "zip_code",
            "zoning",
        ],
    )

    opa, input_validation = loader.load_or_fetch()

    # Convert 'sale_price' and 'market_value' to numeric values
    opa["sale_price"] = pd.to_numeric(opa["sale_price"], errors="coerce")
    opa["market_value"] = pd.to_numeric(opa["market_value"], errors="coerce")

    # Add parcel_type
    opa["parcel_type"] = (
        opa["building_code_description"]
        .str.contains("VACANT LAND", case=False, na=False)
        .map({True: "Land", False: "Building"})
    )

    # Standardize mailing street addresses
    opa["mailing_street"] = opa["mailing_street"].astype(str).apply(standardize_street)

    # Create standardized address column
    opa["standardized_address"] = opa.apply(create_standardized_address, axis=1)

    # Drop columns starting with "mailing_"
    opa = opa.loc[:, ~opa.columns.str.startswith("mailing_")]

    # Drop empty geometries
    opa = opa[~opa.is_empty]

    return opa, input_validation

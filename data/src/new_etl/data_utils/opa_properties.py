import pandas as pd
import re
from ..classes.featurelayer import FeatureLayer
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


def opa_properties() -> FeatureLayer:
    """
    Loads and processes OPA property data, standardizing addresses and cleaning geometries.

    Returns:
        FeatureLayer: A feature layer containing processed OPA property data.
    """
    opa = FeatureLayer(
        name="OPA Properties",
        carto_sql_queries=OPA_PROPERTIES_QUERY,
        use_wkb_geom_field="the_geom",
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

    # Rename columns
    opa.gdf = opa.gdf.rename(columns={"parcel_number": "opa_id"})

    # Convert 'sale_price' and 'market_value' to numeric values
    opa.gdf["sale_price"] = pd.to_numeric(opa.gdf["sale_price"], errors="coerce")
    opa.gdf["market_value"] = pd.to_numeric(opa.gdf["market_value"], errors="coerce")

    # Add parcel_type
    opa.gdf["parcel_type"] = (
        opa.gdf["building_code_description"]
        .str.contains("VACANT LAND", case=False, na=False)
        .map({True: "Land", False: "Building"})
    )

    # Standardize mailing street addresses
    opa.gdf["mailing_street"] = (
        opa.gdf["mailing_street"].astype(str).apply(standardize_street)
    )

    # Create standardized address column
    opa.gdf["standardized_address"] = opa.gdf.apply(create_standardized_address, axis=1)

    # Drop columns starting with "mailing_"
    opa.gdf = opa.gdf.loc[:, ~opa.gdf.columns.str.startswith("mailing_")]

    # Use GeoSeries.make_valid to repair geometries
    opa.gdf["geometry"] = opa.gdf["geometry"].make_valid()

    # Drop empty geometries
    opa.gdf = opa.gdf[~opa.gdf.is_empty]

    return opa

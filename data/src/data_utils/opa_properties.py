import re
import time
from typing import Tuple

import geopandas as gpd
import pandas as pd

from src.classes.loaders import CartoLoader
from src.validation.base import ValidationResult, validate_output
from src.validation.opa_properties import OPAPropertiesOutputValidator

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


def create_standardized_mailing_address(row: pd.Series) -> str:
    """
    Creates a standardized mailing address from multiple address-related columns in a row.

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
    standardized_mailing_address = ", ".join([part for part in parts if part])
    return standardized_mailing_address.lower()


def standardize_street_vectorized(street_series: pd.Series) -> pd.Series:
    """
    Vectorized street name standardization using pandas string operations.

    Args:
        street_series (pd.Series): Series of street names to standardize.

    Returns:
        pd.Series: Series of standardized street names.
    """
    # Convert to string and handle non-string values
    street_series = street_series.astype(str)

    # Apply all replacements using vectorized operations
    for full, abbr in replacements.items():
        # Use case-insensitive regex replacement
        pattern = r"\b" + re.escape(full) + r"\b"
        street_series = street_series.str.replace(pattern, abbr, case=False, regex=True)

    return street_series


def create_standardized_mailing_address_vectorized(gdf: gpd.GeoDataFrame) -> pd.Series:
    """
    Vectorized mailing address standardization using pandas string operations.

    Args:
        gdf (gpd.GeoDataFrame): GeoDataFrame containing address-related columns.

    Returns:
        pd.Series: Series of standardized mailing addresses.
    """
    # Get address columns and handle nulls
    address_1 = gdf["mailing_address_1"].fillna("").astype(str).str.strip()
    address_2 = gdf["mailing_address_2"].fillna("").astype(str).str.strip()
    street = gdf["mailing_street"].fillna("").astype(str).str.strip()
    city_state = gdf["mailing_city_state"].fillna("").astype(str).str.strip()
    zip_code = gdf["mailing_zip"].fillna("").astype(str).str.strip()

    # Combine all parts, filtering out empty strings
    parts = [address_1, address_2, street, city_state, zip_code]

    # Join non-empty parts with commas
    standardized = parts[0]
    for part in parts[1:]:
        # Only add non-empty parts
        mask = (part != "") & (standardized != "")
        standardized = standardized.where(~mask, standardized + ", " + part)
        mask = (part != "") & (standardized == "")
        standardized = standardized.where(~mask, part)

    return standardized.str.lower()


@validate_output(OPAPropertiesOutputValidator)
def opa_properties(
    gdf: gpd.GeoDataFrame = None,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Loads and processes OPA property data, standardizing addresses and cleaning geometries.

    Returns:
        Tuple[GeoDataFrame, ValidationResult]: A tuple containing the processed GeoDataFrame and validation result.

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
        standardized_street_address (str): A standardized street address for the property
        standardized_mailing_address (str): A standardized mailing address for the property owner
        geometry (geometry): The geometry of the property

    Source:
        https://phl.carto.com/api/v2/sql

    Tagline:
        Load OPA data
    """
    print("[OPA_PROPERTIES] Starting opa_properties function")
    function_start = time.time()

    loader_start = time.time()
    print("[OPA_PROPERTIES] Creating CartoLoader")
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
            "unit",
            "street_address",
            "building_code_description",
            "zip_code",
            "zoning",
        ],
    )
    loader_time = time.time() - loader_start
    print(f"[OPA_PROPERTIES] CartoLoader creation: {loader_time:.3f}s")

    load_start = time.time()
    print("[OPA_PROPERTIES] About to call load_or_fetch")
    opa, input_validation = loader.load_or_fetch()
    load_time = time.time() - load_start
    print(f"[OPA_PROPERTIES] load_or_fetch completed: {load_time:.3f}s")
    print(f"[OPA_PROPERTIES] Loaded {len(opa)} rows")

    # Convert 'sale_price' and 'market_value' to numeric values
    numeric_start = time.time()
    print("[OPA_PROPERTIES] Converting sale_price and market_value to numeric")
    opa["sale_price"] = pd.to_numeric(opa["sale_price"], errors="coerce")
    opa["market_value"] = pd.to_numeric(opa["market_value"], errors="coerce")
    numeric_time = time.time() - numeric_start
    print(f"[OPA_PROPERTIES] Numeric conversion: {numeric_time:.3f}s")

    # Convert sale_date to datetime
    date_start = time.time()
    print("[OPA_PROPERTIES] Converting sale_date to datetime")
    opa["sale_date"] = pd.to_datetime(opa["sale_date"])
    date_time = time.time() - date_start
    print(f"[OPA_PROPERTIES] Date conversion: {date_time:.3f}s")

    # Add parcel_type
    parcel_type_start = time.time()
    print("[OPA_PROPERTIES] Adding parcel_type column")
    opa["parcel_type"] = (
        opa["building_code_description"]
        .str.contains("VACANT LAND", case=False, na=False)
        .map({True: "Land", False: "Building"})
    )
    parcel_type_time = time.time() - parcel_type_start
    print(f"[OPA_PROPERTIES] Parcel type addition: {parcel_type_time:.3f}s")

    # Combine street_address and unit into a single column, if unit is not empty
    street_combine_start = time.time()
    print("[OPA_PROPERTIES] Combining street_address and unit")
    opa["street_address"] = opa.apply(
        lambda row: f"{row['street_address']} {row['unit']}"
        if pd.notnull(row["unit"]) and str(row["unit"]).strip() != ""
        else row["street_address"],
        axis=1,
    )
    street_combine_time = time.time() - street_combine_start
    print(f"[OPA_PROPERTIES] Street combine: {street_combine_time:.3f}s")

    # Standardize street addresses
    street_start = time.time()
    print("[OPA_PROPERTIES] Standardizing street addresses")
    opa["street_address"] = opa["street_address"].astype(str).apply(standardize_street)
    street_time = time.time() - street_start
    print(f"[OPA_PROPERTIES] Street standardization: {street_time:.3f}s")

    # Create standardized street address column
    street_std_start = time.time()
    print("[OPA_PROPERTIES] Creating standardized street address column")
    opa["standardized_street_address"] = opa["street_address"].str.lower()
    street_std_time = time.time() - street_std_start
    print(f"[OPA_PROPERTIES] Street address standardization: {street_std_time:.3f}s")

    # Standardize mailing street addresses
    mailing_street_start = time.time()
    print("[OPA_PROPERTIES] Standardizing mailing street addresses (vectorized)")
    opa["mailing_street"] = standardize_street_vectorized(opa["mailing_street"])
    mailing_street_time = time.time() - mailing_street_start
    print(
        f"[OPA_PROPERTIES] Mailing street standardization: {mailing_street_time:.3f}s"
    )

    # Create standardized mailing address column
    address_start = time.time()
    print("[OPA_PROPERTIES] Creating standardized mailing address column (vectorized)")
    opa["standardized_mailing_address"] = (
        create_standardized_mailing_address_vectorized(opa)
    )
    address_time = time.time() - address_start
    print(f"[OPA_PROPERTIES] Mailing address standardization: {address_time:.3f}s")

    # Drop columns starting with "mailing_"
    drop_start = time.time()
    print("[OPA_PROPERTIES] Dropping mailing_ columns")
    opa = opa.loc[:, ~opa.columns.str.startswith("mailing_")]
    drop_time = time.time() - drop_start
    print(f"[OPA_PROPERTIES] Column dropping: {drop_time:.3f}s")

    # Drop unit column
    unit_drop_start = time.time()
    print("[OPA_PROPERTIES] Dropping unit column")
    opa = opa.drop(columns=["unit"])
    unit_drop_time = time.time() - unit_drop_start
    print(f"[OPA_PROPERTIES] Unit column dropping: {unit_drop_time:.3f}s")

    # Drop empty geometries
    geometry_start = time.time()
    print("[OPA_PROPERTIES] Dropping empty geometries")
    opa = opa[~opa.is_empty]
    geometry_time = time.time() - geometry_start
    print(f"[OPA_PROPERTIES] Empty geometry removal: {geometry_time:.3f}s")

    function_total_time = time.time() - function_start
    print(f"[OPA_PROPERTIES] Total function time: {function_total_time:.3f}s")
    print(f"[OPA_PROPERTIES] Returning {len(opa)} rows")

    return opa, input_validation

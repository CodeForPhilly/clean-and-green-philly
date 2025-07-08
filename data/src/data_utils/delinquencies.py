from typing import Tuple

import geopandas as gpd
import pandas as pd

from src.metadata.metadata_utils import current_metadata, provide_metadata
from src.validation.base import ValidationResult, validate_output
from src.validation.delinquencies import DelinquenciesOutputValidator

from ..classes.loaders import CartoLoader
from ..constants.services import DELINQUENCIES_QUERY
from ..utilities import opa_join


@validate_output(DelinquenciesOutputValidator)
@provide_metadata(current_metadata=current_metadata)
def delinquencies(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Adds property tax delinquency information to the input GeoDataFrame by
    joining with a tax delinquencies dataset.

    Args:
        input_gdf (GeoDataFrame): The GeoDataFrame containing property data.

    Returns:
        GeoDataFrame: The input GeoDataFrame with added columns for tax delinquency
        information, including total due, actionable status, payment agreements, and more.

    Tagline:
        Summarize tax delinquencies

    Source:
        https://phl.carto.com/api/v2/sql

    Columns Added:
        total_due (float): Total amount owed.
        most_recent_year_owed (str): Most recent year owed.
        num_years_owed (int): Number of years owed.
        payment_agreement (bool): Indicates if there is a payment agreement.
        is_actionable (bool): Flag for actionable tax delinquency.
        sheriff_sale (bool): Indicates if the property is at risk of sheriff sale.
        total_assessment (float): Total property assessment.

    Columns referenced:
        opa_id
    """

    loader = CartoLoader(
        name="Property Tax Delinquencies",
        carto_queries=DELINQUENCIES_QUERY,
        cols=[
            "opa_number",
            "total_due",
            "is_actionable",
            "payment_agreement",
            "num_years_owed",
            "most_recent_year_owed",
            "total_assessment",
            "sheriff_sale",
        ],
        opa_col="opa_number",
    )

    tax_delinquencies, input_validation = loader.load_or_fetch()

    merged_gdf = opa_join(
        input_gdf,
        tax_delinquencies,
    )

    # Convert num_years_owed to integer, allowing NA values
    merged_gdf["num_years_owed"] = pd.to_numeric(
        merged_gdf["num_years_owed"], errors="coerce"
    ).astype("Int64")  # Using Int64 to allow NA values

    # Convert total_due and total_assessment to float, allowing NA values
    merged_gdf["total_due"] = pd.to_numeric(merged_gdf["total_due"], errors="coerce")
    merged_gdf["total_assessment"] = pd.to_numeric(
        merged_gdf["total_assessment"], errors="coerce"
    )

    # Convert boolean fields from string to boolean
    merged_gdf["is_actionable"] = (
        merged_gdf["is_actionable"]
        .map({"Y": True, "N": False, "NA": False})
        .fillna(False)
    )
    merged_gdf["sheriff_sale"] = (
        merged_gdf["sheriff_sale"]
        .map({"Y": True, "N": False, "NA": False})
        .fillna(False)
    )
    merged_gdf["payment_agreement"] = (
        merged_gdf["payment_agreement"]
        .map({"Y": True, "N": False, "NA": False})
        .fillna(False)
    )

    # Convert most_recent_year_owed to datetime, handling invalid values
    # First, replace invalid values with NaN
    merged_gdf["most_recent_year_owed"] = merged_gdf["most_recent_year_owed"].replace(
        ["nan", "None", ""], pd.NaT
    )

    # Convert valid values to datetime with explicit format
    merged_gdf["most_recent_year_owed"] = pd.to_datetime(
        merged_gdf["most_recent_year_owed"].astype(str) + "-12-31",
        format="%Y-%m-%d",
        errors="coerce",
    )

    # Fill missing values with "NA" for string columns
    for col in ["total_due", "total_assessment"]:
        merged_gdf[col] = merged_gdf[col].fillna("NA")

    delinquency_cols = [
        "most_recent_year_owed",
    ]
    merged_gdf[delinquency_cols] = merged_gdf[delinquency_cols].fillna("NA")

    return merged_gdf, input_validation

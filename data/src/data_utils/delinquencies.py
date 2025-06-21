from typing import Tuple

import geopandas as gpd
import pandas as pd

from src.validation.base import ValidationResult, validate_output
from src.validation.delinquencies import DelinquenciesOutputValidator

from ..classes.loaders import CartoLoader
from ..constants.services import DELINQUENCIES_QUERY
from ..utilities import opa_join


@validate_output(DelinquenciesOutputValidator)
def delinquencies(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Adds property tax delinquency information to the primary feature layer by
    joining with a tax delinquencies dataset.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.

    Returns:
        FeatureLayer: The input feature layer with added columns for tax delinquency
        information, including total due, actionable status, payment agreements, and more.

    Tagline:
        Summarize tax delinquencies

    Source:
        https://phl.carto.com/api/v2/sql

    Columns Added:
        total_due (float): Total amount owed.
        most_recent_year_owed (str): Most recent year owed.
        num_years_owed (int): Number of years owed.
        payment_agreement (str): Indicates if there is a payment agreement.
        is_actionable (str): Flag for actionable tax delinquency.
        sheriff_sale (str): Indicates if the property is at risk of sheriff sale.
        total_assessment (float): Total property assessment.

    Primary Feature Layer Columns Referenced:
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

    # Convert most_recent_year_owed to datetime
    merged_gdf["most_recent_year_owed"] = pd.to_datetime(
        merged_gdf["most_recent_year_owed"].astype(str) + "-12-31"
    )

    # Fill missing values with "NA" for string columns
    for col in ["total_due", "total_assessment"]:
        merged_gdf[col] = merged_gdf[col].fillna("NA")

    delinquency_cols = [
        "most_recent_year_owed",
    ]
    merged_gdf[delinquency_cols] = merged_gdf[delinquency_cols].fillna("NA")

    return merged_gdf, input_validation

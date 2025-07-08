from typing import List, Tuple

import geopandas as gpd
import pandas as pd

from src.validation.base import ValidationResult, validate_output
from src.validation.li_violations import (
    LIViolationsOutputValidator,
    LIViolationsInputValidator,
)

from ..classes.loaders import CartoLoader
from ..constants.services import VIOLATIONS_SQL_QUERY
from ..utilities import opa_join


@validate_output(LIViolationsOutputValidator)
def li_violations(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Process L&I (Licenses and Inspections) data for violations.

    This function filters and processes L&I violations data,
    joining it with the primary feature layer based on spatial relationships
    and OPA (Office of Property Assessment) identifiers.

    Args:
        primary_featurelayer (FeatureLayer): The primary feature layer to join L&I data to.

    Returns:
        FeatureLayer: The primary feature layer updated with L&I data.

    Tagline:
        Counts L&I violations

    Columns added:
        all_violations_past_year (int): Total violations in the past year.
        open_violations_past_year (int): Open violations in the past year.

    Source:
        https://phl.carto.com/api/v2/sql

    Primary Feature Layer Columns Referenced:
        opa_id
    """
    keywords: List[str] = [
        "dumping",
        "blight",
        "rubbish",
        "weeds",
        "graffiti",
        "abandoned",
        "sanitation",
        "litter",
        "vacant",
        "trash",
        "unsafe",
    ]

    loader = CartoLoader(
        name="LI Violations",
        carto_queries=VIOLATIONS_SQL_QUERY,
        opa_col="opa_account_num",
        validator=LIViolationsInputValidator(),
    )

    l_and_i_violations, input_validation = loader.load_or_fetch()

    # Filter for rows where 'casetype' contains any of the keywords, handling NaN values
    l_and_i_violations = l_and_i_violations[
        l_and_i_violations["violationcodetitle"]
        .fillna("")
        .str.lower()
        .str.contains("|".join(keywords))
    ]

    all_violations_count_df: pd.DataFrame = (
        l_and_i_violations.groupby("opa_id")
        .count()
        .reset_index()[["opa_id", "violationnumber", "geometry"]]
    )
    all_violations_count_df = all_violations_count_df.rename(
        columns={"violationnumber": "all_violations_past_year"}
    )
    # filter for only cases where the casestatus is 'IN VIOLATION' or 'UNDER INVESTIGATION'
    violations_gdf: gpd.GeoDataFrame = l_and_i_violations[
        (l_and_i_violations["violationstatus"].str.lower() == "open")
    ]

    open_violations_count_df: pd.DataFrame = (
        violations_gdf.groupby("opa_id")
        .count()
        .reset_index()[["opa_id", "violationnumber", "geometry"]]
    )
    open_violations_count_df = open_violations_count_df.rename(
        columns={"violationnumber": "open_violations_past_year"}
    )
    # join the all_violations_count_df and open_violations_count_df dataframes on opa_id
    violations_count_gdf: gpd.GeoDataFrame = all_violations_count_df.merge(
        open_violations_count_df, how="left", on="opa_id"
    )

    # replace NaN values with 0
    violations_count_gdf.fillna(0, inplace=True)

    # convert the all_violations_past_year and open_violations_past_year columns to integers
    violations_count_gdf["all_violations_past_year"] = violations_count_gdf[
        "all_violations_past_year"
    ].astype(int)
    violations_count_gdf["open_violations_past_year"] = violations_count_gdf[
        "open_violations_past_year"
    ].astype(int)
    violations_count_gdf = violations_count_gdf[
        ["opa_id", "all_violations_past_year", "open_violations_past_year"]
    ]

    # collapse violations_gdf by address and concatenate the violationcodetitle values into a list with a semicolon separator
    l_and_i_violations = (
        l_and_i_violations.groupby("geometry")["violationcodetitle"]
        .apply(lambda x: "; ".join([val for val in x if val is not None]))
        .reset_index()
    )

    # rename the column to 'li_violations'
    l_and_i_violations.rename(
        columns={"violationcodetitle": "li_code_violations"}, inplace=True
    )

    # Violations can work with an OPA join
    merged_gdf = opa_join(
        input_gdf,
        violations_count_gdf,
    )

    merged_gdf[["all_violations_past_year", "open_violations_past_year"]] = (
        merged_gdf[["all_violations_past_year", "open_violations_past_year"]]
        .apply(lambda x: pd.to_numeric(x, errors="coerce"))
        .fillna(0)
        .astype(int)
    )

    return merged_gdf, input_validation

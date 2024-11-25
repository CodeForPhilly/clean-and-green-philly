import pandas as pd
import geopandas as gpd
from typing import List
from ..classes.featurelayer import FeatureLayer
from ..constants.services import VIOLATIONS_SQL_QUERY


def li_violations(primary_featurelayer: FeatureLayer) -> FeatureLayer:
    """
    Process L&I (Licenses and Inspections) data for violations.

    This function filters and processes L&I violations data,
    joining it with the primary feature layer based on spatial relationships
    and OPA (Office of Property Assessment) identifiers.

    Args:
        primary_featurelayer (FeatureLayer): The primary feature layer to join L&I data to.

    Returns:
        FeatureLayer: The primary feature layer updated with L&I data.
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

    # Load data for violations from L&I
    l_and_i_violations: FeatureLayer = FeatureLayer(
        name="LI Violations", carto_sql_queries=VIOLATIONS_SQL_QUERY, from_xy=True
    )

    # Filter for rows where 'casetype' contains any of the keywords, handling NaN values
    l_and_i_violations.gdf = l_and_i_violations.gdf[
        l_and_i_violations.gdf["violationcodetitle"]
        .fillna("")
        .str.lower()
        .str.contains("|".join(keywords))
    ]

    all_violations_count_df: pd.DataFrame = (
        l_and_i_violations.gdf.groupby("opa_account_num")
        .count()
        .reset_index()[["opa_account_num", "violationnumber", "geometry"]]
    )
    all_violations_count_df = all_violations_count_df.rename(
        columns={"violationnumber": "all_violations_past_year"}
    )
    # filter for only cases where the casestatus is 'IN VIOLATION' or 'UNDER INVESTIGATION'
    violations_gdf: gpd.GeoDataFrame = l_and_i_violations.gdf[
        (l_and_i_violations.gdf["violationstatus"].str.lower() == "open")
    ]

    open_violations_count_df: pd.DataFrame = (
        violations_gdf.groupby("opa_account_num")
        .count()
        .reset_index()[["opa_account_num", "violationnumber", "geometry"]]
    )
    open_violations_count_df = open_violations_count_df.rename(
        columns={"violationnumber": "open_violations_past_year"}
    )
    # join the all_violations_count_df and open_violations_count_df dataframes on opa_account_num
    violations_count_gdf: gpd.GeoDataFrame = all_violations_count_df.merge(
        open_violations_count_df, how="left", on="opa_account_num"
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
        ["opa_account_num", "all_violations_past_year", "open_violations_past_year"]
    ]

    # collapse violations_gdf by address and concatenate the violationcodetitle values into a list with a semicolon separator
    l_and_i_violations.gdf = (
        l_and_i_violations.gdf.groupby("geometry")["violationcodetitle"]
        .apply(lambda x: "; ".join([val for val in x if val is not None]))
        .reset_index()
    )

    # rename the column to 'li_violations'
    l_and_i_violations.gdf.rename(
        columns={"violationcodetitle": "li_code_violations"}, inplace=True
    )

    # Violations can work with an OPA join
    primary_featurelayer.opa_join(
        violations_count_gdf,
        "opa_account_num",
    )

    primary_featurelayer.gdf[
        ["all_violations_past_year", "open_violations_past_year"]
    ] = (
        primary_featurelayer.gdf[
            ["all_violations_past_year", "open_violations_past_year"]
        ]
        .apply(lambda x: pd.to_numeric(x, errors="coerce"))
        .fillna(0)
        .astype(int)
    )

    return primary_featurelayer

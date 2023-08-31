from classes.featurelayer import FeatureLayer
from constants.services import COMPLAINTS_SQL_QUERY, VIOLATIONS_SQL_QUERY


def l_and_i(primary_featurelayer):
    # Calculate one year ago from today's date
    l_and_i_complaints = FeatureLayer(
        name="LI Complaints", carto_sql_queries=COMPLAINTS_SQL_QUERY
    )

    # filter for only Status = 'Open'
    l_and_i_complaints.gdf = l_and_i_complaints.gdf[
        l_and_i_complaints.gdf["status"] == "Open"
    ]

    # Group by geometry and concatenate the violationcodetitle values into a list with a semicolon separator
    l_and_i_complaints.gdf = (
        l_and_i_complaints.gdf.groupby("geometry")["service_name"]
        .apply(lambda x: "; ".join([val for val in x if val is not None]))
        .reset_index()
    )
    l_and_i_complaints.rebuild_gdf()

    # collapse complaints_gdf by address and concatenate the violationcodetitle values into a list with a semicolon separator
    # l_and_i_complaints.gdf = l_and_i_complaints.gdf.groupby('address')['service_name'].apply(lambda x: '; '.join([val for val in x if val is not None])).reset_index()

    # rename the column to 'li_complaints'
    l_and_i_complaints.gdf.rename(
        columns={"service_name": "li_complaints"}, inplace=True
    )

    # Load data for violations from L&I
    l_and_i_violations = FeatureLayer(
        name="LI Violations", carto_sql_queries=VIOLATIONS_SQL_QUERY, from_xy=True
    )

    all_violations_count_df = (
        l_and_i_violations.gdf.groupby("opa_account_num")
        .count()
        .reset_index()[["opa_account_num", "violationnumber", "geometry"]]
    )
    all_violations_count_df = all_violations_count_df.rename(
        columns={"violationnumber": "all_violations_past_year"}
    )
    # filter for only cases where the casestatus is 'IN VIOLATION' or 'UNDER INVESTIGATION'
    violations_gdf = l_and_i_violations.gdf[
        (l_and_i_violations.gdf["violationstatus"] == "OPEN")
    ]

    open_violations_count_df = (
        violations_gdf.groupby("opa_account_num")
        .count()
        .reset_index()[["opa_account_num", "violationnumber", "geometry"]]
    )
    open_violations_count_df = open_violations_count_df.rename(
        columns={"violationnumber": "open_violations_past_year"}
    )
    # join the all_violations_count_df and open_violations_count_df dataframes on opa_account_num
    violations_count_gdf = all_violations_count_df.merge(
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

    # collapse violations_gdf by address and concatenate the violationcodetitle values into a list with a semicolon separator
    l_and_i_violations.gdf = (
        l_and_i_violations.gdf.groupby("geometry")["violationcodetitle"]
        .apply(lambda x: "; ".join([val for val in x if val is not None]))
        .reset_index()
    )
    l_and_i_complaints.rebuild_gdf()

    # rename the column to 'li_violations'
    l_and_i_violations.gdf.rename(
        columns={"violationcodetitle": "li_code_violations"}, inplace=True
    )

    # left join the complaints_gdf to the joined_gdf on address
    primary_featurelayer.spatial_join(l_and_i_violations, predicate="contains")

    # left join the violations_gdf to the joined_gdf on opa_account_num
    primary_featurelayer.spatial_join(l_and_i_complaints, predicate="contains")

    return primary_featurelayer

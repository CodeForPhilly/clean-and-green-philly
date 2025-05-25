import geopandas as gpd
import pandas as pd


def opa_join(
    first_gdf: gpd.GeoDataFrame, second_gdf: gpd.GeoDataFrame, opa_column: str
) -> gpd.GeoDataFrame:
    """
    Join 2 dataframes based on opa_id and keeps the 'geometry' column from the left dataframe if it exists in both.
    Assumes that the two dataframes are in standardized form with a string "opa_id" column and geometry columns.
    """

    joined = first_gdf.merge(second_gdf, how="left", on="opa_id")

    # Check if 'geometry' column exists in both dataframes and clean up
    if "geometry_x" in joined.columns and "geometry_y" in joined.columns:
        joined = joined.drop(columns=["geometry_y"]).copy()  # Ensure a full copy
        joined = joined.rename(columns={"geometry_x": "geometry"})

    joined.set_geometry("geometry")
    return joined


def spatial_join(
    first_gdf: gpd.GeoDataFrame,
    second_gdf: gpd.GeoDataFrame,
    how="left",
    predicate="intersects",
) -> gpd.GeoDataFrame:
    """
    Spatial joins in this script are generally left intersect joins.
    They also can create duplicates, so we drop duplicates after the join.
    Note: We may want to revisit the duplicates.
    """
    joined = gpd.sjoin(first_gdf, second_gdf, how=how, predicate=predicate)
    joined.drop(columns=["index_right"], inplace=True)
    joined.drop_duplicates(inplace=True)

    joined = joined.dropna(subset=["opa_id"])

    return joined

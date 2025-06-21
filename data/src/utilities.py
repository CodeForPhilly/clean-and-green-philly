import time

import geopandas as gpd


def opa_join(
    first_gdf: gpd.GeoDataFrame, second_gdf: gpd.GeoDataFrame, opa_col: str = "opa_id"
) -> gpd.GeoDataFrame:
    """
    Join 2 dataframes based on opa_id and keeps the 'geometry' column from the left dataframe if it exists in both.
    Assumes that the two dataframes are in standardized form with a string "opa_id" column and geometry columns.
    """
    start_time = time.time()
    print(
        f"    opa_join: Starting join with {len(first_gdf)} and {len(second_gdf)} rows"
    )

    dropna_start = time.time()
    first_gdf.dropna(subset=[opa_col], inplace=True)
    second_gdf.dropna(subset=[opa_col], inplace=True)
    dropna_time = time.time() - dropna_start
    print(f"    opa_join: dropna operations took {dropna_time:.2f}s")

    merge_start = time.time()
    joined = first_gdf.merge(second_gdf, how="left", on=opa_col)
    merge_time = time.time() - merge_start
    print(f"    opa_join: merge operation took {merge_time:.2f}s")

    # Check if 'geometry' column exists in both dataframes and clean up
    cleanup_start = time.time()
    if "geometry_x" in joined.columns and "geometry_y" in joined.columns:
        joined = (
            joined.drop(columns=["geometry_y"])
            .rename(columns={"geometry_x": "geometry"})
            .copy()
        )

    joined = gpd.GeoDataFrame(joined, geometry="geometry", crs=first_gdf.crs)
    cleanup_time = time.time() - cleanup_start
    print(f"    opa_join: cleanup operations took {cleanup_time:.2f}s")

    total_time = time.time() - start_time
    print(
        f"    opa_join: Total join completed in {total_time:.2f}s ({len(joined)} rows)"
    )

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
    start_time = time.time()
    print(
        f"    spatial_join: Starting spatial join with {len(first_gdf)} and {len(second_gdf)} rows"
    )

    sjoin_start = time.time()
    joined = gpd.sjoin(first_gdf, second_gdf, how=how, predicate=predicate)
    sjoin_time = time.time() - sjoin_start
    print(f"    spatial_join: gpd.sjoin took {sjoin_time:.2f}s ({len(joined)} rows)")

    cleanup_start = time.time()
    joined.drop(columns=["index_right"], inplace=True)
    joined.drop_duplicates(inplace=True)
    joined.dropna(subset=["opa_id"], inplace=True)
    cleanup_time = time.time() - cleanup_start
    print(f"    spatial_join: cleanup operations took {cleanup_time:.2f}s")

    total_time = time.time() - start_time
    print(
        f"    spatial_join: Total spatial join completed in {total_time:.2f}s ({len(joined)} rows)"
    )

    return joined

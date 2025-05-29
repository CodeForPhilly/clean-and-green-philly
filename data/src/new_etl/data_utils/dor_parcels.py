import geopandas as gpd
from shapely.strtree import STRtree

from new_etl.classes.featurelayer import GdfLoader
from new_etl.utilities import spatial_join

from ..constants.services import DOR_PARCELS_URL
from config.config import USE_CRS


def dor_parcels(input_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Updates the primary feature layer by replacing its geometry column with
    polygon geometries from DOR parcels where intersections occur.

    Args:
    primary_featurelayer (FeatureLayer): The primary feature layer to update.

    Returns:
    FeatureLayer: The updated primary feature layer with geometries replaced
    by DOR parcel polygons where possible.
    """
    print("Loading DOR properties from GeoJSON...")

    # Load and preprocess DOR parcels
    loader = GdfLoader(name="DOR Parcels", url=DOR_PARCELS_URL)
    dor_parcels = loader.load_or_fetch()

    # dor_parcels["geometry"] = dor_parcels["geometry"].make_valid()
    dor_parcels = dor_parcels[
        dor_parcels["STATUS"] == 1
    ]  # filter for what I think are only active parcel boundaries

    # Filter only valid polygon or multipolygon geometries
    dor_parcels = dor_parcels[
        dor_parcels.geometry.type.isin(["Polygon", "MultiPolygon"])
    ]
    print(
        f"Number of valid polygon/multipolygon geometries in DOR parcels: {len(dor_parcels)}"
    )

    # Perform spatial join to identify intersecting polygons
    print("Performing spatial join between points and polygons...")

    merged_gdf = spatial_join(input_gdf, dor_parcels[["geometry"]])

    # Replace point geometries with polygon geometries where intersections occur
    mask = ~merged_gdf["index_right"].isna()
    merged_gdf.loc[mask, "geometry"] = dor_parcels.loc[
        merged_gdf.loc[mask, "index_right"], "geometry"
    ].values

    # Drop spatial join index column
    merged_gdf.drop(columns=["index_right"], errors="ignore", inplace=True)

    # Update primary feature layer
    input_gdf = gpd.GeoDataFrame(merged_gdf, geometry="geometry", crs=USE_CRS)

    # Count match statistics
    total_rows = len(merged_gdf)
    matched_rows = mask.sum()
    unmatched_rows = total_rows - matched_rows

    print(f"Total rows: {total_rows}")
    print(f"Matched rows (with polygons): {matched_rows}")
    print(f"Unmatched rows: {unmatched_rows}")

    # Filter out POINT geometries
    input_gdf = input_gdf[input_gdf.geometry.type.isin(["Polygon", "MultiPolygon"])]

    # Dissolve overlapping parcels by opa_id
    print("Dissolving overlapping parcels by opa_id...")
    input_gdf = input_gdf.dissolve(by="opa_id", as_index=False)
    print(f"Size of primary feature layer after dissolve: {len(input_gdf)}")

    # Create an STRtree for fast spatial indexing of the parcel geometries
    parcel_tree = STRtree(input_gdf.geometry)

    # Count overlapping geometries
    overlapping_count = input_gdf.geometry.apply(
        lambda geom: len(parcel_tree.query(geom))
    )
    print("Number of overlaps per parcel after dissolve:")
    print(overlapping_count.value_counts())

    # Count and drop duplicate opa_ids in the primary feature layer
    multiple_matches = input_gdf.duplicated(subset="opa_id", keep=False).sum()
    print(
        f"Rows with duplicate opa_id values in the primary feature layer: {multiple_matches}"
    )

    # Drop duplicates based on opa_id
    input_gdf = input_gdf.drop_duplicates(subset="opa_id", keep="first")
    print(
        f"Updated size of primary feature layer after dropping duplicates: {len(input_gdf)}"
    )

    return input_gdf

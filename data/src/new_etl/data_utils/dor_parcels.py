from ..classes.featurelayer import FeatureLayer
from ..constants.services import DOR_PARCELS_URL
import geopandas as gpd
from config.config import USE_CRS

def dor_parcels(primary_featurelayer: FeatureLayer) -> FeatureLayer:
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
    dor_parcels = gpd.read_file(DOR_PARCELS_URL).to_crs(USE_CRS)
    dor_parcels["geometry"] = dor_parcels["geometry"].make_valid()
    
    # Filter only valid polygon or multipolygon geometries
    dor_parcels = dor_parcels[dor_parcels.geometry.type.isin(["Polygon", "MultiPolygon"])]
    print(f"Number of valid polygon/multipolygon geometries in DOR parcels: {len(dor_parcels)}")
    
    # Ensure the primary feature layer has the same CRS
    primary_featurelayer.gdf = primary_featurelayer.gdf.to_crs(USE_CRS)
    
    # Perform spatial join to identify intersecting polygons
    print("Performing spatial join between points and polygons...")
    spatial_join_result = gpd.sjoin(
        primary_featurelayer.gdf,
        dor_parcels[["geometry"]],  # Only keep geometry column
        how="left", 
        predicate="intersects"
    )
    
    # Replace point geometries with polygon geometries where intersections occur
    mask = ~spatial_join_result["index_right"].isna()
    spatial_join_result.loc[mask, "geometry"] = dor_parcels.loc[
        spatial_join_result.loc[mask, "index_right"], 
        "geometry"
    ].values
    
    # Drop spatial join index column
    spatial_join_result.drop(columns=["index_right"], errors="ignore", inplace=True)
    
    # Update primary feature layer
    primary_featurelayer.gdf = gpd.GeoDataFrame(
        spatial_join_result,
        geometry="geometry",
        crs=USE_CRS
    )
    
    # Count match statistics
    total_rows = len(spatial_join_result)
    matched_rows = mask.sum()
    unmatched_rows = total_rows - matched_rows
    
    print(f"Total rows: {total_rows}")
    print(f"Matched rows (with polygons): {matched_rows}")
    print(f"Unmatched rows: {unmatched_rows}")

    # Count and drop duplicate opa_ids in the primary feature layer
    multiple_matches = primary_featurelayer.gdf.duplicated(subset="opa_id", keep=False).sum()
    print(f"Rows with duplicate opa_id values in the primary feature layer: {multiple_matches}")
    primary_featurelayer.gdf = primary_featurelayer.gdf[~primary_featurelayer.gdf.duplicated(subset="opa_id", keep=False)]
    print(f"Updated size of primary feature layer after dropping duplicates: {len(primary_featurelayer.gdf)}")

    return primary_featurelayer
import os
import tempfile
import datetime
from typing import Tuple

import rioxarray as rxr
import xarray as xr
import geopandas as gpd
import exactextract
import pystac_client
import planetary_computer
import odc.stac
from shapely.geometry import Polygon, MultiPolygon, box

from ..classes.featurelayer import FeatureLayer
from ..metadata.metadata_utils import provide_metadata
from config.config import USE_CRS
from ..constants.services import CENSUS_BGS_URL


def get_current_summer_year() -> int:
    """
    Determine the most recent summer year based on current date.

    Summer is defined as June-August. If current month is before June,
    the most recent summer was last year.

    Returns:
        int: The year of the most recent summer
    """
    today = datetime.datetime.now()
    if today.month < 6:  # Before June
        return today.year - 1
    else:
        return today.year


def get_bbox_from_census_data() -> Tuple[Polygon, Tuple[float, float, float, float]]:
    """
    Get bounding box from census block groups data.

    Returns:
        Tuple[Polygon, Tuple[float, float, float, float]]:
            A tuple containing the boundary as a Polygon and the bounding box coordinates
    """

    census_gdf = gpd.read_file(CENSUS_BGS_URL)
    census_gdf = census_gdf.to_crs(
        "EPSG:4326"
    )  # needs 4326 for planetary computer query

    # Get bounds
    minx, miny, maxx, maxy = census_gdf.total_bounds
    bbox_coords = (minx, miny, maxx, maxy)

    return box(minx, miny, maxx, maxy), bbox_coords


def is_cache_valid(cache_path: str, current_summer_year: int) -> bool:
    """
    Check if the cached NDVI raster exists and is from the current summer year.

    Args:
        cache_path (str): Path to the cached raster file
        current_summer_year (int): The year of the most recent summer

    Returns:
        bool: True if the cache is valid, False otherwise
    """
    if not os.path.exists(cache_path):
        return False

    # Check if the filename includes the current summer year
    filename = os.path.basename(cache_path)
    if f"summer_{current_summer_year}" not in filename:
        return False

    # Verify the file is a valid raster
    try:
        with rxr.open_rasterio(cache_path) as rds:
            if rds.rio.shape and rds.rio.crs:
                return True
    except Exception as e:
        print(f"Error checking cached file: {e}")

    return False


def get_median_ndvi_planetary(
    year: int, bbox_coords: Tuple[float, float, float, float]
) -> xr.DataArray:
    """
    Get Sentinel-2 median NDVI for a specific summer period using batch processing.

    Args:
        year (int): The year to process
        bbox_coords (Tuple[float, float, float, float]): Bounding box coordinates (minx, miny, maxx, maxy)

    Returns:
        xr.DataArray: The processed NDVI data

    Raises:
        ValueError: If no suitable Sentinel-2 data is found
    """
    # Connect to the Planetary Computer STAC API with proper signing
    catalog = pystac_client.Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1",
        modifier=planetary_computer.sign_inplace,
    )

    # Summer period date range
    date_range = f"{year}-06-01/{year}-08-31"
    cloud_cover_threshold = 20  # Cloud cover percentage threshold

    # Search for Sentinel-2 Level-2A data
    search = catalog.search(
        collections=["sentinel-2-l2a"],
        bbox=bbox_coords,
        datetime=date_range,
        query={"eo:cloud_cover": {"lt": cloud_cover_threshold}},
    )

    items = search.item_collection()

    if not items:
        # Try with a higher cloud cover threshold if no items found
        cloud_cover_threshold = 50
        search = catalog.search(
            collections=["sentinel-2-l2a"],
            bbox=bbox_coords,
            datetime=date_range,
            query={"eo:cloud_cover": {"lt": cloud_cover_threshold}},
        )
        items = search.item_collection()
        print(f"Retried with higher cloud threshold, found {len(items)} scenes")

        if not items:
            raise ValueError(f"No Sentinel-2 data found for {date_range}")

    # Define bands of interest - we only need red and nir for NDVI
    bands_of_interest = ["red", "nir"]

    # Load all items at once using odc.stac
    try:
        # Load all scenes at once
        ds = odc.stac.stac_load(
            items,
            bands=bands_of_interest,
            bbox=bbox_coords,
            resolution=10,  # 10m resolution for Sentinel-2
            chunks={},  # Enable Dask for memory efficiency
        )

        # Create a composite by taking the median across the time dimension
        ds_composite = ds.median(dim="time")

        # Calculate NDVI
        red = ds_composite.red
        nir = ds_composite.nir

        # Handle potential scaling issues
        if float(red.max()) > 1:
            red = red / 10000.0
        if float(nir.max()) > 1:
            nir = nir / 10000.0

        ndvi = (nir - red) / (nir + red)

        # Return as a DataArray with proper attributes
        ndvi.attrs = ds_composite.attrs

        return ndvi

    except Exception as e:
        print(f"Error in batch processing for {year}: {e}")
        raise


def generate_ndvi_data(
    cache_path: str, bbox_geom: Polygon, bbox_coords: Tuple[float, float, float, float]
) -> xr.Dataset:
    """
    Generate NDVI data for current and previous summer years.

    Args:
        cache_path (str): Path where the NDVI data will be cached
        bbox_geom (Polygon): Boundary geometry
        bbox_coords (Tuple[float, float, float, float]): Bounding box coordinates

    Returns:
        xr.Dataset: Dataset containing NDVI and NDVI change rasters

    Note:
        The output raster will be approximately 65MB in size.
        Full processing typically takes 10-15 minutes.
    """
    # Get current summer year
    current_summer_year = get_current_summer_year()
    previous_summer_year = current_summer_year - 1

    print(
        f"Generating NDVI data for summers {previous_summer_year} and {current_summer_year}"
    )

    # Get median NDVI for both years
    ndvi_current = get_median_ndvi_planetary(current_summer_year, bbox_coords)
    ndvi_current = ndvi_current.rename("ndvi")

    ndvi_previous = get_median_ndvi_planetary(previous_summer_year, bbox_coords)
    ndvi_previous = ndvi_previous.rename("ndvi_previous")

    # Calculate change
    ndvi_change = ndvi_current - ndvi_previous
    ndvi_change = ndvi_change.rename("ndvi_one_year_change")

    # Combine bands into a dataset
    combined = xr.Dataset({"ndvi": ndvi_current, "ndvi_one_year_change": ndvi_change})

    # Mask invalid values
    valid_mask = ndvi_current >= -2
    combined = combined.where(valid_mask)

    # Save to cache file
    print(f"Saving NDVI data to {cache_path}")
    combined.rio.to_raster(cache_path)

    return combined


def extract_ndvi_to_parcels(
    raster_path: str, parcel_gdf: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """
    Extract NDVI values to parcels.

    Args:
        raster_path (str): Path to the NDVI raster
        parcel_gdf (gpd.GeoDataFrame): GeoDataFrame containing parcels

    Returns:
        gpd.GeoDataFrame: GeoDataFrame with NDVI statistics added

    Note:
        This extraction process typically takes about 3 minutes.
    """
    # Clean the GeoDataFrame
    gdf_clean = parcel_gdf[
        parcel_gdf.geometry.notnull()
        & parcel_gdf.geometry.is_valid
        & parcel_gdf.geometry.apply(lambda g: isinstance(g, (Polygon, MultiPolygon)))
    ].copy()

    # Check if the raster exists
    if not os.path.exists(raster_path):
        raise FileNotFoundError(f"Raster file not found: {raster_path}")

    # Open the raster
    with rxr.open_rasterio(raster_path) as rds:
        raster_crs = rds.rio.crs

        # Reproject raster if needed
        if str(raster_crs) != str(USE_CRS):
            rds = rds.rio.reproject(USE_CRS)

            # Create a temporary file for the reprojected raster
            temp_reprojected_path = raster_path.replace(".tif", "_reprojected.tif")
            rds.rio.to_raster(temp_reprojected_path)
            raster_path = temp_reprojected_path

    # Convert parcel CRS to USE_CRS
    if str(gdf_clean.crs) != str(USE_CRS):
        gdf_clean = gdf_clean.to_crs(USE_CRS)

    # Define columns to include in extraction
    include_cols = list(gdf_clean.columns)

    print(f"Extracting NDVI data to {len(gdf_clean)} parcels...")
    results = exactextract.exact_extract(
        raster_path,
        gdf_clean,
        ["mean"],
        output="pandas",
        include_cols=include_cols,
        strategy="raster-sequential",
        progress=True,
    )

    return results


@provide_metadata()
def ndvi(primary_featurelayer: FeatureLayer) -> FeatureLayer:
    """
    Calculate and add NDVI features to the primary feature layer.

    This function retrieves Sentinel-2 satellite imagery for the most recent summer
    period (June-August) and the previous summer, calculates the median Normalized
    Difference Vegetation Index (NDVI) for each period, and then adds the NDVI values
    and year-over-year change to each parcel.

    NDVI is a measure of vegetation greenness, with values ranging from -1 to 1.
    Higher values indicate more dense, healthy vegetation.

    We use the median peak NDVI over the summer months to capture when land is at
    its greenest. Lower resolution Sentinel-2 data (10m) provides sufficient accuracy
    for the parcel-level analysis while requiring less storage and processing time
    than higher resolution alternatives.

    Args:
        primary_featurelayer (FeatureLayer): Input feature layer containing parcels

    Returns:
        FeatureLayer: Feature layer with added NDVI features

    Note:
        - Full processing (including data retrieval) takes approximately 10-15 minutes
        - Extraction alone takes about 3 minutes
        - The intermediate raster file is approximately 65MB
        - This process typically only needs to run once per year, after summer ends

    Added columns:
        - ndvi_mean: Mean NDVI value for the parcel (current summer)
        - ndvi_one_year_change_mean: Mean year-over-year NDVI change
    """
    # Create a temporary directory for cache files
    temp_dir = tempfile.gettempdir()
    current_summer_year = get_current_summer_year()
    ndvi_cache_path = os.path.join(
        temp_dir, f"ndvi_data_summer_{current_summer_year}.tif"
    )

    # Get boundary
    boundary, bbox_coords = get_bbox_from_census_data()

    # Check if we need to regenerate the NDVI data
    if not is_cache_valid(ndvi_cache_path, current_summer_year):
        print("Generating new NDVI data...")
        generate_ndvi_data(ndvi_cache_path, boundary, bbox_coords)
    else:
        print("Using cached NDVI data")

    # Get the GeoDataFrame from the feature layer
    parcel_gdf = primary_featurelayer.gdf

    # Extract NDVI values to parcels
    results = extract_ndvi_to_parcels(ndvi_cache_path, parcel_gdf)

    # Update the primary feature layer with the new columns from results
    # (instead of creating a new one)
    for column in results.columns:
        if column not in primary_featurelayer.gdf.columns:
            primary_featurelayer.gdf[column] = results[column]

    return primary_featurelayer

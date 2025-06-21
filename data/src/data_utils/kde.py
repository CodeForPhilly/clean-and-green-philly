import functools
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Tuple

import geopandas as gpd
import mapclassify
import numpy as np
import rasterio
from awkde.awkde import GaussianKDE
from rasterio.transform import Affine
from tqdm import tqdm

from src.classes.file_manager import FileManager, LoadType
from src.config.config import USE_CRS
from src.validation.base import ValidationResult

from ..classes.loaders import CartoLoader


# Profiling utilities
def timer(func):
    """Decorator to time function execution"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"⏱️  {func.__name__} took {end_time - start_time:.4f} seconds")
        return result

    return wrapper


def profile_section(section_name: str):
    """Context manager for profiling code sections"""

    class Profiler:
        def __init__(self, name):
            self.name = name
            self.start_time = None

        def __enter__(self):
            self.start_time = time.time()
            return self

        def __exit__(self, _exc_type, _exc_val, _exc_tb):
            end_time = time.time()
            duration = end_time - self.start_time
            print(f"⏱️  {self.name}: {duration:.4f} seconds")

    return Profiler(section_name)


resolution = 1320  # 0.25 miles (in feet, since the CRS is 2272)
batch_size = 50000

file_manager = FileManager()


def kde_predict_chunk(kde: GaussianKDE, chunk: np.ndarray) -> np.ndarray:
    """
    Helper function to predict KDE for a chunk of grid points.

    Args:
        kde (GaussianKDE): The KDE model to use for prediction.
        chunk (np.ndarray): A chunk of grid points for prediction.

    Returns:
        np.ndarray: Predicted KDE values for the chunk.
    """
    return kde.predict(chunk)


@timer
def generic_kde(
    name: str, query: str, resolution: int = resolution, batch_size: int = batch_size
) -> Tuple[str, np.ndarray]:
    """
    Generates a raster file and grid points from kernel density estimation (KDE) for a dataset.

    Args:
        name (str): Name of the dataset being processed.
        query (str): SQL query to fetch data.
        resolution (int): Resolution for the grid. Defaults to 1320.
        batch_size (int): Batch size for processing grid points. Defaults to 100000.

    Returns:
        Tuple[str, np.ndarray]: The raster filename and the array of input points.
    """
    print(f"Initializing FeatureLayer for {name}")

    # Profile data loading
    with profile_section("Data Loading"):
        loader = CartoLoader(name=name, carto_queries=query)
        gdf, input_validation = loader.load_or_fetch()

    gdf.dropna(subset=["geometry"], inplace=True)

    # Profile coordinate extraction
    with profile_section("Coordinate Extraction"):
        coords = np.array([geom.xy for geom in gdf.geometry])
        x, y = coords[:, 0, :].flatten(), coords[:, 1, :].flatten()
        X = np.column_stack((x, y))

    # Profile grid generation
    with profile_section(
        "Grid Generation (np.linspace + np.meshgrid + np.column_stack)"
    ):
        x_grid, y_grid = (
            np.linspace(x.min(), x.max(), resolution),
            np.linspace(y.min(), y.max(), resolution),
        )
        xx, yy = np.meshgrid(x_grid, y_grid)
        grid_points = np.column_stack((xx.ravel(), yy.ravel()))

    # Profile KDE fitting
    with profile_section("KDE Fitting"):
        print(f"Fitting KDE for {name} data")
        kde = GaussianKDE(glob_bw=0.1, alpha=0.999, diag_cov=True)
        kde.fit(X)

    print(f"Predicting KDE values for grid of size {grid_points.shape}")

    # Profile the entire prediction loop
    with profile_section("Entire Prediction Loop"):
        # Profile chunk creation
        with profile_section("Chunk Creation"):
            chunks = [
                grid_points[i : i + batch_size]
                for i in range(0, len(grid_points), batch_size)
            ]
            print(
                f"📊 Created {len(chunks)} chunks of size {batch_size} (total grid points: {len(grid_points)})"
            )

        z = np.zeros(len(grid_points))

        with ProcessPoolExecutor() as executor:
            futures = {
                executor.submit(kde_predict_chunk, kde, chunk): i
                for i, chunk in enumerate(tqdm(chunks, desc="Submitting tasks"))
            }

            for future in tqdm(
                as_completed(futures), total=len(futures), desc="Processing tasks"
            ):
                i = futures[future]
                z[i * batch_size : (i + 1) * batch_size] = future.result()

    zz = z.reshape(xx.shape)

    x_res, y_res = (
        (x.max() - x.min()) / (resolution - 1),
        (y.max() - y.min()) / (resolution - 1),
    )
    min_x, min_y = x.min(), y.min()

    transform = Affine.translation(min_x, min_y) * Affine.scale(x_res, y_res)

    raster_filename = f"{name.lower().replace(' ', '_')}.tif"
    raster_file_path = file_manager.get_file_path(raster_filename, LoadType.TEMP)
    print(f"Saving raster to {raster_filename}")

    # Profile raster saving
    with profile_section("Raster Saving"):
        with rasterio.open(
            raster_file_path,
            "w",
            driver="GTiff",
            height=zz.shape[0],
            width=zz.shape[1],
            count=1,
            dtype=zz.dtype,
            crs=USE_CRS,
            transform=transform,
        ) as dst:
            dst.write(zz, 1)

    return raster_file_path, X, input_validation


@timer
def apply_kde_to_input(
    input_gdf: gpd.GeoDataFrame,
    name: str,
    query: str,
    resolution: int = resolution,
    batch_size: int = batch_size,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Applies KDE to the primary feature layer and adds columns for density, z-score,
    percentile, and percentile as a string.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.
        name (str): Name of the KDE feature.
        query (str): SQL query to fetch data for KDE.
        resolution (int): Resolution for the KDE raster grid.
        batch_size (int): Batch size for processing grid points.

    Returns:
        FeatureLayer: The input feature layer with added KDE-related columns.
    """
    raster_filename, crime_coords, input_validation = generic_kde(
        name, query, resolution, batch_size
    )

    # Profile centroid calculation and coordinate preparation
    with profile_section("Centroid Calculation and Coordinate Preparation"):
        centroids = input_gdf.geometry.centroid

        coord_list = [
            (x, y)
            for x, y in zip(
                centroids.x,
                centroids.y,
            )
        ]

    # Profile raster sampling
    with profile_section("Raster Sampling"):
        with rasterio.open(raster_filename) as src:
            # Load entire raster into memory as numpy array
            raster_array = src.read(1)  # Read the first (and only) band

            # Get the transform for coordinate conversion
            transform = src.transform

            # Convert coordinates to numpy array for vectorized operations
            coords_array = np.array(coord_list)

            # Vectorized coordinate conversion to pixel indices
            rows, cols = ~transform * (coords_array[:, 0], coords_array[:, 1])
            rows = rows.astype(int)
            cols = cols.astype(int)

            # Clip indices to valid bounds
            rows = np.clip(rows, 0, raster_array.shape[0] - 1)
            cols = np.clip(cols, 0, raster_array.shape[1] - 1)

            # Vectorized array indexing
            sampled_values = raster_array[rows, cols].tolist()

    density_column = f"{name.lower().replace(' ', '_')}_density"
    input_gdf[density_column] = sampled_values

    # Profile statistical calculations
    with profile_section("Statistical Calculations (z-scores, percentiles, labels)"):
        # Calculate z-scores
        mean_density = input_gdf[density_column].mean()
        std_density = input_gdf[density_column].std()
        z_score_column = f"{density_column}_zscore"
        input_gdf[z_score_column] = (
            input_gdf[density_column] - mean_density
        ) / std_density

        # Calculate percentiles
        percentile_breaks = list(range(101))
        classifier = mapclassify.Percentiles(
            input_gdf[density_column], pct=percentile_breaks
        )
        percentile_column = f"{density_column}_percentile"
        input_gdf[percentile_column] = classifier.yb.astype(float)

        # Assign percentile labels
        label_column = f"{density_column}_label"
        input_gdf[label_column] = input_gdf[percentile_column].apply(label_percentile)

    print(f"Finished processing {name}")
    return input_gdf, input_validation


def label_percentile(value: float) -> str:
    """
    Converts a percentile value into a human-readable string.

    Args:
        value (float): The percentile value.

    Returns:
        str: The formatted percentile string (e.g., '1st Percentile').
    """
    if 10 <= value % 100 <= 13:
        return f"{value}th Percentile"
    elif value % 10 == 1:
        return f"{value}st Percentile"
    elif value % 10 == 2:
        return f"{value}nd Percentile"
    elif value % 10 == 3:
        return f"{value}rd Percentile"
    else:
        return f"{value}th Percentile"

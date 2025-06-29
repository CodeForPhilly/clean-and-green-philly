import functools
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Tuple

import geopandas as gpd
import mapclassify
import numpy as np
import psutil
import rasterio
from awkde.awkde import GaussianKDE
from rasterio.transform import Affine
from tqdm import tqdm

from src.classes.file_manager import FileManager, LoadType
from src.config.config import USE_CRS, get_logger
from src.validation.base import ValidationResult

from ..classes.loaders import CartoLoader

# Get performance logger
performance_logger = get_logger("performance")


def get_memory_usage():
    """Get current memory usage for the process"""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    return {
        "rss": memory_info.rss / 1024 / 1024,  # MB
        "vms": memory_info.vms / 1024 / 1024,  # MB
        "percent": process.memory_percent(),
    }


def log_memory_usage(stage: str):
    """Log memory usage at a specific stage"""
    memory = get_memory_usage()
    performance_logger.info(
        f"Memory usage at {stage}: "
        f"RSS={memory['rss']:.1f}MB, "
        f"VMS={memory['vms']:.1f}MB, "
        f"Percent={memory['percent']:.1f}%"
    )


def check_system_memory():
    """Check overall system memory availability"""
    memory = psutil.virtual_memory()
    performance_logger.info(
        f"System memory: "
        f"Available={memory.available / 1024 / 1024 / 1024:.1f}GB, "
        f"Used={memory.used / 1024 / 1024 / 1024:.1f}GB, "
        f"Percent={memory.percent:.1f}%"
    )

    # Warn if memory usage is high
    if memory.percent > 85:
        performance_logger.warning(
            f"High system memory usage detected: {memory.percent:.1f}%. "
            f"This may cause performance issues."
        )

    return memory.percent


# Profiling utilities
def timer(func):
    """Decorator to time function execution"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        performance_logger.info(
            f"{func.__name__} took {end_time - start_time:.4f} seconds"
        )
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
            performance_logger.info(f"{self.name}: {duration:.4f} seconds")

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
    performance_logger.info(f"Initializing FeatureLayer for {name}")

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
        performance_logger.info(f"Fitting KDE for {name} data")

        # Debug logging for KDE input data
        performance_logger.info("KDE input data debug:")
        performance_logger.info(f"  Input data shape: {X.shape}")
        performance_logger.info(f"  Input X min: {X[:, 0].min()}, max: {X[:, 0].max()}")
        performance_logger.info(f"  Input Y min: {X[:, 1].min()}, max: {X[:, 1].max()}")
        performance_logger.info(f"  Input data has NaN: {np.isnan(X).any()}")
        performance_logger.info(f"  Input data has Inf: {np.isinf(X).any()}")

        kde = GaussianKDE(glob_bw=0.1, alpha=0.999, diag_cov=True)
        kde.fit(X)

    performance_logger.info(
        f"Predicting KDE values for grid of size {grid_points.shape}"
    )

    # Profile the entire prediction loop
    with profile_section("Entire Prediction Loop"):
        # Profile chunk creation
        with profile_section("Chunk Creation"):
            chunks = [
                grid_points[i : i + batch_size]
                for i in range(0, len(grid_points), batch_size)
            ]
            performance_logger.info(
                f"Created {len(chunks)} chunks of size {batch_size} (total grid points: {len(grid_points)})"
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
    performance_logger.info(f"Saving raster to {raster_filename}")

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

            # Debug logging for raster data
            performance_logger.info("Raster sampling debug:")
            performance_logger.info(f"  Raster shape: {raster_array.shape}")
            performance_logger.info(
                f"  Raster min: {raster_array.min()}, max: {raster_array.max()}"
            )
            performance_logger.info(f"  Raster has NaN: {np.isnan(raster_array).any()}")
            performance_logger.info(f"  Raster has Inf: {np.isinf(raster_array).any()}")
            performance_logger.info(
                f"  Raster unique values count: {len(np.unique(raster_array))}"
            )

            # Get the transform for coordinate conversion
            transform = src.transform

            # Convert coordinates to numpy array for vectorized operations
            coords_array = np.array(coord_list)

            # Debug logging for coordinate conversion
            performance_logger.info(
                f"  Input coordinates min: {coords_array.min(axis=0)}, max: {coords_array.max(axis=0)}"
            )

            # Vectorized coordinate conversion to pixel indices
            rows, cols = ~transform * (coords_array[:, 0], coords_array[:, 1])
            rows = rows.astype(int)
            cols = cols.astype(int)

            # Debug logging for pixel indices
            performance_logger.info(
                f"  Pixel rows min: {rows.min()}, max: {rows.max()}"
            )
            performance_logger.info(
                f"  Pixel cols min: {cols.min()}, max: {cols.max()}"
            )

            # Clip indices to valid bounds
            rows = np.clip(rows, 0, raster_array.shape[0] - 1)
            cols = np.clip(cols, 0, raster_array.shape[1] - 1)

            # Vectorized array indexing
            sampled_values = raster_array[rows, cols].tolist()

            # Debug logging for sampled values
            performance_logger.info(
                f"  Sampled values min: {min(sampled_values)}, max: {max(sampled_values)}"
            )
            performance_logger.info(
                f"  Sampled values unique count: {len(set(sampled_values))}"
            )

    density_column = f"{name.lower().replace(' ', '_')}_density"
    input_gdf[density_column] = sampled_values

    # Profile statistical calculations
    with profile_section("Statistical Calculations (z-scores, percentiles, labels)"):
        # Calculate z-scores
        mean_density = input_gdf[density_column].mean()
        std_density = input_gdf[density_column].std()

        # Debug logging for z-score calculation
        performance_logger.info("Z-score calculation debug:")
        performance_logger.info(f"  Mean density: {mean_density}")
        performance_logger.info(f"  Std density: {std_density}")
        performance_logger.info(f"  Min density: {input_gdf[density_column].min()}")
        performance_logger.info(f"  Max density: {input_gdf[density_column].max()}")
        performance_logger.info(
            f"  Density column has NaN: {input_gdf[density_column].isna().any()}"
        )

        z_score_column = f"{density_column}_zscore"
        z_scores = (input_gdf[density_column] - mean_density) / std_density

        # Debug logging for z-scores
        performance_logger.info(
            f"  Z-scores - Min: {z_scores.min()}, Max: {z_scores.max()}"
        )
        performance_logger.info(f"  Z-scores has NaN: {z_scores.isna().any()}")
        performance_logger.info(f"  Z-scores has Inf: {np.isinf(z_scores).any()}")

        input_gdf[z_score_column] = z_scores

        # Calculate percentiles
        percentile_breaks = list(range(101))
        classifier = mapclassify.Percentiles(
            input_gdf[density_column], pct=percentile_breaks
        )

        # Debug logging for percentile calculation
        performance_logger.info("Percentile calculation debug:")
        performance_logger.info(
            f"  Percentile breaks: {percentile_breaks[:10]}...{percentile_breaks[-10:]}"
        )  # Show first and last 10
        performance_logger.info(f"  Classifier bins: {classifier.bins}")
        performance_logger.info(
            f"  Classifier yb min: {classifier.yb.min()}, max: {classifier.yb.max()}"
        )
        performance_logger.info(
            f"  Classifier yb unique values: {np.unique(classifier.yb)}"
        )

        percentile_column = f"{density_column}_percentile"
        input_gdf[percentile_column] = classifier.yb.astype(int)

        # Debug logging for final percentile column
        performance_logger.info(
            f"  Final percentile column min: {input_gdf[percentile_column].min()}, max: {input_gdf[percentile_column].max()}"
        )
        performance_logger.info(
            f"  Final percentile column unique values: {input_gdf[percentile_column].unique()}"
        )

        # Assign percentile labels
        label_column = f"{density_column}_label"
        input_gdf[label_column] = input_gdf[percentile_column].apply(label_percentile)

    performance_logger.info(f"Finished processing {name}")
    return input_gdf, input_validation


def label_percentile(value: float) -> str:
    """
    Converts a percentile value into a human-readable string.

    Args:
        value (float): The percentile value.

    Returns:
        str: The formatted percentile string (e.g., '1st Percentile').
    """
    # Handle special cases: 11th, 12th, 13th (and 111th, 112th, 113th, etc.)
    if value % 100 in [11, 12, 13]:
        return f"{value}th Percentile"
    elif value % 10 == 1:
        return f"{value}st Percentile"
    elif value % 10 == 2:
        return f"{value}nd Percentile"
    elif value % 10 == 3:
        return f"{value}rd Percentile"
    else:
        return f"{value}th Percentile"

import concurrent.futures
import os
import time
from concurrent.futures import ProcessPoolExecutor
from typing import Tuple

import mapclassify
import numpy as np
import psutil
import rasterio
from awkde.awkde import GaussianKDE
from rasterio.transform import Affine
from tqdm import tqdm

from config.config import USE_CRS

from ..classes.featurelayer import FeatureLayer

# Reduce resolution to make it more manageable while maintaining good spatial detail
resolution = 1320  # 0.25 miles (in feet, since the CRS is 2272)
# Increase chunk size to reduce overhead while keeping reasonable memory usage
# Each chunk takes ~20s to process, so we want chunks that take 1-2 minutes total
batch_size = 50000  # Increased from 25000 to reduce number of chunks


def get_memory_usage():
    """Get current memory usage of the process."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # Convert to MB


def kde_predict_chunk(args):
    """
    Helper function to predict KDE for a chunk of grid points.

    Args:
        args: Tuple containing (chunk, X, glob_bw, alpha, chunk_num, total_chunks)
            chunk: Grid points to predict
            X: Training points
            glob_bw: Bandwidth parameter
            alpha: Alpha parameter
            chunk_num: Current chunk number
            total_chunks: Total number of chunks

    Returns:
        np.ndarray: Predicted KDE values for the chunk
    """
    chunk, X, glob_bw, alpha, chunk_num, total_chunks = args
    try:
        # Create and fit KDE model for this chunk
        kde = GaussianKDE(glob_bw=glob_bw, alpha=alpha, diag_cov=True)
        kde.fit(X)
        return kde.predict(chunk)
    except Exception as e:
        print(f"Error in KDE prediction for chunk {chunk_num + 1}: {str(e)}")
        raise


def generic_kde(
    name: str, query: str, resolution: int = resolution, batch_size: int = batch_size
) -> Tuple[str, np.ndarray]:
    """
    Generates a raster file and grid points from kernel density estimation (KDE) for a dataset.

    Args:
        name (str): Name of the dataset being processed.
        query (str): SQL query to fetch data.
        resolution (int): Resolution for the grid. Defaults to 1320.
        batch_size (int): Batch size for processing grid points. Defaults to 50000.

    Returns:
        Tuple[str, np.ndarray]: The raster filename and the array of input points.
    """
    start_time = time.time()
    print(f"\nInitializing FeatureLayer for {name}")
    print(f"Current memory usage: {get_memory_usage():.1f} MB")

    feature_layer = FeatureLayer(name=name, carto_sql_queries=query)
    print(f"Loaded {len(feature_layer.gdf)} points for {name}")
    print(f"Memory usage after loading data: {get_memory_usage():.1f} MB")

    # Extract coordinates and validate
    coords = np.array([geom.xy for geom in feature_layer.gdf.geometry])
    x, y = coords[:, 0, :].flatten(), coords[:, 1, :].flatten()

    # Remove any points with NaN or infinite coordinates
    valid_mask = ~(np.isnan(x) | np.isnan(y) | np.isinf(x) | np.isinf(y))
    x = x[valid_mask]
    y = y[valid_mask]

    if len(x) == 0:
        raise ValueError("No valid coordinates found after cleaning")

    print(f"Removed {len(coords) - len(x)} invalid points")
    X = np.column_stack((x, y))
    print(f"Extracted coordinates for {len(X)} points")
    print(f"Memory usage after coordinate extraction: {get_memory_usage():.1f} MB")

    # Ensure grid bounds are valid
    x_min, x_max = np.min(x), np.max(x)
    y_min, y_max = np.min(y), np.max(y)

    if not (
        np.isfinite(x_min)
        and np.isfinite(x_max)
        and np.isfinite(y_min)
        and np.isfinite(y_max)
    ):
        raise ValueError("Invalid grid bounds detected")

    x_grid, y_grid = (
        np.linspace(x_min, x_max, resolution),
        np.linspace(y_min, y_max, resolution),
    )
    xx, yy = np.meshgrid(x_grid, y_grid)
    grid_points = np.column_stack((xx.ravel(), yy.ravel()))
    print(f"Created grid with {len(grid_points)} points ({resolution}x{resolution})")
    print(f"Memory usage after grid creation: {get_memory_usage():.1f} MB")

    # Split grid points into chunks
    chunks = [
        grid_points[i : i + batch_size] for i in range(0, len(grid_points), batch_size)
    ]
    print(f"Split into {len(chunks)} chunks of {batch_size} points each")
    print(f"Memory usage after chunking: {get_memory_usage():.1f} MB")

    # KDE parameters - adjusted to be more robust
    glob_bw = 0.1
    alpha = 0.999

    # Prepare arguments for parallel processing
    chunk_args = [
        (chunk, X, glob_bw, alpha, i, len(chunks)) for i, chunk in enumerate(chunks)
    ]

    # Process chunks in parallel
    z = np.zeros(len(grid_points))
    max_workers = max(1, os.cpu_count() - 1)
    print(f"Using {max_workers} worker processes")
    print(f"Memory usage before parallel processing: {get_memory_usage():.1f} MB")

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_chunk = {
            executor.submit(kde_predict_chunk, chunk_arg): i
            for i, chunk_arg in enumerate(chunk_args)
        }
        print(f"Submitted {len(future_to_chunk)} chunks for processing")

        # Process results as they complete
        completed_chunks = 0
        last_progress_time = time.time()

        # Use as_completed to process results in order of completion
        for future in tqdm(
            concurrent.futures.as_completed(future_to_chunk),
            total=len(future_to_chunk),
            desc="Processing KDE predictions",
        ):
            chunk_idx = future_to_chunk[future]
            try:
                result = future.result()
                # Replace any NaN or infinite values with 0
                result = np.nan_to_num(result, nan=0.0, posinf=0.0, neginf=0.0)
                z[chunk_idx * batch_size : (chunk_idx + 1) * batch_size] = result
                completed_chunks += 1

                # Print progress every 60 seconds
                current_time = time.time()
                if current_time - last_progress_time >= 60:
                    elapsed_time = current_time - start_time
                    chunks_per_second = completed_chunks / elapsed_time
                    estimated_remaining = (
                        len(chunks) - completed_chunks
                    ) / chunks_per_second
                    print(f"\nProgress update at {time.strftime('%H:%M:%S')}:")
                    print(f"Completed {completed_chunks}/{len(chunks)} chunks")
                    print(f"Elapsed time: {elapsed_time:.1f} seconds")
                    print(f"Processing speed: {chunks_per_second:.2f} chunks/second")
                    print(
                        f"Estimated time remaining: {estimated_remaining:.1f} seconds"
                    )
                    print(f"Memory usage: {get_memory_usage():.1f} MB")
                    last_progress_time = current_time

            except Exception as e:
                print(f"Error processing chunk {chunk_idx}: {str(e)}")
                raise

    zz = z.reshape(xx.shape)
    print("\nKDE predictions completed")
    print(f"Memory usage after predictions: {get_memory_usage():.1f} MB")

    x_res, y_res = (
        (x_max - x_min) / (resolution - 1),
        (y_max - y_min) / (resolution - 1),
    )

    transform = Affine.translation(x_min, y_min) * Affine.scale(x_res, y_res)

    raster_filename = f"tmp/{name.lower().replace(' ', '_')}.tif"
    print(f"\nSaving raster to {raster_filename}")

    with rasterio.open(
        raster_filename,
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
    print("Raster file saved successfully")
    print(f"Final memory usage: {get_memory_usage():.1f} MB")

    end_time = time.time()
    print(f"\nTotal processing time: {end_time - start_time:.1f} seconds")

    return raster_filename, X


def apply_kde_to_primary(
    primary_featurelayer: FeatureLayer,
    name: str,
    query: str,
    resolution: int = resolution,
) -> FeatureLayer:
    """
    Applies KDE to the primary feature layer and adds columns for density, z-score,
    percentile, and percentile as a string.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.
        name (str): Name of the KDE feature.
        query (str): SQL query to fetch data for KDE.
        resolution (int): Resolution for the KDE raster grid.

    Returns:
        FeatureLayer: The input feature layer with added KDE-related columns.
    """
    raster_filename, crime_coords = generic_kde(name, query, resolution)

    primary_featurelayer.gdf["centroid"] = primary_featurelayer.gdf.geometry.centroid

    coord_list = [
        (x, y)
        for x, y in zip(
            primary_featurelayer.gdf["centroid"].x,
            primary_featurelayer.gdf["centroid"].y,
        )
    ]

    primary_featurelayer.gdf = primary_featurelayer.gdf.drop(columns=["centroid"])

    with rasterio.open(raster_filename) as src:
        sampled_values = [x[0] for x in src.sample(coord_list)]

    density_column = f"{name.lower().replace(' ', '_')}_density"
    primary_featurelayer.gdf[density_column] = sampled_values

    # Calculate z-scores
    mean_density = primary_featurelayer.gdf[density_column].mean()
    std_density = primary_featurelayer.gdf[density_column].std()
    z_score_column = f"{density_column}_zscore"
    primary_featurelayer.gdf[z_score_column] = (
        primary_featurelayer.gdf[density_column] - mean_density
    ) / std_density

    # Calculate percentiles
    percentile_breaks = list(range(101))
    classifier = mapclassify.Percentiles(
        primary_featurelayer.gdf[density_column], pct=percentile_breaks
    )
    percentile_column = f"{density_column}_percentile"
    primary_featurelayer.gdf[percentile_column] = classifier.yb.astype(float)

    # Assign percentile labels
    label_column = f"{density_column}_label"
    primary_featurelayer.gdf[label_column] = primary_featurelayer.gdf[
        percentile_column
    ].apply(label_percentile)

    print(f"Finished processing {name}")
    return primary_featurelayer


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

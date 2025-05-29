from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Tuple

import mapclassify
import numpy as np
import rasterio
from awkde.awkde import GaussianKDE
<<<<<<< HEAD
from new_etl.classes.file_manager import FileManager, LoadType
from ..classes.featurelayer import FeatureLayer
from config.config import USE_CRS
=======
>>>>>>> staging
from rasterio.transform import Affine
from tqdm import tqdm

from src.config.config import USE_CRS

from ..classes.featurelayer import FeatureLayer

resolution = 1320  # 0.25 miles (in feet, since the CRS is 2272)
batch_size = 100000

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

    feature_layer = FeatureLayer(name=name, carto_sql_queries=query)

    coords = np.array([geom.xy for geom in feature_layer.gdf.geometry])
    x, y = coords[:, 0, :].flatten(), coords[:, 1, :].flatten()
    X = np.column_stack((x, y))

    x_grid, y_grid = (
        np.linspace(x.min(), x.max(), resolution),
        np.linspace(y.min(), y.max(), resolution),
    )
    xx, yy = np.meshgrid(x_grid, y_grid)
    grid_points = np.column_stack((xx.ravel(), yy.ravel()))

    print(f"Fitting KDE for {name} data")
    kde = GaussianKDE(glob_bw=0.1, alpha=0.999, diag_cov=True)
    kde.fit(X)

    print(f"Predicting KDE values for grid of size {grid_points.shape}")

    chunks = [
        grid_points[i : i + batch_size] for i in range(0, len(grid_points), batch_size)
    ]
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

    return raster_file_path, X


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

import numpy as np
import rasterio
from awkde.awkde import GaussianKDE
from ..classes.featurelayer import FeatureLayer
from config.config import USE_CRS
from rasterio.transform import Affine
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed

import mapclassify

resolution = 1320  # 0.25 miles (in feet, bc the CRS is 2272)
batch_size = 100000


def kde_predict_chunk(kde, chunk):
    """Helper function to predict KDE for a chunk of grid points."""
    return kde.predict(chunk)


def generic_kde(name, query, resolution=resolution, batch_size=batch_size):
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

    # Split grid points into chunks
    chunks = [
        grid_points[i : i + batch_size] for i in range(0, len(grid_points), batch_size)
    ]

    # Run predictions in parallel
    z = np.zeros(len(grid_points))  # Placeholder for predicted values

    with ProcessPoolExecutor() as executor:
        # Submit the tasks first, wrapped with tqdm to monitor as they're submitted
        futures = {
            executor.submit(kde_predict_chunk, kde, chunk): i
            for i, chunk in enumerate(tqdm(chunks, desc="Submitting tasks"))
        }

        # Now wrap the as_completed with tqdm for progress tracking
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

    raster_filename = f"tmp/{name.lower().replace(' ', '_')}.tif"
    print(f"Saving raster to {raster_filename}")

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

    return raster_filename, X


def apply_kde_to_primary(primary_featurelayer, name, query, resolution=resolution):
    # Generate KDE and raster file
    raster_filename, crime_coords = generic_kde(name, query, resolution)

    # Add centroid column temporarily
    primary_featurelayer.gdf["centroid"] = primary_featurelayer.gdf.geometry.centroid

    # Create list of (x, y) coordinates for centroids
    coord_list = [
        (x, y)
        for x, y in zip(
            primary_featurelayer.gdf["centroid"].x,
            primary_featurelayer.gdf["centroid"].y,
        )
    ]

    # Remove the temporary centroid column
    primary_featurelayer.gdf = primary_featurelayer.gdf.drop(columns=["centroid"])

    # Open the generated raster file and sample the KDE density values at the centroids
    with rasterio.open(raster_filename) as src:
        sampled_values = [x[0] for x in src.sample(coord_list)]

    # Create a column for the density values
    density_column = f"{name.lower().replace(' ', '_')}_density"
    primary_featurelayer.gdf[density_column] = sampled_values

    # Calculate percentiles using mapclassify.Percentiles
    percentile_breaks = list(range(101))  # Percentile breaks from 0 to 100
    classifier = mapclassify.Percentiles(
        primary_featurelayer.gdf[density_column], pct=percentile_breaks
    )

    # Assign the percentile bins to the density values
    primary_featurelayer.gdf[density_column + "_percentile"] = (
        classifier.yb
    )  # yb gives the bin index

    # Apply percentile labels (e.g., 1st Percentile, 2nd Percentile, etc.)
    primary_featurelayer.gdf[density_column + "_label"] = primary_featurelayer.gdf[
        density_column + "_percentile"
    ].apply(label_percentile)

    # Convert the percentile column to float and drop the density column
    primary_featurelayer.gdf[density_column + "_percentile"] = primary_featurelayer.gdf[
        density_column + "_percentile"
    ].astype(float)

    primary_featurelayer.gdf = primary_featurelayer.gdf.drop(columns=[density_column])

    print(f"Finished processing {name}")
    return primary_featurelayer


def label_percentile(value):
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


from constants.services import GUNCRIME_SQL_QUERY
from config.config import USE_CRS
from classes.featurelayer import FeatureLayer
import numpy as np
import matplotlib.pyplot as plt
from awkde.awkde import GaussianKDE
import rasterio
from rasterio.transform import Affine
import mapclassify


def gun_crimes(primary_featurelayer):
    # Initialize gun_crimes object
    gun_crimes = FeatureLayer(
        name="Gun Crimes", carto_sql_queries=GUNCRIME_SQL_QUERY)

    # Extract x, y coordinates from geometry
    x = np.array([])
    y = np.array([])

    for geom in gun_crimes.gdf.geometry:
        coords = np.array(geom.xy)
        x = np.concatenate([x, coords[0]])
        y = np.concatenate([y, coords[1]])

    # Prepare data for KDE
    X = np.array(list(zip(x, y)))

    # Generate grid for plotting
    x_grid, y_grid = np.linspace(x.min(), x.max(), 1000), np.linspace(
        y.min(), y.max(), 1000
    )
    xx, yy = np.meshgrid(x_grid, y_grid)
    grid_points = np.array([xx.ravel(), yy.ravel()]).T

    # Compute adaptive KDE values
    print("fitting KDE for gun crime data")
    kde = GaussianKDE(glob_bw="silverman", alpha=0.999, diag_cov=True)
    kde.fit(X)

    z = kde.predict(grid_points)
    zz = z.reshape(xx.shape)

    # Calculate resolutions and min values
    x_res = (x.max() - x.min()) / (len(x_grid) - 1)
    y_res = (y.max() - y.min()) / (len(y_grid) - 1)
    min_x, min_y = x.min(), y.min()

    # Save the plot in tmp folder
    plt.pcolormesh(xx, yy, zz)
    plt.scatter(x, y, c="red", s=0.005)
    plt.colorbar()
    plt.savefig("tmp/kde.png")

    # Define the affine transform
    transform = Affine.translation(min_x, min_y) * Affine.scale(x_res, y_res)

    # Export as raster
    with rasterio.open(
        "tmp/output.tif",
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

    primary_featurelayer.gdf["centroid"] = primary_featurelayer.gdf.geometry.centroid

    coord_list = [
        (x, y)
        for x, y in zip(
            primary_featurelayer.gdf["centroid"].x,
            primary_featurelayer.gdf["centroid"].y,
        )
    ]

    primary_featurelayer.gdf = primary_featurelayer.gdf.drop(columns=[
                                                             "centroid"])

    src = rasterio.open("tmp/output.tif")
    sampled_values = [x[0] for x in src.sample(coord_list)]

    primary_featurelayer.gdf["guncrime_density"] = sampled_values

    guncrime_classifier = mapclassify.Percentiles(
        primary_featurelayer.gdf["guncrime_density"], pct=[
            50, 75, 90, 95, 99, 100]
    )
    primary_featurelayer.gdf["guncrime_density"] = primary_featurelayer.gdf[
        "guncrime_density"
    ].apply(guncrime_classifier)
    primary_featurelayer.gdf["guncrime_density"] = primary_featurelayer.gdf[
        "guncrime_density"
    ].astype(float)

    primary_featurelayer.gdf["guncrime_density"] = primary_featurelayer.gdf[
        "guncrime_density"
    ].replace(
        [0, 1, 2, 3, 4, 5],
        ["Bottom 50%", "Top 50%", "Top 25%", "Top 10%", "Top 5%", "Top 1%"],
    )

    return primary_featurelayer

import mapclassify
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from awkde.awkde import GaussianKDE
from classes.featurelayer import FeatureLayer
from config.config import USE_CRS
from constants.services import DRUGCRIME_SQL_QUERY
from rasterio.transform import Affine


def drug_crimes(primary_featurelayer):
    # Initialize gun_crimes object
    drug_crimes = FeatureLayer(
        name="Drug Crimes", carto_sql_queries=DRUGCRIME_SQL_QUERY
    )

    # Extract x, y coordinates from geometry
    x = np.array([])
    y = np.array([])

    for geom in drug_crimes.gdf.geometry:
        coords = np.array(geom.xy)
        x = np.concatenate([x, coords[0]])
        y = np.concatenate([y, coords[1]])

    # Prepare data for KDE
    X = np.array(list(zip(x, y)))

    # Generate grid for plotting
    grid_length = 2500

    x_grid, y_grid = (
        np.linspace(x.min(), x.max(), grid_length),
        np.linspace(y.min(), y.max(), grid_length),
    )
    xx, yy = np.meshgrid(x_grid, y_grid)
    grid_points = np.array([xx.ravel(), yy.ravel()]).T

    # Compute adaptive KDE values
    print("fitting KDE for drug crime data")
    kde = GaussianKDE(glob_bw=0.1, alpha=0.999, diag_cov=True)
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
        "tmp/drug_crimes.tif",
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

    primary_featurelayer.gdf = primary_featurelayer.gdf.drop(columns=["centroid"])

    src = rasterio.open("tmp/drug_crimes.tif")
    sampled_values = [x[0] for x in src.sample(coord_list)]

    primary_featurelayer.gdf["drugcrime_density"] = sampled_values

    percentile_breaks = list(range(101))  # [0, 1, 2, ..., 100]

    drugcrime_classifier = mapclassify.Percentiles(
        primary_featurelayer.gdf["drugcrime_density"], pct=percentile_breaks
    )

    primary_featurelayer.gdf["drugcrime_density_percentile"] = primary_featurelayer.gdf[
        "drugcrime_density"
    ].apply(drugcrime_classifier)

    def label_percentile(value):
        if value == 1:
            return "1st Percentile"
        elif value == 2:
            return "2nd Percentile"
        elif value == 3:
            return "3rd Percentile"
        else:
            return f"{value}th Percentile"

    primary_featurelayer.gdf["drugcrime_density_label"] = primary_featurelayer.gdf[
        "drugcrime_density_percentile"
    ].apply(label_percentile)

    primary_featurelayer.gdf["drugcrime_density_percentile"] = primary_featurelayer.gdf[
        "drugcrime_density_percentile"
    ].astype(float)

    primary_featurelayer.gdf = primary_featurelayer.gdf.drop(
        columns=["drugcrime_density"]
    )

    return primary_featurelayer

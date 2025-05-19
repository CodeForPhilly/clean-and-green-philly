import io

import geopandas as gpd
import requests

from src.classes.featurelayer import FeatureLayer
from src.config.config import USE_CRS
from src.constants.services import PPR_PROPERTIES_TO_LOAD


def ppr_properties(primary_featurelayer):
    fallback_url = "https://opendata.arcgis.com/datasets/d52445160ab14380a673e5849203eb64_0.geojson"

    try:
        ppr_properties = FeatureLayer(
            name="PPR Properties",
            esri_rest_urls=PPR_PROPERTIES_TO_LOAD,
            cols=["PUBLIC_NAME"],
        )

        if ppr_properties.gdf is None or ppr_properties.gdf.empty:
            raise ValueError(
                "PPR properties GeoDataFrame is empty or failed to load from Esri REST URL."
            )

        print("Loaded PPR properties from Esri REST URL.")

    except Exception as e:
        print(f"Error loading PPR properties from Esri REST URL: {e}")
        print("Falling back to loading from GeoJSON URL.")

        response = requests.get(fallback_url)
        response.raise_for_status()
        ppr_properties_gdf = gpd.read_file(io.BytesIO(response.content))

        ppr_properties = FeatureLayer(name="PPR Properties")
        ppr_properties.gdf = ppr_properties_gdf

    ppr_properties.gdf = ppr_properties.gdf[["public_name", "geometry"]]

    ppr_properties.gdf = ppr_properties.gdf.to_crs(USE_CRS)

    primary_featurelayer.spatial_join(ppr_properties)

    mask = primary_featurelayer.gdf["public_name"].notnull()

    count_dropped = mask.sum()
    print(f"Number of PPR properties being dropped: {count_dropped}")

    primary_featurelayer.gdf = primary_featurelayer.gdf.drop(
        primary_featurelayer.gdf[mask].index
    )

    primary_featurelayer.gdf = primary_featurelayer.gdf.drop(columns=["public_name"])

    return primary_featurelayer

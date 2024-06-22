import io
import os
import zipfile

import geopandas as gpd
import requests
from classes.featurelayer import FeatureLayer

from config.config import USE_CRS


def park_priority(primary_featurelayer):
    park_url = 'https://parkserve.tpl.org/downloads/Parkserve_Shapefiles_05212024.zip'
    
    file_name_prefix: str = 'Parkserve'

    target_files = [
        file_name_prefix + '_ParkPriorityAreas.shp',
        file_name_prefix + '_ParkPriorityAreas.dbf',
        file_name_prefix + '_ParkPriorityAreas.shx',
        file_name_prefix + '_ParkPriorityAreas.prj',
        file_name_prefix + '_ParkPriorityAreas.cpg',
        file_name_prefix + '_ParkPriorityAreas.sbn',
        file_name_prefix + '_ParkPriorityAreas.sbx'
    ]

    geojson_path = "tmp/phl_parks.geojson"
    shapefile_exists = all(os.path.exists(os.path.join("tmp", file_name)) for file_name in target_files)

    if not os.path.exists(geojson_path):
        if not shapefile_exists:
            print("Downloading park priority data (slow operation)...")
            park_response = requests.get(park_url)

            with io.BytesIO(park_response.content) as f:
                with zipfile.ZipFile(f, "r") as zip_ref:
                    # Extract only the necessary files
                    for file_name in target_files:
                        zip_ref.extract(file_name, "tmp/")
        else:
            print("Park priority files already exist in /tmp, skipping download.")

        pa_parks = gpd.read_file("tmp/" + file_name_prefix + "_ParkPriorityAreas.shp")
        pa_parks = pa_parks.to_crs(USE_CRS)

        # Filter for Philadelphia County
        phl_parks = pa_parks[pa_parks["ID"].str.startswith("42101")]

        # Select relevant columns - modify as needed once we know the correct column names
        phl_parks = phl_parks[["ParkNeed", "geometry"]]

        phl_parks.rename(columns={"ParkNeed": "park_priority"}, inplace=True)

        # Write the filtered data to GeoJSON
        phl_parks.to_file(geojson_path, driver='GeoJSON')
    else:
        print("GeoJSON file already exists, loading from tmp.")
        phl_parks = gpd.read_file(geojson_path)

    park_priority_layer = FeatureLayer("Park Priority")
    park_priority_layer.gdf = phl_parks

    primary_featurelayer.spatial_join(park_priority_layer)

    return primary_featurelayer
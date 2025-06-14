import os

import geopandas as gpd

from src.config.config import USE_CRS

directory = os.path.dirname(os.path.abspath(__file__))
city_limits_file_path = os.path.join(directory, "city_limits.geojson")
CITY_LIMITS = gpd.read_file(city_limits_file_path)
CITY_LIMITS.to_crs(USE_CRS)
PHL_GEOMETRY = CITY_LIMITS.geometry.iloc[0]

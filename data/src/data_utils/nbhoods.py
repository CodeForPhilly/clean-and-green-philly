import requests
import io
import zipfile
import geopandas as gpd
from classes.featurelayer import FeatureLayer
from config.config import USE_CRS


def nbhoods(primary_featurelayer):
    nbhoods_url = (
        "https://raw.githubusercontent.com/opendataphilly/open-geo-data/master/Neighborhoods_Philadelphia/Neighborhoods_Philadelphia.geojson"
    )

    phl_nbhoods = gpd.read_file(nbhoods_url)
    phl_nbhoods.rename(columns={"mapname": "neighborhood"}, inplace=True)
    phl_nbhoods = phl_nbhoods.to_crs(USE_CRS)
    
    nbhoods = FeatureLayer("Neighborhoods")
    nbhoods.gdf = phl_nbhoods

    primary_featurelayer.spatial_join(nbhoods)

    return primary_featurelayer
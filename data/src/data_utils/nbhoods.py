import geopandas as gpd
from classes.featurelayer import FeatureLayer
from constants.services import NBHOODS_URL

from config.config import USE_CRS


def nbhoods(primary_featurelayer):
    phl_nbhoods = gpd.read_file(NBHOODS_URL)
    
    # Correct the column name to uppercase if needed
    if 'MAPNAME' in phl_nbhoods.columns:
        phl_nbhoods.rename(columns={"MAPNAME": "neighborhood"}, inplace=True)
    
    phl_nbhoods = phl_nbhoods.to_crs(USE_CRS)
    
    nbhoods = FeatureLayer("Neighborhoods")
    nbhoods.gdf = phl_nbhoods
    
    red_cols_to_keep = ["neighborhood", "geometry"]
    nbhoods.gdf = nbhoods.gdf[red_cols_to_keep]
    
    primary_featurelayer.spatial_join(nbhoods)
    
    return primary_featurelayer

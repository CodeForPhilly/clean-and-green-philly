import geopandas as gpd
import jenkspy
import pandas as pd
import requests
from classes.featurelayer import FeatureLayer
from constants.services import CENSUS_BGS_URL, PERMITS_QUERY

from config.config import USE_CRS


def dev_probability(primary_featurelayer):
    census_bgs_gdf = gpd.read_file(CENSUS_BGS_URL)
    census_bgs_gdf = census_bgs_gdf.to_crs(USE_CRS)

    base_url = "https://phl.carto.com/api/v2/sql"
    response = requests.get(f"{base_url}?q={PERMITS_QUERY}&format=GeoJSON")

    if response.status_code == 200:
        try:
            permits_gdf = gpd.GeoDataFrame.from_features(
                response.json(), crs="EPSG:4326"
            )
            print("GeoDataFrame created successfully.")
        except Exception as e:
            print(f"Failed to convert response to GeoDataFrame: {e}")
            return primary_featurelayer
    else:
        truncated_response = response.content[:500]
        print(
            f"Failed to fetch permits data. HTTP status code: {response.status_code}. Response text: {truncated_response}"
        )
        return primary_featurelayer

    permits_gdf = permits_gdf.to_crs(USE_CRS)

    joined_gdf = gpd.sjoin(permits_gdf, census_bgs_gdf, how="inner", predicate="within")

    permit_counts = joined_gdf.groupby("index_right").size()
    census_bgs_gdf["permit_count"] = census_bgs_gdf.index.map(permit_counts)
    census_bgs_gdf["permit_count"] = census_bgs_gdf["permit_count"].fillna(0)

    # Classify development probability using Jenks natural breaks
    breaks = jenkspy.jenks_breaks(census_bgs_gdf["permit_count"], n_classes=3)
    census_bgs_gdf["dev_rank"] = pd.cut(
        census_bgs_gdf["permit_count"], bins=breaks, labels=["Low", "Medium", "High"]
    ).astype(str)

    updated_census_bgs = FeatureLayer(
        name="Updated Census Block Groups",
        gdf=census_bgs_gdf[["permit_count", "dev_rank", "geometry"]],
        use_wkb_geom_field="geometry",
        cols=["permit_count", "dev_rank"],
    )

    updated_census_bgs.gdf = updated_census_bgs.gdf.to_crs(USE_CRS)

    primary_featurelayer.spatial_join(updated_census_bgs)

    return primary_featurelayer

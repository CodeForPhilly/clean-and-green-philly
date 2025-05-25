import os
from typing import List
import geopandas as gpd
import pandas as pd
from esridump.dumper import EsriDumper
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from shapely import wkb

from config.config import USE_CRS


# Esri data loader
def load_esri_data(esri_rest_urls: List[str], input_crs: str):
    """
    Load data from Esri REST URLs and add a parcel_type column based on the URL.

    Args:
        esri_rest_urls (list[str]): List of Esri REST URLs to fetch data from.
        input_crs (str): CRS of the source data.
    Returns:
        GeoDataFrame: Combined GeoDataFrame with data from all URLs.
    """
    gdfs = []
    for url in esri_rest_urls:
        # Determine parcel_type based on URL patterns
        parcel_type = (
            "Land"
            if "Vacant_Indicators_Land" in url
            else "Building"
            if "Vacant_Indicators_Bldg" in url
            else None
        )

        dumper = EsriDumper(url)
        features = [feature for feature in dumper]

        if not features:
            continue  # Skip if no features were found

        geojson_features = {"type": "FeatureCollection", "features": features}
        gdf = gpd.GeoDataFrame.from_features(geojson_features, crs=input_crs).to_crs(
            USE_CRS
        )

        if parcel_type:
            gdf["parcel_type"] = parcel_type  # Add the parcel_type column

        gdfs.append(gdf)

    return pd.concat(gdfs, ignore_index=True)


# Carto data loader
def load_carto_data(
    queries: List[str],
    input_crs: str,
    wkb_geom_field: str | None = "the_geom",
    max_workers: int = os.cpu_count(),
    chunk_size: int = 100000,
):
    gdfs = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for query in queries:
            total_rows = get_carto_total_rows(query)
            for offset in range(0, total_rows, chunk_size):
                futures.append(
                    executor.submit(
                        fetch_carto_chunk,
                        query,
                        offset,
                        input_crs,
                        wkb_geom_field,
                        chunk_size,
                    )
                )
        for future in tqdm(
            as_completed(futures), total=len(futures), desc="Processing Carto chunks"
        ):
            gdfs.append(future.result())
    return pd.concat(gdfs, ignore_index=True)


def fetch_carto_chunk(
    query: str,
    offset: int,
    input_crs: str,
    wkb_geom_field: str | None = "the_geom",
    chunk_size: int = 100000,
):
    chunk_query = f"{query} LIMIT {chunk_size} OFFSET {offset}"
    response = requests.get(
        "https://phl.carto.com/api/v2/sql", params={"q": chunk_query}
    )
    response.raise_for_status()
    data = response.json().get("rows", [])
    if not data:
        return gpd.GeoDataFrame()
    df = pd.DataFrame(data)
    geometry = (
        wkb.loads(df[wkb_geom_field], hex=True)
        if wkb_geom_field
        else gpd.points_from_xy(df.x, df.y)
    )
    return gpd.GeoDataFrame(df, geometry=geometry, crs=input_crs).to_crs(USE_CRS)


def get_carto_total_rows(query):
    count_query = f"SELECT COUNT(*) as count FROM ({query}) as subquery"
    response = requests.get(
        "https://phl.carto.com/api/v2/sql", params={"q": count_query}
    )
    response.raise_for_status()
    return response.json()["rows"][0]["count"]

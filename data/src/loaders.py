import geopandas as gpd
import pandas as pd
from esridump.dumper import EsriDumper
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from shapely import wkb


# Esri data loader
def load_esri_data(esri_rest_urls, input_crs, target_crs):
    """
    Load data from Esri REST URLs and add a parcel_type column based on the URL.

    Args:
        esri_rest_urls (list[str]): List of Esri REST URLs to fetch data from.
        input_crs (str): CRS of the source data.
        target_crs (str): Target CRS to which data should be reprojected.

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
            target_crs
        )

        if parcel_type:
            gdf["parcel_type"] = parcel_type  # Add the parcel_type column

        gdfs.append(gdf)

    return pd.concat(gdfs, ignore_index=True)


# Carto data loader
def load_carto_data(
    queries, max_workers, chunk_size, use_wkb_geom_field, input_crs, target_crs
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
                        chunk_size,
                        use_wkb_geom_field,
                        input_crs,
                        target_crs,
                    )
                )
        for future in tqdm(
            as_completed(futures), total=len(futures), desc="Processing Carto chunks"
        ):
            gdfs.append(future.result())
    return pd.concat(gdfs, ignore_index=True)


def fetch_carto_chunk(
    query, offset, chunk_size, use_wkb_geom_field, input_crs, target_crs
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
        wkb.loads(df[use_wkb_geom_field], hex=True)
        if use_wkb_geom_field
        else gpd.points_from_xy(df.x, df.y)
    )
    return gpd.GeoDataFrame(df, geometry=geometry, crs=input_crs).to_crs(target_crs)


def get_carto_total_rows(query):
    count_query = f"SELECT COUNT(*) as count FROM ({query}) as subquery"
    response = requests.get(
        "https://phl.carto.com/api/v2/sql", params={"q": count_query}
    )
    response.raise_for_status()
    return response.json()["rows"][0]["count"]

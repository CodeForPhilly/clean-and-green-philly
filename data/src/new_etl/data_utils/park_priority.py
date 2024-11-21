import os
import zipfile
from io import BytesIO
from typing import List, Union

import geopandas as gpd
import requests
from bs4 import BeautifulSoup
from ..classes.featurelayer import FeatureLayer
from config.config import USE_CRS
from tqdm import tqdm
import pyogrio


def get_latest_shapefile_url() -> str:
    """
    Scrapes the TPL website to get the URL of the latest shapefile.

    Returns:
        str: The URL of the latest shapefile.

    Raises:
        ValueError: If the shapefile link is not found on the page.
    """
    url: str = "https://www.tpl.org/park-data-downloads"
    response: requests.Response = requests.get(url)
    soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")

    shapefile_link: Union[BeautifulSoup, None] = soup.find("a", string="Shapefile")
    if shapefile_link:
        return str(shapefile_link["href"])
    else:
        raise ValueError("Shapefile link not found on the page")


def download_and_process_shapefile(
    geojson_path: str, park_url: str, target_files: List[str], file_name_prefix: str
) -> gpd.GeoDataFrame:
    """
    Downloads and processes the shapefile to create a GeoDataFrame for Philadelphia parks.

    Args:
        geojson_path (str): Path to save the GeoJSON file.
        park_url (str): URL to download the shapefile.
        target_files (List[str]): List of files to extract from the shapefile.
        file_name_prefix (str): Prefix for the file names to be extracted.

    Returns:
        gpd.GeoDataFrame: GeoDataFrame containing the processed park data.
    """
    print("Downloading and processing park priority data...")
    response: requests.Response = requests.get(park_url, stream=True)
    total_size: int = int(response.headers.get("content-length", 0))

    with tqdm(
        total=total_size, unit="iB", unit_scale=True, desc="Downloading"
    ) as progress_bar:
        buffer: BytesIO = BytesIO()
        for data in response.iter_content(1024):
            size: int = buffer.write(data)
            progress_bar.update(size)

    with zipfile.ZipFile(buffer) as zip_ref:
        for file_name in tqdm(target_files, desc="Extracting"):
            zip_ref.extract(file_name, "tmp/")

    print("Processing shapefile...")
    pa_parks: gpd.GeoDataFrame = gpd.read_file(
        "tmp/" + file_name_prefix + "_ParkPriorityAreas.shp"
    )
    pa_parks = pa_parks.to_crs(USE_CRS)

    phl_parks: gpd.GeoDataFrame = pa_parks[pa_parks["ID"].str.startswith("42101")]
    phl_parks = phl_parks.loc[:, ["ParkNeed", "geometry"]]

    if isinstance(phl_parks, gpd.GeoDataFrame):
        phl_parks.rename(columns={"ParkNeed": "park_priority"}, inplace=True)
    else:
        raise TypeError("Expected a GeoDataFrame, got Series or another type instead")

    print(f"Writing filtered data to GeoJSON: {geojson_path}")
    phl_parks.to_file(geojson_path, driver="GeoJSON")

    return phl_parks


def park_priority(primary_featurelayer: FeatureLayer) -> FeatureLayer:
    """
    Downloads and processes park priority data, then joins it with the primary feature layer.

    Args:
        primary_featurelayer (FeatureLayer): The primary feature layer to join with park priority data.

    Returns:
        FeatureLayer: The primary feature layer with park priority data joined.
    """
    park_url: str = get_latest_shapefile_url()
    print(f"Downloading park priority data from: {park_url}")

    file_name_prefix: str = "Parkserve"
    target_files: List[str] = [
        file_name_prefix + "_ParkPriorityAreas.shp",
        file_name_prefix + "_ParkPriorityAreas.dbf",
        file_name_prefix + "_ParkPriorityAreas.shx",
        file_name_prefix + "_ParkPriorityAreas.prj",
        file_name_prefix + "_ParkPriorityAreas.CPG",
        file_name_prefix + "_ParkPriorityAreas.sbn",
        file_name_prefix + "_ParkPriorityAreas.sbx",
    ]
    geojson_path: str = "tmp/phl_parks.geojson"

    os.makedirs("tmp/", exist_ok=True)

    try:
        if os.path.exists(geojson_path):
            print(f"GeoJSON file already exists, loading from {geojson_path}")
            phl_parks: gpd.GeoDataFrame = gpd.read_file(geojson_path)
        else:
            raise pyogrio.errors.DataSourceError(
                "GeoJSON file missing, forcing download."
            )

    except (pyogrio.errors.DataSourceError, ValueError) as e:
        print(f"Error loading GeoJSON: {e}. Re-downloading and processing shapefile.")
        if os.path.exists(geojson_path):
            os.remove(geojson_path)  # Delete the corrupted GeoJSON if it exists
        phl_parks = download_and_process_shapefile(
            geojson_path, park_url, target_files, file_name_prefix
        )

    park_priority_layer: FeatureLayer = FeatureLayer("Park Priority")
    park_priority_layer.gdf = phl_parks

    primary_featurelayer.spatial_join(park_priority_layer)
    return primary_featurelayer

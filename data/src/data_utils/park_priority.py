import os
import re
from io import BytesIO
from typing import List, Union

import fiona
import geopandas as gpd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from src.config.config import USE_CRS

from ..classes.file_manager import FileManager, FileType, LoadType
from ..metadata.metadata_utils import provide_metadata
from ..utilities import spatial_join

file_manager = FileManager()


def get_latest_shapefile_url() -> str:
    """
    Scrapes the TPL website to get the URL of the latest shapefile.

    Returns:from ..classes.featurelayer import FeatureLayer

        str: The URL of the latest shapefile.

    Raises:
        ValueError: If the shapefile link is not found on the page.
    """
    url: str = "https://www.tpl.org/park-data-downloads"
    response: requests.Response = requests.get(url)
    soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")
    shapefile_link: Union[BeautifulSoup, None] = soup.find(
        "a", string=re.compile(r"Shapefile")
    )
    if shapefile_link:
        return str(shapefile_link["href"])
    else:
        raise ValueError("Shapefile link not found on the page")


def download_and_process_shapefile(
    geojson_filename: str, park_url: str, target_files: List[str], file_name_prefix: str
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
    target_files_paths = [
        file_manager.get_file_path(filename, LoadType.TEMP) for filename in target_files
    ]
    if any([not os.path.exists(file_path) for file_path in target_files_paths]):
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

        print("Extracting files from the downloaded zip...")
        file_manager.extract_files(buffer, target_files)

    else:
        print("Parks data already located in filesystem - proceeding")

    print("Processing shapefile...")

    def filter_shapefile_generator():
        file_path = file_manager.get_file_path(
            file_name_prefix + "_ParkPriorityAreas.shp", LoadType.TEMP
        )

        with fiona.open(file_path) as source:
            for feature in source:
                if not feature["properties"]["ID"].startswith("42101"):
                    continue
                filtered_feature = feature
                filtered_feature["properties"] = {
                    column: value
                    for column, value in feature["properties"].items()
                    if column in ["ParkNeed"]
                }
                yield filtered_feature

    phl_parks: gpd.GeoDataFrame = gpd.GeoDataFrame.from_features(
        filter_shapefile_generator()
    )

    # ISSUE Check this CRS
    phl_parks.crs = USE_CRS
    phl_parks = phl_parks.to_crs(USE_CRS)

    if isinstance(phl_parks, gpd.GeoDataFrame):
        phl_parks.rename(columns={"ParkNeed": "park_priority"}, inplace=True)
    else:
        raise TypeError("Expected a GeoDataFrame, got Series or another type instead")

    print(f"Writing filtered data to GeoJSON: {geojson_filename}")
    file_manager.save_gdf(phl_parks, geojson_filename, LoadType.TEMP, FileType.GEOJSON)

    return phl_parks


@provide_metadata()
def park_priority(input_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Downloads and processes park priority data, then joins it with the primary feature layer.

    Args:
        primary_featurelayer (FeatureLayer): The primary feature layer to join with park priority data.

    Returns:
        FeatureLayer: The primary feature layer with park priority data joined.

    Tagline:
        Labels high-priority park areas.

    Columns Added:
        park_priority (int): The park priority score.

    Primary Feature Layer Columns Referenced:
        opa_id, geometry

    Source:
        https://www.tpl.org/park-data-downloads
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
    geojson_filename = "phl_parks"

    try:
        phl_parks = file_manager.load_gdf(
            geojson_filename, FileType.GEOJSON, LoadType.TEMP
        )
    except FileNotFoundError as e:
        print(f"Error loading GeoJSON: {e}. Re-downloading and processing shapefile.")
        phl_parks = download_and_process_shapefile(
            geojson_filename, park_url, target_files, file_name_prefix
        )

    merged_gdf = spatial_join(input_gdf, phl_parks)
    return merged_gdf

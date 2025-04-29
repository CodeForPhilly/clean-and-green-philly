import os
from enum import Enum
from io import BytesIO
from typing import List
import zipfile

import geopandas as gpd
from tqdm import tqdm

from config.config import ROOT_DIRECTORY


class LoadType(Enum):
    TEMP = "temp"
    CACHE = "cache"


class FileManager:
    """
    A manager for interacting with cached files or temporary files loaded from or extracting into the local filesystem.
    """

    def __init__(self):
        """
        Initialize the FileManager with paths for the temporary and cache directories at the root directory of the project.
        """
        self.temp_directory = os.path.join(ROOT_DIRECTORY, "tmp")
        self.cache_directory = os.path.join(ROOT_DIRECTORY, "cache")

        if not os.path.exists(self.temp_directory):
            os.makedirs(self.temp_directory)
        if not os.path.exists(self.cache_directory):
            os.makedirs(self.cache_directory)

    def get_file_path(self, file_name: str, load_type: LoadType) -> str:
        """
        Get the full file path for a given file depending on whether it belongs in the temporary or cache directory.

        Args:
            file_name (str): The name of the file.
            load_type (LoadType): The destination type of the file (TEMP or CACHE).
        """
        parent_directory = (
            self.temp_directory if load_type == LoadType.TEMP else self.cache_directory
        )
        return os.path.join(parent_directory, file_name)

    def load_gdf(self, file_name: str, load_type: LoadType) -> gpd.GeoDataFrame:
        """
        Loads a GeoDataFrame into memory from a local file in the temporary or cache directory.

        Args:
            file_name (str): The name of the file.
            load_type (LoadType): The destination type of the file (TEMP or CACHE).
        """
        file_path = self.get_file_path(file_name, load_type)
        if os.path.exists(file_path):
            return gpd.read_file(file_path)
        else:
            raise FileNotFoundError(
                f"File {file_name} not found in corresponding directory."
            )

    def save_gdf(
        self, gdf: gpd.GeoDataFrame, file_name: str, load_type: LoadType
    ) -> None:
        """
        Saves a GeoDataFrame to a local file in the temporary or cache directory.

        Args:
            gdf (gpd.GeoDataFrame): The GeoDataFrame to save.
            file_name (str): The name of the file.
            load_type (LoadType): The destination type of the file (TEMP or CACHE).
        """
        file_path = self.get_file_path(file_name, load_type)
        gdf.to_file(file_path, driver="GeoJSON")

    def extract_files(self, buffer: BytesIO, filenames: List[str]) -> None:
        """
        Extracts files stored in a zip buffer to the local temp directory. Because cache is intended only for finalized
        geoparquet files that contain the cleaned, final data, we store all intermediate extracted files in the temp directory
        by default.

        Args:
            buffer (BytesIO): The zip file buffer containing all of the files to extract.
            filenames (List[str]): A list of the filenames to be extracted from the zip file.
        """
        destination = self.temp_directory
        with zipfile.ZipFile(buffer) as zip_ref:
            for filename in tqdm(filenames, desc="Extracting"):
                zip_ref.extract(filename, destination)

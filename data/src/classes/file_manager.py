import glob
import os
import time
import zipfile
from datetime import datetime
from enum import Enum
from io import BytesIO
from typing import List

import geopandas as gpd
from tqdm import tqdm

from src.config.config import CACHE_FRACTION, ROOT_DIRECTORY

print(f"Root directory is {ROOT_DIRECTORY}")


class LoadType(Enum):
    TEMP = "temp"
    SOURCE_CACHE = "source_cache"
    PIPELINE_CACHE = "pipeline_cache"


class FileType(Enum):
    GEOJSON = "geojson"
    PARQUET = "parquet"
    PMTILES = "pmtiles"
    CSV = "csv"


class FileManager:
    """
    A manager for interacting with cached files or temporary files loaded from or extracting into the local filesystem.
    """

    _instance = None

    def __init__(self, fraction=CACHE_FRACTION):
        """
        Initialize the FileManager with paths for the temporary and cache directories at the root directory of the project.
        """
        if FileManager._instance is not None:
            return FileManager._instance

        self.storage_directory = os.path.join(ROOT_DIRECTORY, "storage")

        if not os.path.exists(self.storage_directory):
            os.makedirs(self.storage_directory)

        self.fraction = fraction
        self.temp_directory = os.path.join(self.storage_directory, "temp")
        self.source_cache_directory = os.path.join(
            self.storage_directory, "source_cache"
        )
        self.pipeline_cache_directory = os.path.join(
            self.storage_directory, "pipeline_cache"
        )

        if not os.path.exists(self.temp_directory):
            os.makedirs(self.temp_directory)
        if not os.path.exists(self.source_cache_directory):
            os.makedirs(self.source_cache_directory)
        if not os.path.exists(self.pipeline_cache_directory):
            os.makedirs(self.pipeline_cache_directory)

    def generate_file_label(self, table_name: str) -> str:
        """
        Generates a file label for a given table name to cache parquet files according to format
        <table_name>_<date>_<(old | new)>.parquet according whether it was generated from the new or old pipeline (use just new for now).
        Args:
            table_name (str): The name of the table.
        Returns:
            str: The generated file label.
        """
        date = datetime.now().strftime("%Y_%m_%d")
        return f"{table_name}_{date}_new"

    def get_file_path(
        self, file_name: str, load_type: LoadType, file_type: FileType | None = None
    ) -> str:
        """
        Get the full file path for a given file depending on whether it belongs in the temporary or cache directory.

        Args:
            file_name (str): The name of the file.
            file_type (FileType): The type of the file (GEOJSON or PARQUET).
            load_type (LoadType): The destination type of the file (TEMP or CACHE).
        """
        parent_directory = (
            self.temp_directory
            if load_type == LoadType.TEMP
            else self.source_cache_directory
            if load_type == LoadType.SOURCE_CACHE
            else self.pipeline_cache_directory
        )
        file_name = f"{file_name}.{file_type.value}" if file_type else file_name
        return os.path.join(parent_directory, file_name)

    def check_file_exists(
        self, file_name: str, load_type: LoadType, file_type: FileType | None = None
    ) -> bool:
        """
        Checks if a file exists in the temporary or cache directory.
        Args:
            file_name (str): The name of the file.
            load_type (LoadType): The destination type of the file (TEMP or CACHE).
        Returns:
            bool: True if the file exists, False otherwise.
        """
        file_path = self.get_file_path(file_name, load_type, file_type)
        return os.path.exists(file_path)

    def check_source_cache_file_exists(
        self, table_name: str, load_type: LoadType
    ) -> bool:
        """
        Checks for the existence of a file matching the given tablename in the caching directories -
        either a source file for the data or an intermediate step in the pipeline.
        Args:
            table_name (str): The name of the table of source data.
            load_type (LoadType): The destination type of the file (either SOURCE_CACHE or PIPELINE_CACHE).
        """
        start_time = time.time()
        print(
            f"    FileManager.check_source_cache_file_exists: Checking for {table_name}"
        )

        directory = (
            self.source_cache_directory
            if load_type == LoadType.SOURCE_CACHE
            else self.pipeline_cache_directory
        )
        # Use glob pattern matching for more efficient file searching
        pattern = os.path.join(directory, f"*{table_name}*.parquet")

        glob_start = time.time()
        files = glob.glob(pattern)
        glob_time = time.time() - glob_start

        result = len(files) > 0
        total_time = time.time() - start_time

        print(
            f"    FileManager.check_source_cache_file_exists: Found {len(files)} files in {glob_time:.2f}s (total: {total_time:.2f}s)"
        )
        return result

    def get_most_recent_cache(self, table_name: str) -> gpd.GeoDataFrame | None:
        """
        Returns the most recently generated file in the cache directory for a given table name.
        Args:
            table_name (str): The name of the table.
        Returns:
            GeoDataFrame: The dataframe loaded from the most recent cached file.
            None: If no files exist for the given table name.
        """
        start_time = time.time()
        print(
            f"    FileManager.get_most_recent_cache: Loading most recent cache for {table_name}"
        )

        # Use glob pattern matching for more efficient file searching
        pattern = os.path.join(self.source_cache_directory, f"*{table_name}*.parquet")

        glob_start = time.time()
        cached_files = glob.glob(pattern)
        glob_time = time.time() - glob_start

        if not cached_files:
            print("    FileManager.get_most_recent_cache: No cached files found")
            return None

        # Get the most recent file by modification time
        mtime_start = time.time()
        most_recent_file = max(cached_files, key=os.path.getmtime)
        mtime_time = time.time() - mtime_start

        print(
            f"    FileManager.get_most_recent_cache: Found {len(cached_files)} files, most recent: {os.path.basename(most_recent_file)}"
        )
        print(
            f"    FileManager.get_most_recent_cache: Glob took {glob_time:.2f}s, mtime check took {mtime_time:.2f}s"
        )

        # Load the parquet file
        load_start = time.time()
        gdf = gpd.read_parquet(most_recent_file)
        load_time = time.time() - load_start

        total_time = time.time() - start_time
        print(
            f"    FileManager.get_most_recent_cache: Parquet load took {load_time:.2f}s (total: {total_time:.2f}s)"
        )

        return gdf

    def load_gdf(
        self, file_name: str, load_type: LoadType, file_type: FileType | None = None
    ) -> gpd.GeoDataFrame:
        """
        Loads a GeoDataFrame into memory from a local file in the temporary or cache directory.

        Args:
            file_name (str): The name of the file.
            file_type (FileType): The type of the file (GEOJSON or PARQUET).
            load_type (LoadType): The destination type of the file (TEMP or CACHE).
        """
        file_path = self.get_file_path(file_name, load_type, file_type)
        if os.path.exists(file_path):
            gdf = (
                gpd.read_parquet(file_path)
                if file_type == FileType.PARQUET
                else gpd.read_file(file_path)
            )
            return gdf
        else:
            raise FileNotFoundError(
                f"File {file_name} not found in corresponding directory."
            )

    def save_gdf(
        self,
        gdf: gpd.GeoDataFrame,
        file_name: str,
        load_type: LoadType,
        file_type: FileType | None = None,
    ) -> None:
        """
        Saves a GeoDataFrame to a local file in the temporary or cache directory.

        Args:
            gdf (gpd.GeoDataFrame): The GeoDataFrame to save.
            file_name (str): The name of the file.
            file_type (FileType): The type of the file (GEOJSON or PARQUET).
            load_type (LoadType): The destination type of the file (TEMP or CACHE).
        """
        start_time = time.time()
        print(f"    FileManager.save_gdf: Starting save for {file_name}")

        file_path = self.get_file_path(file_name, load_type, file_type)
        print(f"    FileManager.save_gdf: Target path: {file_path}")

        if file_type == FileType.PARQUET:
            print(
                f"    FileManager.save_gdf: Writing parquet file ({len(gdf)} rows, {len(gdf.columns)} columns)"
            )
            parquet_start = time.time()
            gdf.to_parquet(file_path, index=False)
            parquet_time = time.time() - parquet_start
            print(f"    FileManager.save_gdf: Parquet write took {parquet_time:.2f}s")
        elif file_type == FileType.GEOJSON:
            print("    FileManager.save_gdf: Writing GeoJSON file")
            geojson_start = time.time()
            gdf.to_file(file_path, driver="GeoJSON")
            geojson_time = time.time() - geojson_start
            print(f"    FileManager.save_gdf: GeoJSON write took {geojson_time:.2f}s")
        elif file_type == FileType.CSV:
            print("    FileManager.save_gdf: Writing CSV file")
            csv_start = time.time()
            gdf.to_csv(file_path)
            csv_time = time.time() - csv_start
            print(f"    FileManager.save_gdf: CSV write took {csv_time:.2f}s")
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        total_time = time.time() - start_time
        print(f"    FileManager.save_gdf: Total save operation took {total_time:.2f}s")

    def save_fractional_gdf(
        self,
        gdf: gpd.GeoDataFrame,
        file_name: str,
        load_type: LoadType,
    ) -> None:
        """
        Saves a portion of a supplied GeoDataFrame to a local file in the temporary or cache directory based on a deterministic selection of some of the rows.

        Args:
            gdf (gpd.GeoDataFrame): The GeoDataFrame to save.
            file_name (str): The name of the file.
            load_type (LoadType): The destination type of the file (TEMP or CACHE).

        This will always be used for a parquet file in our used case, so no need to pass in file_type.
        """

        num_rows = len(gdf)
        num_rows_to_save = int(num_rows * self.fraction)
        reduced_gdf = gdf.iloc[:: num_rows // num_rows_to_save]
        file_path = self.get_file_path(file_name, load_type, FileType.PARQUET)

        reduced_gdf.to_parquet(file_path, index=False)

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

    def extract_all(self, buffer: BytesIO) -> None:
        """
        Extract everything in a buffer to the local temp directory.

        Args:
            buffer (BytesIO): The zip file buffer containing all of the data to extract.
        """
        destination = self.temp_directory
        with zipfile.ZipFile(buffer) as zip_ref:
            zip_ref.extractall(destination)

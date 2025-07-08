import os
from io import BytesIO
from typing import Tuple

import geopandas as gpd
import pandas as pd

from src.config.config import ROOT_DIRECTORY
from src.metadata.metadata_utils import current_metadata, provide_metadata
from src.validation.base import ValidationResult, validate_output
from src.validation.vacant_properties import VacantPropertiesOutputValidator

from ..classes.loaders import EsriLoader, google_cloud_bucket
from ..constants.services import VACANT_PROPS_LAYERS_TO_LOAD


def load_backup_data_from_local(file_path: str, parcel_type: str) -> pd.DataFrame:
    """
    Loads backup data from local geoparquet file as a DataFrame, ensuring compatibility for matching.

    Args:
        file_path (str): The path to the local geoparquet file.
        parcel_type (str): The type of parcel ("Buildings" or "Land") to assign to the data.

    Returns:
        pd.DataFrame: A DataFrame containing the backup data with only the "opa_id" column.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Backup file {file_path} not found.")

    try:
        gdf = gpd.read_parquet(file_path)
    except Exception as e:
        raise ValueError(f"Error reading geoparquet file: {e}")

    print(f"Loaded backup {parcel_type.lower()} data from local file: {file_path}")

    # Ensure only opa_id is retained and convert to DataFrame (drop geometry)
    gdf = gdf[["opa_id"]]
    gdf = gdf.drop(columns=["geometry"], errors="ignore")

    # Add parcel_type column
    gdf["parcel_type"] = parcel_type

    return gdf


def load_backup_data_from_gcs(file_name: str) -> pd.DataFrame | None:
    """
    Loads backup data from Google Cloud Storage as a DataFrame, ensuring compatibility for matching.

    Args:
        file_name (str): The name of the file to load from GCS.

    Returns:
        pd.DataFrame: A DataFrame containing the backup data with only the "opa_id" column.
    """
    bucket = google_cloud_bucket()
    if not bucket:
        print("No Google Cloud bucket available - skipping backup data load.")
        raise ValueError("Missing Google cloud bucket to load backup data")
    blob = bucket.blob(file_name)
    if not blob.exists():
        raise FileNotFoundError(f"File {file_name} not found in the GCS bucket.")
    file_bytes = blob.download_as_bytes()
    try:
        gdf = gpd.read_file(BytesIO(file_bytes))
    except Exception as e:
        raise ValueError(f"Error reading GeoJSON file: {e}")

    print("Loaded backup data from GCS.")

    # Ensure only opa_id is retained and convert to DataFrame (drop geometry)
    gdf = gdf[["OPA_ID"]].rename(columns={"OPA_ID": "opa_id"})
    gdf = gdf.drop(columns=["geometry"], errors="ignore")

    return gdf


def check_null_percentage(df: pd.DataFrame, threshold: float = 0.05) -> None:
    """
    Checks if any column in the DataFrame has more than the given threshold of null values.

    Args:
        df (pd.DataFrame): The DataFrame to check for null percentages.
        threshold (float): The threshold for acceptable null percentages (default is 5%).

    Raises:
        ValueError: If any column has more null values than the threshold.
    """
    null_percentages = df.isnull().mean()
    for col, pct in null_percentages.items():
        if pct > threshold:
            raise ValueError(
                f"Column '{col}' has more than {threshold * 100}% null values ({pct * 100}%)."
            )


@validate_output(VacantPropertiesOutputValidator)
@provide_metadata(current_metadata=current_metadata)
def vacant_properties(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Adds a "vacant" column to the input GeoDataFrame based on vacant property data from
    ESRI layers and backup data from local geoparquet files if necessary.

    Args:
        input_gdf (GeoDataFrame): The GeoDataFrame containing property data.

    Returns:
        GeoDataFrame: The input GeoDataFrame with an added "vacant" column.

    Tagline:
        Identify vacant properties.

    Columns Added:
        vacant (bool): Indicates whether the property is vacant.

    Columns referenced:
        opa_id

    Known Issues:
        - The vacant land data is below the threshold, so backup data is loaded from local files.
        - The vacant buildings data is below the threshold, so backup data is loaded from local files.
    """
    loader = EsriLoader(
        name="Vacant Properties",
        esri_urls=VACANT_PROPS_LAYERS_TO_LOAD,
        cols=["opa_id", "parcel_type"],
    )

    vacant_properties, input_validation = loader.load_or_fetch()

    # Filter for different property types in the dataset
    vacant_buildings_gdf = vacant_properties[
        vacant_properties["parcel_type"] == "Buildings"
    ]
    vacant_land_gdf = vacant_properties[vacant_properties["parcel_type"] == "Land"]

    print(
        f"Vacant buildings data size in the default dataset: {len(vacant_buildings_gdf)} rows."
    )
    print(f"Vacant land data size in the default dataset: {len(vacant_land_gdf)} rows.")

    # Check if the vacant buildings data is below the threshold
    if len(vacant_buildings_gdf) < 9000:
        print(
            "Vacant buildings data is below the threshold. Removing vacant buildings rows and loading backup data from local files."
        )
        vacant_properties = vacant_properties[
            vacant_properties["parcel_type"] != "Buildings"
        ]

        # Attempt to load backup buildings data from local files
        try:
            backup_buildings_gdf = load_backup_data_from_local(
                ROOT_DIRECTORY / "../backup_data/buildings_backup_2024_06_24.parquet",
                "Buildings",
            )

            # Append backup data to the existing dataset
            print(
                f"Appending backup buildings data ({len(backup_buildings_gdf)} rows) to the existing data."
            )

            vacant_properties = pd.concat(
                [vacant_properties, backup_buildings_gdf], ignore_index=True
            )
        except Exception as e:
            print(
                f"Unable to load backup buildings data with error {e} - proceeding with pipeline using only available buildings data"
            )

    # Check if the vacant land data is below the threshold
    if len(vacant_land_gdf) < 20000:
        print(
            "Vacant land data is below the threshold. Removing vacant land rows and loading backup data from local files."
        )
        vacant_properties = vacant_properties[
            vacant_properties["parcel_type"] != "Land"
        ]

        # Attempt to load backup land data from local files
        try:
            backup_land_gdf = load_backup_data_from_local(
                ROOT_DIRECTORY / "../backup_data/land_backup_2024_06_24.parquet",
                "Land",
            )

            # Append backup data to the existing dataset
            print(
                f"Appending backup land data ({len(backup_land_gdf)} rows) to the existing data."
            )

            vacant_properties = pd.concat(
                [vacant_properties, backup_land_gdf], ignore_index=True
            )
        except Exception as e:
            print(
                f"Unable to load backup land data with error {e} - proceeding with pipeline using only available land data"
            )

    # Convert to a regular DataFrame by dropping geometry
    df = vacant_properties.drop(columns=["geometry"], errors="ignore")

    # Drop rows with missing opa_id
    df.dropna(subset=["opa_id"], inplace=True)

    # Final check for null percentages
    check_null_percentage(df)

    # Add "vacant" column to input GeoDataFrame
    input_gdf["vacant"] = input_gdf["opa_id"].isin(df["opa_id"])

    # Drop parcel_type column after processing
    df.drop(columns=["parcel_type"], inplace=True)

    return input_gdf, input_validation

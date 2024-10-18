from classes.featurelayer import FeatureLayer, google_cloud_bucket
from constants.services import VACANT_PROPS_LAYERS_TO_LOAD
import geopandas as gpd

from io import BytesIO

import pandas as pd


def load_backup_data_from_gcs(file_name: str) -> gpd.GeoDataFrame:
    """
    Load backup data from Google Cloud Storage (GCS) and return it as a GeoDataFrame.

    Args:
        file_name (str): The name of the file in GCS to load.

    Returns:
        gpd.GeoDataFrame: The loaded GeoDataFrame from the backup.
    """
    # Get the bucket using the google_cloud_bucket function
    bucket = google_cloud_bucket()

    # Ensure the file name is correctly passed to the blob
    blob = bucket.blob(file_name)
    if not blob.exists():
        raise FileNotFoundError(f"File {file_name} not found in the GCS bucket.")

    # Download the file from GCS
    file_bytes = blob.download_as_bytes()

    # Load the contents into a GeoDataFrame
    gdf = gpd.read_file(BytesIO(file_bytes))
    print(f"Loaded backup data from GCS: {len(gdf)} rows.")

    # Rename the backup data columns to match the original dataset's format
    gdf = gdf.rename(
        columns={
            "ADDRESS": "address",
            "OWNER1": "owner_1",
            "OWNER2": "owner_2",
            "BLDG_DESC": "building_description",
            "CouncilDistrict": "council_district",
            "ZoningBaseDistrict": "zoning_base_district",
            "ZipCode": "zipcode",
            "OPA_ID": "opa_id",
        }
    )

    return gdf


def vacant_properties() -> FeatureLayer:
    """
    Load vacant properties data from Esri or backup from Google Cloud Storage (GCS) if the row count for vacant land is below 20,000.

    The function initializes a `FeatureLayer` for vacant properties, checks if the vacant land data from Esri contains fewer than 20,000 rows,
    and if so, loads backup data from GCS. The function also renames certain columns for consistency.

    Returns:
        FeatureLayer: The `FeatureLayer` object containing the vacant properties data.
    """

    vacant_properties = FeatureLayer(
        name="Vacant Properties",
        esri_rest_urls=VACANT_PROPS_LAYERS_TO_LOAD,
        cols=[
            "ADDRESS",
            "OWNER1",
            "OWNER2",
            "BLDG_DESC",
            "COUNCILDISTRICT",
            "ZONINGBASEDISTRICT",
            "ZIPCODE",
            "OPA_ID",
            "parcel_type",
        ],
    )

    # Check for vacant land specifically
    vacant_land_gdf = vacant_properties.gdf[
        vacant_properties.gdf["parcel_type"] == "Land"
    ]

    # Print the size of the vacant land dataset
    print(f"Vacant land data size: {len(vacant_land_gdf)} rows.")

    # If the number of rows is less than 20,000, load backup data from GCS
    if len(vacant_land_gdf) < 20000:
        print("Vacant land data is below the threshold. Loading backup data from GCS.")
        backup_gdf = load_backup_data_from_gcs("vacant_indicators_land_06_2024.geojson")

        # Ensure columns match between the backup and the original dataset
        common_columns = vacant_properties.gdf.columns.intersection(backup_gdf.columns)

        # Align the backup data with the original dataset's columns
        backup_gdf = backup_gdf[common_columns]

        # Add the parcel_type column to the backup data and set it to "Land"
        backup_gdf["parcel_type"] = "Land"

        # Drop the old land data from the main dataframe
        vacant_properties.gdf = vacant_properties.gdf[
            vacant_properties.gdf["parcel_type"] != "Land"
        ]

        # Concatenate the backup data with the existing data
        print(f"Appending backup data ({len(backup_gdf)} rows) to the existing data.")
        vacant_properties.gdf = pd.concat(
            [vacant_properties.gdf, backup_gdf], ignore_index=True
        )

    # Print the size of the dataset before dropping NAs
    print(
        f"Vacant properties data size before dropping NAs: {len(vacant_properties.gdf)} rows."
    )

    # Drop rows with missing 'opa_id' values
    vacant_properties.gdf.dropna(subset=["opa_id"], inplace=True)

    # Print the size of the dataset after dropping NAs
    print(
        f"Vacant properties data size after dropping NAs: {len(vacant_properties.gdf)} rows."
    )

    # Rename columns for consistency (this ensures the existing data also matches)
    vacant_properties.gdf = vacant_properties.gdf.rename(
        columns={
            "owner1": "owner_1",
            "owner2": "owner_2",
            "bldg_desc": "building_description",
            "councildistrict": "council_district",
            "zoningbasedistrict": "zoning_base_district",
        }
    )

    return vacant_properties

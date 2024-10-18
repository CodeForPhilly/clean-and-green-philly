from classes.featurelayer import FeatureLayer, google_cloud_bucket
from constants.services import VACANT_PROPS_LAYERS_TO_LOAD
import geopandas as gpd
from config.config import USE_CRS
from io import BytesIO

import pandas as pd


def load_backup_data_from_gcs(file_name: str) -> gpd.GeoDataFrame:
    bucket = google_cloud_bucket()
    blob = bucket.blob(file_name)
    if not blob.exists():
        raise FileNotFoundError(f"File {file_name} not found in the GCS bucket.")

    file_bytes = blob.download_as_bytes()
    try:
        gdf = gpd.read_file(BytesIO(file_bytes))
    except Exception as e:
        raise ValueError(f"Error reading GeoJSON file: {e}")

    print("Loaded backup data from GCS.")

    # Ensure column names are consistent
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


def check_null_percentage(df: pd.DataFrame, threshold: float = 0.05):
    """Checks if any column in the dataframe has more than the given threshold of null values."""
    null_percentages = df.isnull().mean()
    for col, pct in null_percentages.items():
        if col not in ["owner1", "owner2"] and pct > threshold:
            raise ValueError(
                f"Column '{col}' has more than {threshold * 100}% null values ({pct * 100}%)."
            )


def vacant_properties() -> FeatureLayer:
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

    # Rename columns for consistency in the original data
    vacant_properties.gdf = vacant_properties.gdf.rename(
        columns={
            "ADDRESS": "address",
            "OWNER1": "owner_1",
            "OWNER2": "owner_2",
            "BLDG_DESC": "building_description",
            "COUNCILDISTRICT": "council_district",
            "ZONINGBASEDISTRICT": "zoning_base_district",
            "ZIPCODE": "zipcode",
            "OPA_ID": "opa_id",
        }
    )

    vacant_land_gdf = vacant_properties.gdf[
        vacant_properties.gdf["parcel_type"] == "Land"
    ]
    print(f"Vacant land data size: {len(vacant_land_gdf)} rows.")

    if len(vacant_land_gdf) < 20000:
        print("Vacant land data is below the threshold. Loading backup data from GCS.")
        backup_gdf = load_backup_data_from_gcs("vacant_indicators_land_06_2024.geojson")

        # Ensure CRS is consistent with project-wide CRS (USE_CRS)
        if backup_gdf.crs != USE_CRS:
            print(f"Reprojecting backup data from {backup_gdf.crs} to {USE_CRS}")
            backup_gdf = backup_gdf.to_crs(USE_CRS)

        # Ensure CRS is the same
        if backup_gdf.crs != vacant_properties.gdf.crs:
            backup_gdf = backup_gdf.to_crs(vacant_properties.gdf.crs)

        # Map backup dataset column names to match the original dataset
        backup_gdf = backup_gdf.rename(
            columns={
                "owner_1": "owner1",
                "owner_2": "owner2",
                "building_description": "bldg_desc",
                "council_district": "councildistrict",
                "zoning_base_district": "zoningbasedistrict",
            }
        )

        # Set parcel_type to "Land" for backup data
        backup_gdf["parcel_type"] = "Land"

        # Select only the columns present in the original dataset
        backup_gdf = backup_gdf[vacant_properties.gdf.columns]

        # Ensure all necessary columns are present in backup data
        for col in vacant_properties.gdf.columns:
            if col not in backup_gdf.columns:
                backup_gdf[col] = None

        # Check for column mismatches between original and backup datasets
        for col in vacant_properties.gdf.columns:
            if vacant_properties.gdf[col].dtype != backup_gdf[col].dtype:
                print(
                    f"Warning: Data type mismatch in column '{col}'. Original: {vacant_properties.gdf[col].dtype}, Backup: {backup_gdf[col].dtype}"
                )

        # Verify if backup data contains more than expected null values
        check_null_percentage(backup_gdf)

        # Remove existing Land data
        vacant_properties.gdf = vacant_properties.gdf[
            vacant_properties.gdf["parcel_type"] != "Land"
        ]

        # Concatenate the backup data with the existing data
        print(f"Appending backup data ({len(backup_gdf)} rows) to the existing data.")
        vacant_properties.gdf = pd.concat(
            [vacant_properties.gdf, backup_gdf], ignore_index=True
        )

        # Ensure concatenated data is still a GeoDataFrame
        vacant_properties.gdf = gpd.GeoDataFrame(
            vacant_properties.gdf, geometry="geometry"
        )

    print(
        f"Vacant properties data size before dropping NAs: {len(vacant_properties.gdf)} rows."
    )
    vacant_properties.gdf.dropna(subset=["opa_id"], inplace=True)
    print(
        f"Vacant properties data size after dropping NAs: {len(vacant_properties.gdf)} rows."
    )

    # Final null value check before returning
    check_null_percentage(vacant_properties.gdf)

    # Final column renaming and selection
    vacant_properties.gdf = vacant_properties.gdf.rename(
        columns={
            "owner1": "owner_1",
            "owner2": "owner_2",
            "councildistrict": "council_district",
            "zoningbasedistrict": "zoning_base_district",
        }
    )

    # Select only the final columns needed
    final_columns = [
        "address",
        "owner_1",
        "owner_2",
        "council_district",
        "zoning_base_district",
        "zipcode",
        "opa_id",
        "parcel_type",
        "geometry",
    ]

    vacant_properties.gdf = vacant_properties.gdf[final_columns]

    # Ensure concatenated data is still a GeoDataFrame
    vacant_properties.gdf = gpd.GeoDataFrame(vacant_properties.gdf, geometry="geometry")

    return vacant_properties

from classes.featurelayer import FeatureLayer, google_cloud_bucket
from constants.services import VACANT_PROPS_LAYERS_TO_LOAD
import geopandas as gpd
from io import BytesIO
import pandas as pd


def load_backup_data_from_gcs(file_name: str) -> pd.DataFrame:
    bucket = google_cloud_bucket()
    blob = bucket.blob(file_name)
    if not blob.exists():
        raise FileNotFoundError(f"File {file_name} not found in the GCS bucket.")

    file_bytes = blob.download_as_bytes()
    try:
        # Read GeoJSON as a GeoDataFrame
        gdf = gpd.read_file(BytesIO(file_bytes))
    except Exception as e:
        raise ValueError(f"Error reading GeoJSON file: {e}")

    print("Loaded backup data from GCS.")

    # Ensure only opa_id is retained and convert to DataFrame (drop geometry)
    gdf = gdf[["OPA_ID"]].rename(columns={"OPA_ID": "opa_id"})

    # Drop the geometry column to avoid CRS issues (we don't need the geometry for matching)
    gdf = gdf.drop(columns=["geometry"], errors="ignore")

    return gdf


def check_null_percentage(df: pd.DataFrame, threshold: float = 0.05):
    """Checks if any column in the dataframe has more than the given threshold of null values."""
    null_percentages = df.isnull().mean()
    for col, pct in null_percentages.items():
        if pct > threshold:
            raise ValueError(
                f"Column '{col}' has more than {threshold * 100}% null values ({pct * 100}%)."
            )


def vacant_properties(primary_featurelayer) -> FeatureLayer:
    vacant_properties = FeatureLayer(
        name="Vacant Properties",
        esri_rest_urls=VACANT_PROPS_LAYERS_TO_LOAD,
        cols=[
            "OPA_ID",
            "parcel_type",
        ],  # Only need opa_id and parcel_type from the vacancy layers
    )

    print("Columns in vacant properties dataset:", vacant_properties.gdf.columns)

    # Rename columns for consistency in the original data
    vacant_properties.gdf = vacant_properties.gdf.rename(columns={"OPA_ID": "opa_id"})

    # Check for "Land" properties in the default dataset
    vacant_land_gdf = vacant_properties.gdf[
        vacant_properties.gdf["parcel_type"] == "Land"
    ]
    print(f"Vacant land data size in the default dataset: {len(vacant_land_gdf)} rows.")

    # If vacant land properties are below the threshold (20,000 rows), load backup data
    if len(vacant_land_gdf) < 20000:
        print(
            "Vacant land data is below the threshold. Removing vacant land rows and loading backup data from GCS."
        )

        # Drop vacant land rows from the current dataset
        vacant_properties.gdf = vacant_properties.gdf[
            vacant_properties.gdf["parcel_type"] != "Land"
        ]

        # Load backup data and ensure it's a DataFrame (dropping geometry)
        backup_gdf = load_backup_data_from_gcs("vacant_indicators_land_06_2024.geojson")

        # Add a parcel_type column with value "Land" for all rows in the backup data
        backup_gdf["parcel_type"] = "Land"

        # Concatenate the backup data with the existing data
        print(f"Appending backup data ({len(backup_gdf)} rows) to the existing data.")
        vacant_properties.gdf = pd.concat(
            [vacant_properties.gdf, backup_gdf], ignore_index=True
        )

    # Drop the geometry column to convert to a regular DataFrame
    df = vacant_properties.gdf.drop(columns=["geometry"], errors="ignore")

    # Drop rows where opa_id is missing
    df.dropna(subset=["opa_id"], inplace=True)

    # Final null value check before returning
    check_null_percentage(df)

    # Create vacant column in the primary feature layer as True/False
    primary_featurelayer.gdf["vacant"] = primary_featurelayer.gdf["opa_id"].isin(df["opa_id"])

    print("Vacant column added based on opa_id match.")

    # Drop the parcel_type column once the decision has been made
    df.drop(columns=["parcel_type"], inplace=True)

    # Return primary_featurelayer after adding vacant column
    return primary_featurelayer

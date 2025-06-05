from io import BytesIO

import geopandas as gpd
import pandas as pd

from ..classes.featurelayer import EsriLoader, google_cloud_bucket
from ..constants.services import VACANT_PROPS_LAYERS_TO_LOAD
from ..metadata.metadata_utils import provide_metadata


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


@provide_metadata()
def vacant_properties(input_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Adds a "vacant" column to the primary feature layer based on vacant property data from
    ESRI layers and backup data from Google Cloud Storage if necessary.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.

    Returns:
        FeatureLayer: The input feature layer with an added "vacant" column.

    Tagline:
        Identify vacant properties.

    Columns Added:
        vacant (bool): Indicates whether the property is vacant.

    Primary Feature Layer Columns Referenced:
        opa_id

    Known Issues:
        - The vacant land data is below the threshold, so backup data is loaded from GCS.
    """
    loader = EsriLoader(
        name="Vacant Properties",
        esri_urls=VACANT_PROPS_LAYERS_TO_LOAD,
        cols=["opa_id", "parcel_type"],
    )

    vacant_properties = loader.load_or_fetch()

    # Filter for "Land" properties in the dataset
    vacant_land_gdf = vacant_properties[vacant_properties["parcel_type"] == "Land"]
    print(f"Vacant land data size in the default dataset: {len(vacant_land_gdf)} rows.")

    # Check if the vacant land data is below the threshold
    if len(vacant_land_gdf) < 20000:
        print(
            "Vacant land data is below the threshold. Removing vacant land rows and loading backup data from GCS."
        )
        vacant_properties = vacant_properties[
            vacant_properties["parcel_type"] != "Land"
        ]

        # Attempt to load backup data from GCS
        try:
            backup_gdf = load_backup_data_from_gcs(
                "vacant_indicators_land_06_2024.geojson"
            )

            # Add parcel_type column to backup data
            backup_gdf["parcel_type"] = "Land"

            # Append backup data to the existing dataset
            print(
                f"Appending backup data ({len(backup_gdf)} rows) to the existing data."
            )
            vacant_properties.gdf = pd.concat(
                [vacant_properties.gdf, backup_gdf], ignore_index=True
            )
        except Exception as e:
            print(
                f"Unable to load backup data for vacancies with error {e} - proceeding with pipeline using only vacant building data"
            )

    # Convert to a regular DataFrame by dropping geometry
    df = vacant_properties.drop(columns=["geometry"], errors="ignore")

    # Drop rows with missing opa_id
    df.dropna(subset=["opa_id"], inplace=True)

    # Final check for null percentages
    check_null_percentage(df)

    # Add "vacant" column to primary feature layer
    input_gdf["vacant"] = input_gdf["opa_id"].isin(df["opa_id"])

    # Drop parcel_type column after processing
    df.drop(columns=["parcel_type"], inplace=True)

    return input_gdf

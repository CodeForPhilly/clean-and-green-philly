from io import BytesIO

import geopandas as gpd
import pandas as pd

from ..classes.featurelayer import FeatureLayer, google_cloud_bucket
from ..constants.services import VACANT_PROPS_LAYERS_TO_LOAD
from ..metadata.metadata_utils import provide_metadata
from ..validation.base import GeoValidator
from ..validation.vacant_properties import VacantPropertiesValidator


def load_backup_data_from_gcs(file_name: str) -> pd.DataFrame:
    """
    Loads backup data from Google Cloud Storage as a DataFrame, ensuring compatibility for matching.

    Args:
        file_name (str): The name of the file to load from GCS.

    Returns:
        pd.DataFrame: A DataFrame containing the backup data with opa_id and geometry.
    """
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

    # Keep both opa_id and geometry, just rename opa_id for consistency
    gdf = gdf.rename(columns={"OPA_ID": "opa_id"})
    return gdf


def analyze_duplicates(df: pd.DataFrame) -> None:
    """
    Analyze duplicate OPA IDs in the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame to analyze for duplicates.
    """
    # Get all duplicate OPA IDs
    duplicates = df[df.duplicated(subset=["opa_id"], keep=False)]

    if not duplicates.empty:
        print(f"\nFound {len(duplicates)} rows with duplicate OPA IDs")
        print(
            f"Number of unique OPA IDs with duplicates: {duplicates['opa_id'].nunique()}"
        )

        # Group by OPA ID and analyze differences
        for opa_id, group in duplicates.groupby("opa_id"):
            print(f"\nAnalyzing duplicates for OPA ID: {opa_id}")
            print(f"Number of duplicates: {len(group)}")

            # Compare all columns for differences
            for col in group.columns:
                if col != "opa_id":  # Skip OPA ID since we know it's the same
                    unique_values = group[col].unique()
                    if len(unique_values) > 1:
                        print(f"\nColumn '{col}' has different values:")
                        print(group[[col]].value_counts().to_string())

            # Print full rows for manual inspection
            print("\nFull rows for manual inspection:")
            print(group.to_string())
            print("\n" + "=" * 80)


def analyze_geometry_nulls(gdf: gpd.GeoDataFrame) -> None:
    """
    Analyze null geometries in the GeoDataFrame.

    Args:
        gdf (gpd.GeoDataFrame): GeoDataFrame to analyze for null geometries.
    """
    # Get rows with null geometries
    null_geoms = gdf[gdf.geometry.isnull()]

    if not null_geoms.empty:
        print(f"\nFound {len(null_geoms)} rows with null geometries")
        print(
            f"Percentage of rows with null geometries: {(len(null_geoms) / len(gdf)) * 100:.2f}%"
        )

        # Check if nulls are coming from specific sources
        if "parcel_type" in gdf.columns:
            print("\nNull geometries by parcel_type:")
            print(null_geoms["parcel_type"].value_counts())

        # Print first few rows with null geometries for inspection
        print("\nFirst 5 rows with null geometries:")
        print(null_geoms.head().to_string())

        # Check if these rows have other data
        print("\nColumns with non-null values in rows with null geometries:")
        for col in null_geoms.columns:
            if col != "geometry":
                non_null_count = null_geoms[col].count()
                if non_null_count > 0:
                    print(f"{col}: {non_null_count} non-null values")


def load_vacant_properties() -> FeatureLayer:
    """Load and validate vacant properties data."""
    vacant_properties = FeatureLayer(
        name="Vacant Properties",
        esri_rest_urls=VACANT_PROPS_LAYERS_TO_LOAD,
        cols=["OPA_ID", "parcel_type"],  # Only need opa_id and parcel_type
    )

    # Rename columns for consistency
    vacant_properties.gdf = vacant_properties.gdf.rename(columns={"OPA_ID": "opa_id"})

    # Filter for "Land" properties in the dataset
    vacant_land_gdf = vacant_properties.gdf[
        vacant_properties.gdf["parcel_type"] == "Land"
    ]
    print(f"Vacant land data size in the default dataset: {len(vacant_land_gdf)} rows.")

    # Check if the vacant land data is below the threshold
    if len(vacant_land_gdf) < 20000:
        print(
            "Vacant land data is below the threshold. Removing vacant land rows and loading backup data from GCS."
        )
        vacant_properties.gdf = vacant_properties.gdf[
            vacant_properties.gdf["parcel_type"] != "Land"
        ]

        # Load backup data
        backup_gdf = load_backup_data_from_gcs("vacant_indicators_land_06_2024.geojson")

        # Add parcel_type column to backup data
        backup_gdf["parcel_type"] = "Land"

        # Append backup data to the existing dataset
        print(f"Appending backup data ({len(backup_gdf)} rows) to the existing data.")
        vacant_properties.gdf = pd.concat(
            [vacant_properties.gdf, backup_gdf], ignore_index=True
        )

    # Check for null OPA IDs before dropping them
    null_opa_ids = vacant_properties.gdf[vacant_properties.gdf["opa_id"].isnull()]
    if not null_opa_ids.empty:
        print(f"\nFound {len(null_opa_ids)} rows with null OPA IDs:")
        print("Indices of rows with null OPA IDs:")
        print(null_opa_ids.index.tolist())
        print("\nDropping rows with null OPA IDs...")

    # Drop rows with missing opa_id
    vacant_properties.gdf.dropna(subset=["opa_id"], inplace=True)
    print(f"Remaining rows after dropping null OPA IDs: {len(vacant_properties.gdf)}")

    # Analyze duplicates before handling them
    print("\nAnalyzing duplicates in the dataset...")
    analyze_duplicates(vacant_properties.gdf)

    # Drop duplicates, keeping the first occurrence
    original_len = len(vacant_properties.gdf)
    vacant_properties.gdf.drop_duplicates(subset=["opa_id"], keep="first", inplace=True)
    print(f"\nDropped {original_len - len(vacant_properties.gdf)} duplicate rows")
    print(f"Remaining rows after dropping duplicates: {len(vacant_properties.gdf)}")

    # Analyze null geometries
    print("\nAnalyzing null geometries...")
    analyze_geometry_nulls(vacant_properties.gdf)

    # Drop rows with null geometries since they're from backup data and we only need their opa_id
    original_len = len(vacant_properties.gdf)
    vacant_properties.gdf = vacant_properties.gdf[
        ~vacant_properties.gdf.geometry.isnull()
    ]
    print(
        f"\nDropped {original_len - len(vacant_properties.gdf)} rows with null geometries"
    )
    print(
        f"Remaining rows after dropping null geometries: {len(vacant_properties.gdf)}"
    )

    # Now validate the cleaned data
    GeoValidator.validate(vacant_properties.gdf)

    return vacant_properties


@provide_metadata()
@GeoValidator.validate_input
@VacantPropertiesValidator.validate_output
def vacant_properties(primary_featurelayer: FeatureLayer) -> FeatureLayer:
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
    # Load and validate vacant properties data
    vacant_props = load_vacant_properties()

    # Convert to a regular DataFrame by dropping geometry
    df = vacant_props.gdf.drop(columns=["geometry"], errors="ignore")

    # Debug: Print available columns
    print("\nAvailable columns in primary_featurelayer:")
    print(primary_featurelayer.gdf.columns.tolist())
    print("\nAvailable columns in vacant properties:")
    print(df.columns.tolist())

    # Ensure opa_id is string type for consistent comparison
    df["opa_id"] = df["opa_id"].astype(str)

    # Check if opa_id exists in primary_featurelayer
    if "opa_id" not in primary_featurelayer.gdf.columns:
        print(
            "Warning: opa_id not found in primary_featurelayer. Checking for parcel_number..."
        )
        if "parcel_number" in primary_featurelayer.gdf.columns:
            print("Found parcel_number, using it as opa_id")
            primary_featurelayer.gdf["opa_id"] = primary_featurelayer.gdf[
                "parcel_number"
            ].astype(str)
        else:
            raise ValueError(
                "Neither opa_id nor parcel_number found in primary_featurelayer"
            )
    else:
        primary_featurelayer.gdf["opa_id"] = primary_featurelayer.gdf["opa_id"].astype(
            str
        )

    # Add "vacant" column to primary feature layer
    primary_featurelayer.gdf["vacant"] = primary_featurelayer.gdf["opa_id"].isin(
        df["opa_id"]
    )

    # Drop parcel_type column after processing
    df.drop(columns=["parcel_type"], inplace=True)

    return primary_featurelayer

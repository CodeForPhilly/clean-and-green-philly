from typing import Tuple

import geopandas as gpd
import pandas as pd

from src.validation.base import ValidationResult, validate_output
from src.validation.council_dists import (
    CouncilDistrictsInputValidator,
    CouncilDistrictsOutputValidator,
)

from ..classes.loaders import EsriLoader
from ..constants.services import COUNCIL_DISTRICTS_TO_LOAD
from ..utilities import spatial_join

pd.set_option("future.no_silent_downcasting", True)


@validate_output(CouncilDistrictsOutputValidator)
def council_dists(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Associates properties in the primary feature layer with council districts
    using a spatial join.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.

    Returns:
        FeatureLayer: The input feature layer with properties spatially joined
        to council districts, ensuring no duplicate entries.

    Tagline:
        Assigns council districts

    Columns added:
        district (str): The council district associated with the property.

    Primary Feature Layer Columns Referenced:
        opa_id, geometry
    """

    loader = EsriLoader(
        name="Council Districts",
        esri_urls=COUNCIL_DISTRICTS_TO_LOAD,
        cols=["district"],
        validator=CouncilDistrictsInputValidator(),
        input_crs="EPSG:4326",  # Load in geographic coordinates since the data appears to be lat/lon
    )

    council_dists, input_validation = loader.load_or_fetch()

    # Check that the required columns exist in the DataFrame
    required_columns = ["district", "geometry"]
    missing_columns = [
        col for col in required_columns if col not in council_dists.columns
    ]
    if missing_columns:
        raise KeyError(
            f"Missing required columns in council districts data: {', '.join(missing_columns)}"
        )

    # Check if CRS match before spatial join
    if input_gdf.crs != council_dists.crs:
        print(
            f"CRS MISMATCH: Input properties CRS ({input_gdf.crs}) != Council districts CRS ({council_dists.crs})"
        )
        print("Converting council districts to match input properties CRS...")
        council_dists = council_dists.to_crs(input_gdf.crs)
        print(f"Council districts CRS after conversion: {council_dists.crs}")
    else:
        print("CRS match confirmed")

    merged_gdf = spatial_join(input_gdf, council_dists, predicate="within")

    # Drop duplicates in the primary feature layer
    merged_gdf.drop_duplicates(inplace=True)

    # Debug: Check for duplicate OPA IDs and show what's causing them
    if merged_gdf.duplicated(subset=["opa_id"]).any():
        duplicate_count = merged_gdf.duplicated(subset=["opa_id"]).sum()
        print(f"\n[DEBUG] Found {duplicate_count} duplicate OPA IDs after spatial join")

        # Show the actual duplicate OPA IDs
        duplicate_opa_ids = merged_gdf[
            merged_gdf.duplicated(subset=["opa_id"], keep=False)
        ]
        print("\n[DEBUG] Duplicate OPA IDs details:")
        print(f"Total rows with duplicates: {len(duplicate_opa_ids)}")

        # Show first few duplicate groups
        duplicate_groups = duplicate_opa_ids.groupby("opa_id")
        print("\n[DEBUG] First 5 duplicate groups:")
        for i, (opa_id, group) in enumerate(duplicate_groups):
            if i >= 5:
                break
            print(f"\nOPA ID '{opa_id}' appears {len(group)} times:")
            print(group[["opa_id", "district", "geometry"]].to_string(index=False))

        # Show summary of what's different between duplicates
        print("\n[DEBUG] Summary of duplicate causes:")
        for opa_id, group in duplicate_groups:
            if len(group) > 1:
                print(f"OPA ID {opa_id}: {len(group)} rows")
                if "district" in group.columns:
                    districts = group["district"].unique()
                    print(f"  Districts: {districts}")
                if "geometry" in group.columns:
                    geom_types = group["geometry"].type.unique()
                    print(f"  Geometry types: {geom_types}")
                break  # Just show first one as example

    # Ensure we have only one row per opa_id (in case spatial join created duplicates)
    if merged_gdf.duplicated(subset=["opa_id"]).any():
        print(
            f"Found {merged_gdf.duplicated(subset=['opa_id']).sum()} duplicate OPA IDs after spatial join"
        )
        print("Keeping first occurrence of each OPA ID...")
        merged_gdf = merged_gdf.drop_duplicates(subset=["opa_id"], keep="first")
        print(f"After deduplication: {len(merged_gdf)} rows")

    # Check for properties without district assignments
    if "district" in merged_gdf.columns:
        null_district_count = merged_gdf["district"].isna().sum()
        if null_district_count > 0:
            print(
                f"\n[DEBUG] Found {null_district_count} properties without district assignments"
            )
            print("Attempting to assign districts using nearest neighbor...")

            # For properties without districts, try to assign based on nearest district
            null_district_mask = merged_gdf["district"].isna()
            properties_without_districts = merged_gdf[null_district_mask]

            if len(properties_without_districts) > 0:
                # Use nearest neighbor to assign districts
                for idx in properties_without_districts.index:
                    property_geom = merged_gdf.loc[idx, "geometry"]
                    # Find the nearest district boundary
                    distances = council_dists.geometry.distance(property_geom)
                    nearest_district_idx = distances.idxmin()
                    nearest_district = council_dists.loc[
                        nearest_district_idx, "district"
                    ]
                    merged_gdf.loc[idx, "district"] = nearest_district

                print(
                    f"Assigned districts to {null_district_count} properties using nearest neighbor"
                )

            # Final check
            final_null_count = merged_gdf["district"].isna().sum()
            if final_null_count > 0:
                print(
                    f"WARNING: {final_null_count} properties still have null district values"
                )

    return merged_gdf, input_validation

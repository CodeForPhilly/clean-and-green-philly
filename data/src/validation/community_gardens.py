from typing import List, Tuple

import geopandas as gpd
import pandas as pd

from src.config.config import USE_CRS

from ..classes.loaders import FeatureLayer
from .base import ServiceValidator
from ..constants.services import COMMUNITY_GARDENS_TO_LOAD


class CommunityGardensValidator(ServiceValidator):
    """Validator for community gardens data quality and processing."""

    def validate(self, gdf: gpd.GeoDataFrame) -> Tuple[bool, List[str]]:
        """
        Validate community gardens data and processing.

        Args:
            gdf: GeoDataFrame containing the processed data

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []

        # Check required columns
        required_cols = {"geometry", "vacant", "opa_id"}
        missing_cols = required_cols - set(gdf.columns)
        if missing_cols:
            errors.append(f"Missing required columns: {missing_cols}")

        # Check data types
        if "vacant" in gdf.columns and not pd.api.types.is_bool_dtype(gdf["vacant"]):
            errors.append("'vacant' column must be boolean type")

        # Check for null geometries
        null_geoms = gdf.geometry.isna().sum()
        if null_geoms > 0:
            errors.append(f"Found {null_geoms} null geometries")

        # Check for invalid geometries
        invalid_geoms = ~gdf.geometry.is_valid
        if invalid_geoms.any():
            errors.append(f"Found {invalid_geoms.sum()} invalid geometries")

        # Load and validate community gardens data
        try:
            community_gardens = FeatureLayer(
                name="Community Gardens", esri_rest_urls=COMMUNITY_GARDENS_TO_LOAD
            )

            # Check CRS
            if community_gardens.gdf.crs != USE_CRS:
                errors.append(
                    f"Community gardens data has incorrect CRS: {community_gardens.gdf.crs}, expected {USE_CRS}"
                )

            # Check geometry types
            geom_types = community_gardens.gdf.geometry.geom_type.value_counts()
            if len(geom_types) > 1:
                errors.append(
                    f"Community gardens data contains multiple geometry types: {geom_types.to_dict()}"
                )

            # Check for null geometries in community gardens
            null_garden_geoms = community_gardens.gdf.geometry.isna().sum()
            if null_garden_geoms > 0:
                errors.append(
                    f"Found {null_garden_geoms} null geometries in community gardens data"
                )

            # Check for invalid geometries in community gardens
            invalid_garden_geoms = ~community_gardens.gdf.geometry.is_valid
            if invalid_garden_geoms.any():
                errors.append(
                    f"Found {invalid_garden_geoms.sum()} invalid geometries in community gardens data"
                )

            # Check total number of properties being masked
            if "vacant" in gdf.columns:
                masked_count = (~gdf["vacant"]).sum()
                if masked_count > 5000:
                    errors.append(
                        f"Too many properties being masked ({masked_count} > 5000). This may indicate a data issue."
                    )

                # Check if more parcels are being masked than there are gardens
                if masked_count > len(community_gardens.gdf):
                    errors.append(
                        f"More parcels being masked ({masked_count}) than there are community gardens ({len(community_gardens.gdf)}). This may indicate a data issue."
                    )

            # Log statistics
            if "vacant" in gdf.columns:
                total_props = len(gdf)
                masked_props = (~gdf["vacant"]).sum()
                print("\nCommunity Gardens Statistics:")
                print(f"Total properties: {total_props}")
                print(f"Properties masked as non-vacant: {masked_props}")
                print(f"Percentage masked: {(masked_props / total_props) * 100:.2f}%")
                print(f"Total community gardens: {len(community_gardens.gdf)}")

        except Exception as e:
            errors.append(
                f"Error loading or validating community gardens data: {str(e)}"
            )

        return len(errors) == 0, errors

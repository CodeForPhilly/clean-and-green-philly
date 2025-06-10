from typing import List, Tuple

import geopandas as gpd

from .base import ServiceValidator


class RCOGeomsValidator(ServiceValidator):
    """Validator for RCO geoms service."""

    def validate(self, data: gpd.GeoDataFrame) -> Tuple[bool, List[str]]:
        """
        Validate RCO geoms data.

        Critical checks:
        - Required fields present (rco_info, rco_names, geometry)
        - RCO fields are strings
        - Valid geometries
        - RCO info format is correct (semicolon-separated fields)
        - RCO names format is correct (pipe-separated when multiple)

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []

        # Check required columns
        errors.extend(
            self.check_required_columns(data, ["rco_info", "rco_names", "geometry"])
        )

        # Check data types
        if "rco_info" in data.columns and data["rco_info"].dtype != "object":
            errors.append("rco_info must be string type")
        if "rco_names" in data.columns and data["rco_names"].dtype != "object":
            errors.append("rco_names must be string type")

        # Check geometry validity
        if not data.geometry.is_valid.all():
            errors.append("Found invalid geometries")

        # Check RCO info format
        if "rco_info" in data.columns:
            # Check that non-empty rco_info contains expected fields
            non_empty_info = data[data["rco_info"].notna() & (data["rco_info"] != "")]
            if len(non_empty_info) > 0:
                sample_info = non_empty_info["rco_info"].iloc[0]
                if ";" not in sample_info:
                    errors.append("rco_info should contain semicolon-separated fields")

        # Check RCO names format
        if "rco_names" in data.columns:
            # Check that non-empty rco_names contains pipe separator when multiple
            non_empty_names = data[
                data["rco_names"].notna() & (data["rco_names"] != "")
            ]
            if len(non_empty_names) > 0:
                sample_names = non_empty_names["rco_names"].iloc[0]
                if "|" not in sample_names and "," in sample_names:
                    errors.append(
                        "rco_names should use pipe (|) as separator for multiple RCOs"
                    )

        # Log statistics about RCO coverage
        if "rco_names" in data.columns:
            total_properties = len(data)
            properties_with_rco = len(
                data[data["rco_names"].notna() & (data["rco_names"] != "")]
            )
            properties_with_multiple_rcos = len(
                data[data["rco_names"].str.contains("|", na=False)]
            )

            print("RCO Coverage Statistics:")
            print(f"- Total properties: {total_properties}")
            print(
                f"- Properties with RCO: {properties_with_rco} ({properties_with_rco / total_properties:.1%})"
            )
            print(
                f"- Properties with multiple RCOs: {properties_with_multiple_rcos} ({properties_with_multiple_rcos / total_properties:.1%})"
            )

        return len(errors) == 0, errors

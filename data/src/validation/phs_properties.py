from typing import List, Tuple

import geopandas as gpd

from .base import ServiceValidator


class PHSPropertiesValidator(ServiceValidator):
    """Validator for PHS properties service."""

    MAX_MATCHES = 30000  # Maximum reasonable number of PHS program matches

    def validate(self, data: gpd.GeoDataFrame) -> Tuple[bool, List[str]]:
        """
        Validate PHS properties data.

        Critical checks:
        - Required fields present (phs_care_program)
        - phs_care_program is string type
        - Total matches is below threshold
        - No null geometries
        - Valid geometries
        - No duplicate properties

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []

        # Check required columns
        required_columns = ["phs_care_program", "geometry"]
        errors.extend(self.check_required_columns(data, required_columns))

        # Check data types and values
        if "phs_care_program" in data.columns:
            # Check type
            if data["phs_care_program"].dtype != "object":
                errors.append("phs_care_program must be string type")

            # Check values
            invalid_values = data[~data["phs_care_program"].isin(["Yes", "No"])][
                "phs_care_program"
            ].unique()
            if len(invalid_values) > 0:
                errors.append(
                    f"phs_care_program must be 'Yes' or 'No', found: {sorted(invalid_values)}"
                )

            # Get PHS properties subset
            phs_properties = data[data["phs_care_program"] == "Yes"]
            total_matches = len(phs_properties)

            # Check total matches
            if total_matches > self.MAX_MATCHES:
                errors.append(
                    f"Found {total_matches} PHS program matches, which exceeds the maximum of {self.MAX_MATCHES}"
                )

            # Check for null geometries
            null_geoms = phs_properties.geometry.isnull().sum()
            if null_geoms > 0:
                errors.append(f"Found {null_geoms} PHS properties with null geometries")

            # Check for duplicate geometries
            if len(phs_properties) > 0:
                # Convert geometries to WKT for comparison
                wkt_geoms = phs_properties.geometry.apply(
                    lambda x: x.wkt if x else None
                )
                duplicate_geoms = wkt_geoms.value_counts()
                duplicates = duplicate_geoms[duplicate_geoms > 1]
                if len(duplicates) > 0:
                    errors.append(
                        f"Found {len(duplicates)} duplicate geometries in PHS properties"
                    )

            # Log statistics
            print("\nPHS Properties Statistics:")
            print(f"- Total properties: {len(data)}")
            print(
                f"- Properties in PHS program: {total_matches} ({total_matches / len(data):.1%})"
            )

        # Check geometry validity
        if not data.geometry.is_valid.all():
            invalid_count = (~data.geometry.is_valid).sum()
            errors.append(f"Found {invalid_count} invalid geometries")

        return len(errors) == 0, errors

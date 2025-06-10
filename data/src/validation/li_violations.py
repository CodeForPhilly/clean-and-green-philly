from typing import List, Tuple

import geopandas as gpd
import pandas as pd

from .base_validator import BaseValidator


class LIViolationsValidator(BaseValidator):
    """
    Validator for L&I violations data.
    Ensures proper counting and categorization of violations.
    """

    # Keywords used to filter violations
    VIOLATION_KEYWORDS = {
        "dumping",
        "blight",
        "rubbish",
        "weeds",
        "graffiti",
        "abandoned",
        "sanitation",
        "litter",
        "vacant",
        "trash",
        "unsafe",
    }

    def validate(self, gdf: gpd.GeoDataFrame) -> Tuple[bool, List[str]]:
        """
        Validate the L&I violations data.

        Args:
            gdf (gpd.GeoDataFrame): The GeoDataFrame to validate.

        Returns:
            Tuple[bool, List[str]]: A tuple containing:
                - bool: Whether the validation passed
                - List[str]: List of error messages if validation failed
        """
        errors = []

        # Check required columns
        required_columns = [
            "all_violations_past_year",
            "open_violations_past_year",
            "li_code_violations",
            "opa_id",  # Required for checking duplicates
        ]
        missing_columns = [col for col in required_columns if col not in gdf.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")

        # Check for duplicate OPA IDs
        if "opa_id" in gdf.columns:
            duplicate_opa_ids = gdf[gdf.duplicated(subset=["opa_id"], keep=False)]
            if not duplicate_opa_ids.empty:
                errors.append(
                    f"Found {len(duplicate_opa_ids)} duplicate OPA IDs in the violations data"
                )
                # Log some examples of duplicates
                example_duplicates = duplicate_opa_ids["opa_id"].head(5).tolist()
                errors.append(
                    f"Example duplicate OPA IDs: {', '.join(map(str, example_duplicates))}"
                )

        if "all_violations_past_year" in gdf.columns:
            # Check for null values
            null_violations = gdf[gdf["all_violations_past_year"].isna()]
            if not null_violations.empty:
                errors.append(
                    f"Found {len(null_violations)} properties with null all_violations_past_year"
                )

            # Check for negative values
            negative_violations = gdf[gdf["all_violations_past_year"] < 0]
            if not negative_violations.empty:
                errors.append(
                    f"Found {len(negative_violations)} properties with negative all_violations_past_year"
                )

            # Check for non-integer values
            non_integer_violations = gdf[
                ~gdf["all_violations_past_year"].apply(lambda x: float(x).is_integer())
            ]
            if not non_integer_violations.empty:
                errors.append(
                    f"Found {len(non_integer_violations)} properties with non-integer all_violations_past_year"
                )

        if "open_violations_past_year" in gdf.columns:
            # Check for null values
            null_open = gdf[gdf["open_violations_past_year"].isna()]
            if not null_open.empty:
                errors.append(
                    f"Found {len(null_open)} properties with null open_violations_past_year"
                )

            # Check for negative values
            negative_open = gdf[gdf["open_violations_past_year"] < 0]
            if not negative_open.empty:
                errors.append(
                    f"Found {len(negative_open)} properties with negative open_violations_past_year"
                )

            # Check for non-integer values
            non_integer_open = gdf[
                ~gdf["open_violations_past_year"].apply(lambda x: float(x).is_integer())
            ]
            if not non_integer_open.empty:
                errors.append(
                    f"Found {len(non_integer_open)} properties with non-integer open_violations_past_year"
                )

        # Check that open violations don't exceed total violations
        if all(
            col in gdf.columns
            for col in ["all_violations_past_year", "open_violations_past_year"]
        ):
            invalid_counts = gdf[
                gdf["open_violations_past_year"] > gdf["all_violations_past_year"]
            ]
            if not invalid_counts.empty:
                errors.append(
                    f"Found {len(invalid_counts)} properties where open_violations_past_year exceeds all_violations_past_year"
                )

        # Check violation codes
        if "li_code_violations" in gdf.columns:
            # Check for null values
            null_codes = gdf[gdf["li_code_violations"].isna()]
            if not null_codes.empty:
                errors.append(
                    f"Found {len(null_codes)} properties with null li_code_violations"
                )

            # Check that violation codes contain expected keywords
            def check_violation_keywords(codes: str) -> bool:
                if pd.isna(codes):
                    return True
                codes_lower = codes.lower()
                return any(
                    keyword in codes_lower for keyword in self.VIOLATION_KEYWORDS
                )

            invalid_codes = gdf[
                ~gdf["li_code_violations"].apply(check_violation_keywords)
            ]
            if not invalid_codes.empty:
                errors.append(
                    f"Found {len(invalid_codes)} properties with violation codes not matching expected keywords"
                )

        # Log statistics about violations
        if all(
            col in gdf.columns
            for col in ["all_violations_past_year", "open_violations_past_year"]
        ):
            total_properties = len(gdf)
            properties_with_violations = len(gdf[gdf["all_violations_past_year"] > 0])
            properties_with_open_violations = len(
                gdf[gdf["open_violations_past_year"] > 0]
            )

            print("\nL&I Violations Statistics:")
            print(f"- Total properties: {total_properties}")
            print(
                f"- Properties with violations: {properties_with_violations} ({properties_with_violations / total_properties * 100:.1f}%)"
            )
            print(
                f"- Properties with open violations: {properties_with_open_violations} ({properties_with_open_violations / total_properties * 100:.1f}%)"
            )

        return len(errors) == 0, errors

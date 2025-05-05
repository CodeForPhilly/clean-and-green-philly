from typing import Tuple

import pandas as pd

from .base import BaseValidator


class TreeCanopyValidator(BaseValidator):
    """
    Validator for tree canopy data.

    This validator ensures that:
    1. The required 'tree_canopy_gap' column exists
    2. The tree_canopy_gap values are numeric and within expected range (0 to 1)
    3. The geometry column is valid
    """

    def validate(self, data: pd.DataFrame) -> Tuple[bool, list[str]]:
        """
        Validate the tree canopy data.

        Args:
            data (pd.DataFrame): The DataFrame containing tree canopy data.

        Returns:
            Tuple[bool, list[str]]: A tuple containing:
                - bool: True if validation passes, False otherwise
                - list[str]: List of error messages if validation fails
        """
        errors = []

        # Check for required column
        if "tree_canopy_gap" not in data.columns:
            errors.append("Missing required column: tree_canopy_gap")
            return False, errors

        # Check data type of tree_canopy_gap
        if not pd.api.types.is_numeric_dtype(data["tree_canopy_gap"]):
            errors.append("tree_canopy_gap must be numeric")
            return False, errors

        # Check value range (tree canopy gap should be between 0 and 1)
        if (data["tree_canopy_gap"] < 0).any() or (data["tree_canopy_gap"] > 1).any():
            errors.append("tree_canopy_gap values must be between 0 and 1")
            return False, errors

        # Check for missing values
        missing_values = data["tree_canopy_gap"].isna().sum()
        if missing_values > 0:
            errors.append(
                f"Found {missing_values} missing values in tree_canopy_gap column"
            )

        # Check geometry validity
        if not data.geometry.is_valid.all():
            errors.append("Found invalid geometries")

        # Log statistics about tree canopy gaps
        total_properties = len(data)
        high_gap = len(
            data[data["tree_canopy_gap"] >= 0.3]
        )  # Using 0.3 as threshold for "very low tree canopy"
        medium_gap = len(
            data[(data["tree_canopy_gap"] >= 0.1) & (data["tree_canopy_gap"] < 0.3)]
        )
        low_gap = len(data[data["tree_canopy_gap"] < 0.1])

        print("\nTree Canopy Gap Statistics:")
        print(f"- Total properties: {total_properties}")
        print(f"- High gap (≥0.3): {high_gap} ({high_gap / total_properties:.1%})")
        print(
            f"- Medium gap (0.1-0.3): {medium_gap} ({medium_gap / total_properties:.1%})"
        )
        print(f"- Low gap (<0.1): {low_gap} ({low_gap / total_properties:.1%})")

        return len(errors) == 0, errors

import geopandas as gpd
import pandera.pandas as pa

from .base import BaseValidator, is_statistical_summaries_enabled

# Define the Tree Canopy DataFrame Schema
TreeCanopySchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # Tree canopy gap - must be numeric, but allow nulls for testing
        "tree_canopy_gap": pa.Column(
            float,
            nullable=True,  # Allow nulls for testing, but we'll catch them in custom validation
            description="The amount of tree canopy lacking (0.0 to 1.0)",
        ),
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=False,
    coerce=False,
)


class TreeCanopyInputValidator(BaseValidator):
    """Validator for tree canopy service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        print(f"DEBUG: _custom_validation called with check_stats={check_stats}")
        print(f"DEBUG: DataFrame shape: {gdf.shape}")
        print(f"DEBUG: DataFrame columns: {gdf.columns.tolist()}")

        errors = []

        # Always run row-level checks
        print("DEBUG: About to call _row_level_validation")
        self._row_level_validation(gdf, errors)
        print(f"DEBUG: After _row_level_validation, errors: {errors}")

        # Only run statistical checks if requested and data is large enough
        if check_stats and len(gdf) >= self.min_stats_threshold:
            print("DEBUG: About to call _statistical_validation")
            self._statistical_validation(gdf, errors)
            print(f"DEBUG: After _statistical_validation, errors: {errors}")
            # Only print statistical summary if explicitly enabled via context manager
            if is_statistical_summaries_enabled():
                self._print_statistical_summary(gdf)

        # Add all errors to the validator's error list
        print(f"DEBUG: Adding {len(errors)} errors to self.errors")
        self.errors.extend(errors)
        print(f"DEBUG: Total errors in self.errors: {len(self.errors)}")


class TreeCanopyOutputValidator(BaseValidator):
    """Validator for tree canopy service output with comprehensive statistical validation."""

    schema = TreeCanopySchema
    min_stats_threshold = (
        100  # Only run statistical validation for datasets with >= 100 rows
    )

    def _row_level_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Row-level validation that works with any dataset size."""

        # Call parent class method to get empty dataframe check
        super()._row_level_validation(gdf, errors)

        # Check for required columns using helper method
        required_columns = ["tree_canopy_gap", "opa_id"]
        self._validate_required_columns(gdf, required_columns, errors)

        # Validate tree_canopy_gap column
        if "tree_canopy_gap" in gdf.columns:
            # Only fail on nulls if the dataset is small
            null_gap = gdf["tree_canopy_gap"].isna().sum()
            if len(gdf) < self.min_stats_threshold and null_gap > 0:
                errors.append(
                    f"Found {null_gap} null values in 'tree_canopy_gap' column (not allowed for small datasets)"
                )

            # Check for non-numeric values (excluding nulls)
            non_null_gap = gdf["tree_canopy_gap"].dropna()
            non_numeric_gap = (
                ~non_null_gap.apply(lambda x: isinstance(x, (int, float)))
            ).sum()
            if non_numeric_gap > 0:
                errors.append(
                    f"Found {non_numeric_gap} non-numeric values in 'tree_canopy_gap' column"
                )

            # Check for values outside expected range (0.0 to 1.0) - excluding nulls
            out_of_range = ((non_null_gap < 0.0) | (non_null_gap > 1.0)).sum()
            if out_of_range > 0:
                errors.append(
                    f"Found {out_of_range} values outside expected range [0.0, 1.0] in 'tree_canopy_gap' column"
                )

        # Validate opa_id column
        if "opa_id" in gdf.columns:
            # Check for null values
            null_opa = gdf["opa_id"].isna().sum()
            if null_opa > 0:
                errors.append(f"Found {null_opa} null values in 'opa_id' column")

            # Check for non-string values
            non_string_opa = (~gdf["opa_id"].apply(lambda x: isinstance(x, str))).sum()
            if non_string_opa > 0:
                errors.append(
                    f"Found {non_string_opa} non-string values in 'opa_id' column"
                )

            # Check for duplicates
            duplicate_opa = gdf["opa_id"].duplicated().sum()
            if duplicate_opa > 0:
                errors.append(
                    f"Found {duplicate_opa} duplicate values in 'opa_id' column"
                )

        # Validate geometry types
        if "geometry" in gdf.columns:
            # Check for null geometries
            null_geometry = gdf["geometry"].isna().sum()
            if null_geometry > 0:
                errors.append(f"Found {null_geometry} null geometries")

            # Check for valid geometry types (Point, Polygon, MultiPolygon)
            valid_types = ["Point", "Polygon", "MultiPolygon"]
            invalid_geometries = ~gdf["geometry"].type.isin(valid_types)
            invalid_count = invalid_geometries.sum()
            if invalid_count > 0:
                errors.append(
                    f"Found {invalid_count} geometries with invalid types (must be one of {valid_types})"
                )

        print(f"DEBUG: Total errors found: {len(errors)}")
        for error in errors:
            print(f"DEBUG: Error: {error}")

    def _statistical_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Statistical validation that requires larger datasets."""

        # Skip statistical validation for small datasets
        if len(gdf) < self.min_stats_threshold:
            print(
                f"DEBUG: Skipping statistical validation, dataset too small: {len(gdf)} rows"
            )
            return

        # Tree canopy gap statistical validation
        if "tree_canopy_gap" in gdf.columns:
            gap_stats = gdf["tree_canopy_gap"].describe()

            # Print all stats for debugging
            print(f"DEBUG: gap_stats = {gap_stats}")

            # Check non-null percentage (should be around 99.86%)
            non_null_percentage = (
                gdf["tree_canopy_gap"].notna().sum() / len(gdf)
            ) * 100
            print(f"DEBUG: non_null_percentage = {non_null_percentage}")
            if not (99.0 <= non_null_percentage <= 100.0):
                errors.append(
                    f"Tree canopy gap non-null percentage ({non_null_percentage:.2f}%) outside expected range [99.0, 100.0]"
                )
                print("DEBUG: Failed non-null percentage check")

            # Check maximum value (should be around 0.4565896114)
            max_gap = gap_stats["max"]
            print(f"DEBUG: max_gap = {max_gap}")
            if not (0.4 <= max_gap <= 0.5):
                errors.append(
                    f"Tree canopy gap maximum ({max_gap:.6f}) outside expected range [0.4, 0.5]"
                )
                print("DEBUG: Failed max check")

            # Check mean value (should be around 0.1688201897)
            mean_gap = gap_stats["mean"]
            print(f"DEBUG: mean_gap = {mean_gap}")
            if not (0.15 <= mean_gap <= 0.19):
                errors.append(
                    f"Tree canopy gap mean ({mean_gap:.6f}) outside expected range [0.15, 0.19]"
                )
                print("DEBUG: Failed mean check")

            # Check standard deviation (should be around 0.08536259767)
            std_gap = gap_stats["std"]
            print(f"DEBUG: std_gap = {std_gap}")
            if not (0.08 <= std_gap <= 0.09):
                errors.append(
                    f"Tree canopy gap standard deviation ({std_gap:.6f}) outside expected range [0.08, 0.09]"
                )
                print("DEBUG: Failed std check")

            # Check Q1 (should be around 0.1155013519)
            q1_gap = gap_stats["25%"]
            print(f"DEBUG: q1_gap = {q1_gap}")
            if not (0.11 <= q1_gap <= 0.12):
                errors.append(
                    f"Tree canopy gap Q1 ({q1_gap:.6f}) outside expected range [0.11, 0.12]"
                )
                print("DEBUG: Failed Q1 check")

            # Check Q3 (should be around 0.228886177)
            q3_gap = gap_stats["75%"]
            print(f"DEBUG: q3_gap = {q3_gap}")
            if not (0.22 <= q3_gap <= 0.24):
                errors.append(
                    f"Tree canopy gap Q3 ({q3_gap:.6f}) outside expected range [0.22, 0.24]"
                )
                print("DEBUG: Failed Q3 check")

        print(f"DEBUG: Statistical validation errors: {errors}")

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print statistical summary for columns added by the tree canopy service."""
        self._print_summary_header("Tree Canopy Service Statistics", gdf)

        # tree_canopy_gap - The amount of tree canopy lacking
        if "tree_canopy_gap" in gdf.columns:
            gap_stats = gdf["tree_canopy_gap"].describe()
            non_null_count = gdf["tree_canopy_gap"].notna().sum()
            non_null_percentage = (non_null_count / len(gdf)) * 100

            print("\nTree Canopy Gap Statistics:")
            print(f"  Non-null percentage: {non_null_percentage:.2f}%")
            print(f"  Mean: {gap_stats['mean']:.6f}")
            print(f"  Standard deviation: {gap_stats['std']:.6f}")
            print(f"  Minimum: {gap_stats['min']:.6f}")
            print(f"  Q1 (25%): {gap_stats['25%']:.6f}")
            print(f"  Median (50%): {gap_stats['50%']:.6f}")
            print(f"  Q3 (75%): {gap_stats['75%']:.6f}")
            print(f"  Maximum: {gap_stats['max']:.6f}")

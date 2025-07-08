import geopandas as gpd
import pandera.pandas as pa

from .base import BaseValidator, DistributionParams, distribution_check, row_count_check

# Define the LI Violations DataFrame Schema
LIViolationsSchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # All violations past year - must be integer with no NAs
        "all_violations_past_year": pa.Column(
            int,
            nullable=False,
            description="Total number of violations in the past year",
        ),
        # Open violations past year - must be integer with no NAs
        "open_violations_past_year": pa.Column(
            int,
            nullable=False,
            description="Number of open violations in the past year",
        ),
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=False,
    coerce=False,
)

LIViolationsReferenceCount = 54401

LIViolationsInputSchema = pa.DataFrameSchema(
    columns={
        "opa_id": pa.Column(pa.Int, checks=pa.Check(lambda s: s.dropna() != "")),
        "geometry": pa.Column("geometry"),
        "violationcodetitle": pa.Column(str),
        "violationnumber": pa.Column(str),
        "violationstatus": pa.Column(str),
    },
    checks=row_count_check(LIViolationsReferenceCount, tolerance=0.1),
    strict=False,
)


class LIViolationsInputValidator(BaseValidator):
    """Validator for LI violations service input."""

    schema = LIViolationsInputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        pass


all_violations_params = DistributionParams(
    max_value=14, mean=0.0725, std=0.405, q1=0.0, q3=0.0
)
open_violations_params = DistributionParams(
    max_value=11, mean=0.0147, std=0.178, q1=0.0, q3=0.0
)

output_schema = pa.DataFrameSchema(
    {
        "all_violations_past_year": pa.Column(
            int, checks=[*distribution_check(all_violations_params)]
        ),
        "open_violations_past_year": pa.Column(
            int, checks=[*distribution_check(open_violations_params)]
        ),
    }
)


class LIViolationsOutputValidator(BaseValidator):
    """Validator for LI violations service output with comprehensive statistical validation."""

    schema = LIViolationsSchema
    min_stats_threshold = (
        100  # Only run statistical validation for datasets with >= 100 rows
    )

    def _row_level_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Row-level validation that works with any dataset size."""

        # Call parent class method to get empty dataframe check
        super()._row_level_validation(gdf, errors)

        # Check for required columns using helper method
        required_columns = [
            "all_violations_past_year",
            "open_violations_past_year",
            "opa_id",
        ]
        self._validate_required_columns(gdf, required_columns, errors)

        # Validate all_violations_past_year column
        if "all_violations_past_year" in gdf.columns:
            # Check for null values
            null_all_violations = gdf["all_violations_past_year"].isna().sum()
            if null_all_violations > 0:
                errors.append(
                    f"Found {null_all_violations} null values in 'all_violations_past_year' column"
                )

            # Check for non-integer values (excluding nulls)
            non_null_all_violations = gdf["all_violations_past_year"].dropna()
            non_integer_all_violations = (
                ~non_null_all_violations.apply(lambda x: isinstance(x, int))
            ).sum()
            if non_integer_all_violations > 0:
                errors.append(
                    f"Found {non_integer_all_violations} non-integer values in 'all_violations_past_year' column"
                )

            # Check for negative values
            negative_all_violations = (non_null_all_violations < 0).sum()
            if negative_all_violations > 0:
                errors.append(
                    f"Found {negative_all_violations} negative values in 'all_violations_past_year' column"
                )

        # Validate open_violations_past_year column
        if "open_violations_past_year" in gdf.columns:
            # Check for null values
            null_open_violations = gdf["open_violations_past_year"].isna().sum()
            if null_open_violations > 0:
                errors.append(
                    f"Found {null_open_violations} null values in 'open_violations_past_year' column"
                )

            # Check for non-integer values (excluding nulls)
            non_null_open_violations = gdf["open_violations_past_year"].dropna()
            non_integer_open_violations = (
                ~non_null_open_violations.apply(lambda x: isinstance(x, int))
            ).sum()
            if non_integer_open_violations > 0:
                errors.append(
                    f"Found {non_integer_open_violations} non-integer values in 'open_violations_past_year' column"
                )

            # Check for negative values
            negative_open_violations = (non_null_open_violations < 0).sum()
            if negative_open_violations > 0:
                errors.append(
                    f"Found {negative_open_violations} negative values in 'open_violations_past_year' column"
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

    def _statistical_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Statistical validation that requires larger datasets."""

        # Skip statistical validation for small datasets
        if len(gdf) < self.min_stats_threshold:
            return

        # all_violations_past_year statistical validation
        if "all_violations_past_year" in gdf.columns:
            all_violations_stats = gdf["all_violations_past_year"].describe()

            # Check maximum value (should be around 14)
            max_all_violations = all_violations_stats["max"]
            if not (10 <= max_all_violations <= 20):
                errors.append(
                    f"All violations past year maximum ({max_all_violations}) outside expected range [10, 20]"
                )

            # Check mean value (should be around 0.0725)
            mean_all_violations = all_violations_stats["mean"]
            if not (0.05 <= mean_all_violations <= 0.10):
                errors.append(
                    f"All violations past year mean ({mean_all_violations:.4f}) outside expected range [0.05, 0.10]"
                )

            # Check standard deviation (should be around 0.405)
            std_all_violations = all_violations_stats["std"]
            if not (0.35 <= std_all_violations <= 0.45):
                errors.append(
                    f"All violations past year standard deviation ({std_all_violations:.3f}) outside expected range [0.35, 0.45]"
                )

            # Check Q1 (should be around 0.000)
            q1_all_violations = all_violations_stats["25%"]
            if not (0.0 <= q1_all_violations <= 0.001):
                errors.append(
                    f"All violations past year Q1 ({q1_all_violations:.3f}) outside expected range [0.0, 0.001]"
                )

            # Check Q3 (should be around 0.000)
            q3_all_violations = all_violations_stats["75%"]
            if not (0.0 <= q3_all_violations <= 0.001):
                errors.append(
                    f"All violations past year Q3 ({q3_all_violations:.3f}) outside expected range [0.0, 0.001]"
                )

        # open_violations_past_year statistical validation
        if "open_violations_past_year" in gdf.columns:
            open_violations_stats = gdf["open_violations_past_year"].describe()

            # Check maximum value (should be around 11)
            max_open_violations = open_violations_stats["max"]
            if not (8 <= max_open_violations <= 15):
                errors.append(
                    f"Open violations past year maximum ({max_open_violations}) outside expected range [8, 15]"
                )

            # Check mean value (should be around 0.0147)
            mean_open_violations = open_violations_stats["mean"]
            if not (0.01 <= mean_open_violations <= 0.02):
                errors.append(
                    f"Open violations past year mean ({mean_open_violations:.4f}) outside expected range [0.01, 0.02]"
                )

            # Check standard deviation (should be around 0.178)
            std_open_violations = open_violations_stats["std"]
            if not (0.15 <= std_open_violations <= 0.20):
                errors.append(
                    f"Open violations past year standard deviation ({std_open_violations:.3f}) outside expected range [0.15, 0.20]"
                )

            # Check Q1 (should be around 0.000)
            q1_open_violations = open_violations_stats["25%"]
            if not (0.0 <= q1_open_violations <= 0.001):
                errors.append(
                    f"Open violations past year Q1 ({q1_open_violations:.3f}) outside expected range [0.0, 0.001]"
                )

            # Check Q3 (should be around 0.000)
            q3_open_violations = open_violations_stats["75%"]
            if not (0.0 <= q3_open_violations <= 0.001):
                errors.append(
                    f"Open violations past year Q3 ({q3_open_violations:.3f}) outside expected range [0.0, 0.001]"
                )

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print LI violations-specific statistical summary."""
        self._print_summary_header("LI Violations Statistics", gdf)

        if "all_violations_past_year" in gdf.columns:
            all_violations_stats = gdf["all_violations_past_year"].describe()
            print("All violations past year statistics:")
            print(f"  Mean: {all_violations_stats['mean']:.4f}")
            print(f"  Std:  {all_violations_stats['std']:.3f}")
            print(f"  Min:  {all_violations_stats['min']:.0f}")
            print(f"  Max:  {all_violations_stats['max']:.0f}")
            print(f"  Q1:   {all_violations_stats['25%']:.3f}")
            print(f"  Q3:   {all_violations_stats['75%']:.3f}")

        if "open_violations_past_year" in gdf.columns:
            open_violations_stats = gdf["open_violations_past_year"].describe()
            print("Open violations past year statistics:")
            print(f"  Mean: {open_violations_stats['mean']:.4f}")
            print(f"  Std:  {open_violations_stats['std']:.3f}")
            print(f"  Min:  {open_violations_stats['min']:.0f}")
            print(f"  Max:  {open_violations_stats['max']:.0f}")
            print(f"  Q1:   {open_violations_stats['25%']:.3f}")
            print(f"  Q3:   {open_violations_stats['75%']:.3f}")

        self._print_summary_footer()

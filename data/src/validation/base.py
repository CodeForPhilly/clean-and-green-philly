import functools
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, List, Optional

import geopandas as gpd
import pandas as pd
import pandera.pandas as pa
from pandera import Check

from src.config.config import (
    USE_CRS,
    get_logger,
    is_statistical_summaries_enabled,
)
from src.constants.city_limits import PHL_GEOMETRY


class ValidationResult:
    def __init__(self, success: bool, errors: List[str] = []):
        self.success = success
        self.errors = errors

    def __bool__(self):
        return self.success


class BaseValidator(ABC):
    """Base class for service-specific data validation."""

    schema = None  # Can be DataFrameSchema or None
    min_stats_threshold = 100  # Can be overridden by subclasses

    def __init_subclass__(cls):
        schema = getattr(cls, "schema", None)
        if schema is not None:
            # Check if it's a property (has getter/setter)
            if hasattr(schema, "__get__"):
                # It's a property, so we can't check the type at class definition time
                pass
            elif not isinstance(schema, pa.DataFrameSchema):
                raise TypeError(
                    f"{cls.__name__} must define a 'schema' class variable that is a pandera.pandas.DataFrameSchema instance."
                )
        return super().__init_subclass__()

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.errors = []

    def _print_sample_problematic_data(
        self,
        gdf: gpd.GeoDataFrame,
        mask: pd.Series,
        error_type: str,
        max_samples: int = 10,
    ):
        """
        Print a sample of problematic data for debugging.

        Args:
            gdf: The GeoDataFrame containing the data
            mask: Boolean mask identifying problematic rows
            error_type: Description of the error type
            max_samples: Maximum number of samples to print
        """
        if not mask.any():
            return

        problematic_data = gdf[mask]
        sample_size = min(len(problematic_data), max_samples)

        print(
            f"\n=== Sample of {error_type} ({sample_size} of {len(problematic_data)} total) ==="
        )

        # Print sample data with key columns
        sample_data = problematic_data.head(sample_size)

        # Include opa_id if available, plus geometry info
        columns_to_show = []
        if "opa_id" in sample_data.columns:
            columns_to_show.append("opa_id")

        # Add a few other common columns if they exist
        for col in ["public_name", "owner_type", "parcel_type", "zoning"]:
            if col in sample_data.columns:
                columns_to_show.append(col)
                break

        # Always include geometry info
        if len(columns_to_show) > 0:
            print(sample_data[columns_to_show].to_string(index=False))

        # Print geometry bounds for each sample
        print("\nGeometry bounds (minx, miny, maxx, maxy):")
        for i, (idx, row) in enumerate(sample_data.iterrows()):
            bounds = row.geometry.bounds
            opa_info = f"OPA: {row['opa_id']}" if "opa_id" in row else f"Row {i + 1}"
            print(f"  {opa_info}: {bounds}")

        if len(problematic_data) > max_samples:
            print(f"  ... and {len(problematic_data) - max_samples} more")
        print("=" * 60)

    def _print_sample_duplicate_opa_ids(
        self, gdf: gpd.GeoDataFrame, max_samples: int = 10
    ):
        """
        Print a sample of duplicate OPA IDs for debugging.

        Args:
            gdf: The GeoDataFrame containing the data
            max_samples: Maximum number of duplicate groups to show
        """
        if "opa_id" not in gdf.columns:
            return

        # Find duplicates
        duplicates = gdf[gdf.duplicated(subset="opa_id", keep=False)]
        if len(duplicates) == 0:
            return

        # Group by opa_id and get counts
        duplicate_counts = duplicates["opa_id"].value_counts()
        total_duplicates = len(duplicate_counts)

        print(
            f"\n=== Sample of Duplicate OPA IDs ({min(max_samples, total_duplicates)} of {total_duplicates} duplicate groups) ==="
        )

        # Show first few duplicate groups
        for i, (opa_id, count) in enumerate(duplicate_counts.head(max_samples).items()):
            print(f"\nOPA ID '{opa_id}' appears {count} times:")

            # Get all rows with this OPA ID
            duplicate_rows = gdf[gdf["opa_id"] == opa_id]

            # Show key columns for these rows
            columns_to_show = ["opa_id"]
            for col in ["public_name", "owner_type", "parcel_type", "zoning"]:
                if col in duplicate_rows.columns:
                    columns_to_show.append(col)
                    break

            print(duplicate_rows[columns_to_show].to_string(index=False))

        if total_duplicates > max_samples:
            print(f"\n... and {total_duplicates - max_samples} more duplicate groups")
        print("=" * 60)

    def validate_geometry(self, gdf: gpd.GeoDataFrame) -> ValidationResult:
        """
        Validate geometry data in the GeoDataFrame.
        """
        geometry_debug_logger = get_logger("geometry_debug")

        # Extract EPSG code from input CRS
        gdf.crs.to_epsg() if gdf.crs else None
        USE_CRS.split(":")[1] if ":" in USE_CRS else USE_CRS
        correct_crs = gdf.crs == USE_CRS

        # Debug: Print simplified CRS information on single line
        geometry_debug_logger.info(
            f"CRS: {gdf.crs} (expected: {USE_CRS}) - Match: {correct_crs}"
        )

        # Debug: Print sample geometry coordinates
        geometry_debug_logger.info("Sample geometry coordinates (first 3):")
        for i in range(min(3, len(gdf))):
            geom = gdf.iloc[i].geometry
            if geom.geom_type == "Point":
                coords = (geom.x, geom.y)
            else:
                coords = geom.bounds  # (minx, miny, maxx, maxy)
            geometry_debug_logger.info(f"  Row {i}: {coords}")

        # Step 1: Get Philadelphia's bounding box
        phl_start = time.time()
        phl_bounds = PHL_GEOMETRY.bounds  # (minx, miny, maxx, maxy)
        geometry_debug_logger.info(f"Philadelphia bounds: {phl_bounds}")
        time.time() - phl_start

        # Step 2: Get all geometry bounding boxes at once
        bbox_start = time.time()
        geometry_bounds = (
            gdf.geometry.bounds
        )  # DataFrame with minx, miny, maxx, maxy for each geometry
        time.time() - bbox_start

        # Debug: Print sample of geometry bounds
        geometry_debug_logger.info("Sample geometry bounds (first 3):")
        for i in range(min(3, len(geometry_bounds))):
            bounds = geometry_bounds.iloc[i]
            geometry_debug_logger.info(f"  Row {i}: {bounds.to_dict()}")

        # Step 3: Create three categories using coordinate logic
        category_start = time.time()

        # Category 1 - Definitely Outside: No overlap with Philadelphia's bounding box
        definitely_outside = (
            (geometry_bounds["maxx"] < phl_bounds[0])  # entirely to the left
            | (geometry_bounds["minx"] > phl_bounds[2])  # entirely to the right
            | (geometry_bounds["maxy"] < phl_bounds[1])  # entirely below
            | (geometry_bounds["miny"] > phl_bounds[3])  # entirely above
        )

        # Category 2 - Definitely Inside: Completely contained within Philadelphia's bounding box
        definitely_inside = (
            (
                geometry_bounds["minx"] >= phl_bounds[0]
            )  # left edge inside or on boundary
            & (
                geometry_bounds["maxx"] <= phl_bounds[2]
            )  # right edge inside or on boundary
            & (
                geometry_bounds["miny"] >= phl_bounds[1]
            )  # bottom edge inside or on boundary
            & (
                geometry_bounds["maxy"] <= phl_bounds[3]
            )  # top edge inside or on boundary
        )

        # Category 3 - Boundary Cases: Everything else (overlaps but extends beyond)
        boundary_cases = ~(definitely_outside | definitely_inside)

        time.time() - category_start

        # Print category statistics
        cat1_count = definitely_outside.sum()
        cat2_count = definitely_inside.sum()
        cat3_count = boundary_cases.sum()

        # Step 4: Apply validation logic
        validation_start = time.time()

        # Mark Category 1 as invalid (outside Philadelphia)
        if cat1_count > 0:
            outside_phl = True
            # Print sample of definitely outside geometries
            self._print_sample_problematic_data(
                gdf, definitely_outside, "Definitely Outside Philadelphia"
            )
        else:
            # Only run expensive intersection test on Category 3 geometries
            if cat3_count > 0:
                boundary_gdf = gdf[boundary_cases]
                boundary_outside = ~boundary_gdf.geometry.intersects(PHL_GEOMETRY)
                outside_phl = boundary_outside.any()

                if outside_phl:
                    # Print sample of boundary cases that don't intersect
                    boundary_outside_mask = boundary_cases.copy()
                    boundary_outside_mask[boundary_cases] = boundary_outside
                    self._print_sample_problematic_data(
                        gdf,
                        boundary_outside_mask,
                        "Boundary Cases Outside Philadelphia",
                    )
            else:
                outside_phl = False

        time.time() - validation_start

        total_time = time.time() - phl_start
        print(
            f"    [GEOMETRY] {total_time:.3f}s ({cat1_count} outside, {cat2_count} inside, {cat3_count} boundary)"
        )

        if not correct_crs:
            self.errors.append(
                f"Geodataframe for {self.__class__.__name__} is not using the correct coordinate system pegged to Philadelphia"
            )

        if outside_phl:
            self.errors.append(
                f"Dataframe for {self.__class__.__name__} contains observations outside Philadelphia limits."
            )

        return ValidationResult(success=True, errors=[])

    def opa_validation(self, gdf: gpd.GeoDataFrame):
        """
        Validate the opa_id column in a geodataframe if it exists, including checks for string types and uniqueness

        Args:
            gdf (GeoDataFrame): The GeoDataFrame input to validate.

        Appends errors to the class instance errors
        """
        if "opa_id" in gdf.columns:
            opa_validation_start = time.time()

            # Profile the expensive .apply() call
            opa_string_start = time.time()
            non_string_mask = ~gdf["opa_id"].apply(lambda x: isinstance(x, str))
            opa_string_time = time.time() - opa_string_start

            if non_string_mask.any():
                self.errors.append(
                    f"OPA ids are not all typed as strings for {self.__class__.__name__}"
                )
                # Print sample of non-string OPA IDs
                self._print_sample_problematic_data(
                    gdf, non_string_mask, "Non-String OPA IDs"
                )

            # Profile the uniqueness check
            unique_start = time.time()
            unique_opa = gdf["opa_id"].is_unique
            unique_time = time.time() - unique_start

            if not unique_opa:
                self.errors.append(
                    f"OPA ids contain some duplicates for {self.__class__.__name__}"
                )
                # Print sample of duplicate OPA IDs
                self._print_sample_duplicate_opa_ids(gdf)

            total_opa_time = time.time() - opa_validation_start
            print(
                f"    [OPA] {total_opa_time:.3f}s (string check: {opa_string_time:.3f}s, uniqueness: {unique_time:.3f}s)"
            )

    def validate(
        self, gdf: gpd.GeoDataFrame, check_stats: bool = True
    ) -> ValidationResult:
        """
        Validate the data after a service runs.

        Args:
            gdf: The GeoDataFrame to validate
            check_stats: Whether to run statistical checks (skip for unit tests with small data)

        Returns:
            ValidationResult: A boolean success together with a list of collected errors from validation
        """
        validate_start = time.time()

        # Geometry validation
        geometry_start = time.time()
        self.validate_geometry(gdf)
        geometry_time = time.time() - geometry_start
        if self.errors:
            print("\n[GEOMETRY VALIDATION ERROR]")
            for error in self.errors:
                print(error)
            return ValidationResult(success=False, errors=self.errors.copy())

        # OPA validation
        opa_start = time.time()
        self.opa_validation(gdf)
        opa_time = time.time() - opa_start
        if self.errors:
            print("\n[OPA VALIDATION ERROR]")
            for error in self.errors:
                print(error)
            return ValidationResult(success=False, errors=self.errors.copy())

        # Schema validation
        schema_start = time.time()
        if self.schema:
            try:
                self.schema.validate(gdf, lazy=True)
            except pa.errors.SchemaErrors as err:
                print("\n[SCHEMA VALIDATION ERROR]")
                print("First 10 failure cases:")
                print(err.failure_cases.head(10).to_string(index=False))

                # Summarize errors instead of adding each one individually
                failure_summary = {}
                for _, row in err.failure_cases.iterrows():
                    col = row.get("column", "")
                    check = row.get("check", "")
                    failure = row.get("failure_case", "")

                    # Create a key for this type of error
                    error_key = f"{col} - {check}"

                    if error_key not in failure_summary:
                        failure_summary[error_key] = {"count": 0, "examples": []}

                    failure_summary[error_key]["count"] += 1

                    # Keep track of a few examples
                    if len(failure_summary[error_key]["examples"]) < 3:
                        if pd.notna(failure):
                            if isinstance(failure, (int, float)):
                                example = f"value {failure}"
                            else:
                                example = f"value '{failure}'"
                        else:
                            example = "null/empty value"
                        failure_summary[error_key]["examples"].append(example)

                # Add summarized error messages
                for error_key, details in failure_summary.items():
                    count = details["count"]
                    examples = details["examples"]
                    if count == 1:
                        msg = f"Schema validation failed: {error_key} (1 failure: {examples[0]})"
                    else:
                        example_str = ", ".join(examples)
                        msg = f"Schema validation failed: {error_key} ({count} failures, examples: {example_str})"
                    self.errors.append(msg)

                return ValidationResult(success=False, errors=self.errors.copy())
        schema_time = time.time() - schema_start

        # Custom validation
        custom_start = time.time()
        self._custom_validation(gdf, check_stats=check_stats)
        custom_time = time.time() - custom_start
        if self.errors:
            print("\n[CUSTOM VALIDATION ERROR]")
            for error in self.errors:
                print(error)
            return ValidationResult(success=False, errors=self.errors.copy())

        total_validate_time = time.time() - validate_start
        print(
            f"  [VALIDATE] {total_validate_time:.3f}s (geometry: {geometry_time:.3f}s, opa: {opa_time:.3f}s, schema: {schema_time:.3f}s, custom: {custom_time:.3f}s)"
        )

        return ValidationResult(success=True, errors=[])

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        """
        Template method for custom validation that follows a consistent pattern.

        Args:
            gdf: GeoDataFrame to validate
            check_stats: Whether to run statistical checks (skip for unit tests with small data)
        """
        errors = []

        # Always run row-level checks
        self._row_level_validation(gdf, errors)

        # Only run statistical checks if requested and data is large enough
        if check_stats and len(gdf) >= self.min_stats_threshold:
            self._statistical_validation(gdf, errors)
            # Only print statistical summary if explicitly enabled via context manager
            if is_statistical_summaries_enabled():
                self._print_statistical_summary(gdf)

        # Add all errors to the validator's error list
        self.errors.extend(errors)

    def _row_level_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Row-level validation that works on any dataset size. Override in subclasses."""
        # Check for empty dataframes
        if len(gdf) == 0:
            errors.append("DataFrame is empty - no data to validate")
            return

    def _statistical_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Statistical validation that requires larger datasets. Override in subclasses."""
        pass

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print domain-specific statistics. Override in subclasses."""
        pass

    def _validate_required_columns(
        self, gdf: gpd.GeoDataFrame, required_columns: list, errors: list
    ):
        """Check for missing required columns using pandera."""
        missing_columns = [col for col in required_columns if col not in gdf.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {missing_columns}")

    def _validate_column_schema(
        self, gdf: gpd.GeoDataFrame, column_schemas: dict, errors: list
    ):
        """Validate multiple columns against pandera column definitions."""
        # Create temporary schema with just the columns to validate
        temp_schema = pa.DataFrameSchema(column_schemas, strict=False)
        try:
            temp_schema.validate(gdf, lazy=True)
        except pa.errors.SchemaErrors as err:
            errors.append(err.failure_cases)

    def _validate_unique_count(
        self,
        gdf: gpd.GeoDataFrame,
        column: str,
        errors: list,
        expected_count=None,
        min_count=None,
        max_count=None,
    ):
        """Check if column has expected number of unique values."""
        if column not in gdf.columns:
            errors.append(f"Column '{column}' not found for unique count validation")
            return

        unique_count = gdf[column].nunique()

        if expected_count is not None and unique_count != expected_count:
            errors.append(
                f"Column '{column}' has {unique_count} unique values, expected {expected_count}"
            )

        if min_count is not None and unique_count < min_count:
            errors.append(
                f"Column '{column}' has {unique_count} unique values, minimum expected {min_count}"
            )

        if max_count is not None and unique_count > max_count:
            errors.append(
                f"Column '{column}' has {unique_count} unique values, maximum expected {max_count}"
            )

    def _print_summary_header(self, title: str, gdf: gpd.GeoDataFrame):
        """Print standard header with title and total count."""
        print(f"\n=== {title} ===")
        print(f"Total records: {len(gdf):,}")

    def _print_summary_footer(self):
        """Print standard footer separator."""
        print("=" * 50)


class BaseKDEValidator(BaseValidator):
    """
    Base validator for KDE (Kernel Density Estimation) outputs.

    Validates common KDE output columns and provides hooks for application-specific
    range validation. All KDE outputs should have:
    - density_label (string, non-null)
    - density (numeric, non-null, application-specific ranges)
    - density_zscore (numeric, non-null, application-specific ranges)
    - density_percentile (numeric, non-null, range 0-100)
    """

    # Abstract properties that subclasses must define
    @property
    @abstractmethod
    def density_label_column(self) -> str:
        """Return the name of the density label column."""
        pass

    @property
    @abstractmethod
    def density_column(self) -> str:
        """Return the name of the density column."""
        pass

    @property
    @abstractmethod
    def density_zscore_column(self) -> str:
        """Return the name of the density zscore column."""
        pass

    @property
    @abstractmethod
    def density_percentile_column(self) -> str:
        """Return the name of the density percentile column."""
        pass

    @property
    def schema(self):
        """Dynamic schema based on column names."""
        return pa.DataFrameSchema(
            {
                self.density_label_column: pa.Column(str, nullable=False),
                self.density_column: pa.Column(float, nullable=False),
                self.density_zscore_column: pa.Column(float, nullable=False),
                self.density_percentile_column: pa.Column(
                    int,
                    nullable=False,
                    checks=Check.in_range(0, 100, include_min=True, include_max=True),
                ),
            }
        )

    def _row_level_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Row-level validation for KDE outputs."""
        super()._row_level_validation(gdf, errors)

        # Check for required KDE columns using dynamic column names
        required_columns = [
            self.density_label_column,
            self.density_column,
            self.density_zscore_column,
            self.density_percentile_column,
        ]
        self._validate_required_columns(gdf, required_columns, errors)

        # Validate density ranges (application-specific)
        self._validate_density_ranges(gdf, errors)

        # Validate application-specific requirements
        self._validate_application_specific(gdf, errors)

    def _statistical_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Statistical validation for KDE outputs."""
        # Check percentile distribution (should be roughly uniform 0-100)
        if self.density_percentile_column in gdf.columns:
            percentiles = gdf[self.density_percentile_column]

            # Check that percentiles span a reasonable range
            min_percentile = percentiles.min()
            max_percentile = percentiles.max()

            if min_percentile < 0 or max_percentile > 100:
                errors.append(
                    f"Percentile values outside expected range [0, 100]: "
                    f"min={min_percentile:.2f}, max={max_percentile:.2f}"
                )

            # Check that we have a reasonable distribution (not all same value)
            unique_percentiles = percentiles.nunique()
            if unique_percentiles < 10:  # Arbitrary threshold
                errors.append(
                    f"Percentile distribution appears too narrow: "
                    f"only {unique_percentiles} unique values"
                )

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print KDE-specific statistical summary."""
        self._print_summary_header("KDE Output Statistics", gdf)

        if self.density_column in gdf.columns:
            density_stats = gdf[self.density_column].describe()
            print("Density statistics:")
            print(f"  Mean: {density_stats['mean']:.4e}")
            print(f"  Std:  {density_stats['std']:.4e}")
            print(f"  Min:  {density_stats['min']:.4e}")
            print(f"  Max:  {density_stats['max']:.4e}")

        if self.density_zscore_column in gdf.columns:
            zscore_stats = gdf[self.density_zscore_column].describe()
            print("Z-score statistics:")
            print(f"  Mean: {zscore_stats['mean']:.4f}")
            print(f"  Std:  {zscore_stats['std']:.4f}")
            print(f"  Min:  {zscore_stats['min']:.4f}")
            print(f"  Max:  {zscore_stats['max']:.4f}")

        if self.density_percentile_column in gdf.columns:
            percentile_stats = gdf[self.density_percentile_column].describe()
            print("Percentile statistics:")
            print(f"  Mean: {percentile_stats['mean']:.2f}")
            print(f"  Std:  {percentile_stats['std']:.2f}")
            print(f"  Min:  {percentile_stats['min']:.2f}")
            print(f"  Max:  {percentile_stats['max']:.2f}")

        self._print_summary_footer()

    @abstractmethod
    def _validate_density_ranges(self, gdf: gpd.GeoDataFrame, errors: list):
        """
        Validate density and zscore ranges for the specific application.

        Override in subclasses to implement application-specific range validation.
        This method should check that density and density_zscore values are within
        expected ranges for the particular use case.

        Args:
            gdf: The GeoDataFrame to validate
            errors: List to append validation errors to
        """
        pass

    def _validate_application_specific(self, gdf: gpd.GeoDataFrame, errors: list):
        """
        Validate application-specific requirements beyond standard KDE validation.

        Override in subclasses to add domain-specific validation logic.
        Default implementation does nothing.

        Args:
            gdf: The GeoDataFrame to validate
            errors: List to append validation errors to
        """
        pass


def validate_output(
    validator_cls: BaseValidator,
):
    def decorator(func: Callable[[gpd.GeoDataFrame], gpd.GeoDataFrame]):
        @functools.wraps(func)
        def wrapper(gdf: gpd.GeoDataFrame = None, *args, **kwargs):
            decorator_start = time.time()

            # Create validator
            validator_create_start = time.time()
            validator = validator_cls()
            time.time() - validator_create_start

            # Call the original function
            func_call_start = time.time()
            output_gdf, input_validation = func(gdf, *args, **kwargs)
            func_call_time = time.time() - func_call_start

            # Perform output validation
            output_validation_start = time.time()
            output_validation = validator.validate(output_gdf)
            output_validation_time = time.time() - output_validation_start

            # Check if validation failed and raise exception
            if not output_validation:
                print(
                    f"\n[VALIDATION FAILED] Service {func.__name__} failed validation:"
                )
                for error in output_validation.errors:
                    print(f"  - {error}")
                raise ValueError(
                    f"Validation failed for {func.__name__}: {output_validation.errors}"
                )

            # Create complete validation result
            validation_merge_start = time.time()
            complete_validation = {}
            complete_validation["input"] = input_validation
            complete_validation["output"] = output_validation
            time.time() - validation_merge_start

            decorator_total_time = time.time() - decorator_start
            print(
                f"[VALIDATOR] {decorator_total_time:.3f}s (function: {func_call_time:.3f}s, validation: {output_validation_time:.3f}s)"
            )

            return output_gdf, complete_validation

        return wrapper

    return decorator


no_na_check = Check.ne("NA", error="Value cannot be NA")

unique_check = Check(lambda s: s.is_unique, error="Should have all unique values")


def unique_value_check(lower: int, upper: int) -> Check:
    return Check(
        lambda s: s.nunique() >= lower and s.nunique() < upper,
        error=f"Number of unique values is roughly between {lower} and {upper}",
    )


def null_percentage_check(null_percent: float) -> Check:
    return Check(
        lambda s: s.isnull().mean() >= 0.8 * null_percent
        and s.isnull().mean() <= 1.2 * null_percent,
        error=f"Percentage of nulls in column should be roughly {null_percent}",
    )


def row_count_check(reference_count: int, tolerance: float = 0.1) -> Check:
    """
    Create a check that validates if the DataFrame's row count is within a specified tolerance range.

    Args:
        reference_count: The expected number of rows
        tolerance: The allowed deviation as a percentage (default 10%)

    Returns:
        Check: A pandera Check object that validates row count
    """
    lower_bound = reference_count * (1 - tolerance)
    upper_bound = reference_count * (1 + tolerance)

    return Check(
        lambda df: df.shape[0] >= lower_bound and df.shape[0] <= upper_bound,
        error=f"DataFrame size must be between {int(lower_bound)} and {int(upper_bound)} rows (±{tolerance * 100}% from {reference_count}).",
    )


@dataclass
class DistributionParams:
    min_value: Optional[int | float] = None
    max_value: Optional[int | float] = None
    mean: Optional[int | float] = None
    median: Optional[int | float] = None
    std: Optional[int | float] = None
    q1: Optional[int | float] = None
    q3: Optional[int | float] = None


def distribution_check(params: DistributionParams) -> List[Check]:
    res = []

    if params.min_value:
        res.append(
            Check(lambda s: pd.to_numeric(s, errors="coerce").min() >= params.min_value)
        )
    if params.max_value:
        res.append(
            Check(lambda s: pd.to_numeric(s, errors="coerce").max() <= params.max_value)
        )
    if params.mean:
        res.append(
            Check(
                lambda s: pd.to_numeric(s, errors="coerce").mean() >= 0.8 * params.mean
                and pd.to_numeric(s, errors="coerce").mean() <= 1.2 * params.mean,
                error=f"Column mean should be roughly {params.mean}",
            )
        )
    if params.median:
        res.append(
            Check(
                lambda s: pd.to_numeric(s, errors="coerce").quantile(0.5)
                >= 0.8 * params.median
                and pd.to_numeric(s, errors="coerce").quantile(0.5)
                <= 1.2 * params.median,
                error=f"Column median should be roughly {params.median}",
            )
        )
    if params.std:
        res.append(
            Check(
                lambda s: pd.to_numeric(s, errors="coerce").std() >= 0.8 * params.std
                and pd.to_numeric(s, errors="coerce").std() <= 1.2 * params.std,
                error=f"Column standard deviation should be roughly {params.std}",
            )
        )
    if params.q1:
        res.append(
            Check(
                lambda s: pd.to_numeric(s, errors="coerce").quantile(0.25)
                >= 0.8 * params.q1
                and pd.to_numeric(s, errors="coerce").quantile(0.25) <= 1.2 * params.q1,
                error=f"Column first quantile should be roughly {params.q1}",
            )
        )
    if params.q3:
        res.append(
            Check(
                lambda s: pd.to_numeric(s, errors="coerce").quantile(0.75)
                >= 0.8 * params.q3
                and pd.to_numeric(s, errors="coerce").quantile(0.75) <= 1.2 * params.q3,
                error=f"Column third quantile should be roughly {params.q3}",
            )
        )

    return res

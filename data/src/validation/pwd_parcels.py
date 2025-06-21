import time
from datetime import datetime

import geopandas as gpd
import pandera.pandas as pa

from .base import BaseValidator, ValidationResult

# Define the PWD Parcels DataFrame Schema
PWDParcelsSchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # Condo unit flag - must be boolean with no NAs
        "is_condo_unit": pa.Column(
            bool,
            nullable=False,
            description="Indicates whether the property is a condominium unit",
        ),
        # Parcel area - must be non-negative float
        "parcel_area_sqft": pa.Column(
            float,
            pa.Check.greater_than_or_equal_to(0),
            nullable=False,
            description="The area of the parcel in square feet",
        ),
        # Additional fields that may be present from other services
        "market_value": pa.Column(
            float,
            pa.Check.greater_than_or_equal_to(0),
            nullable=True,
            description="Property market value",
        ),
        "sale_price": pa.Column(
            float,
            pa.Check.greater_than_or_equal_to(0),
            nullable=True,
            description="Last sale price",
        ),
        "sale_date": pa.Column(
            datetime, nullable=True, description="Date of last sale"
        ),
        "zip_code": pa.Column(
            str, nullable=True, description="ZIP code of the property"
        ),
        "zoning": pa.Column(str, nullable=True, description="Zoning classification"),
        "standardized_street_address": pa.Column(
            str, nullable=True, description="Standardized street address"
        ),
        "standardized_mailing_address": pa.Column(
            str, nullable=True, description="Standardized mailing address"
        ),
        "owner_1": pa.Column(str, nullable=True, description="Primary owner"),
        "owner_2": pa.Column(str, nullable=True, description="Secondary owner"),
        "building_code_description": pa.Column(
            str, nullable=True, description="Building code description"
        ),
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=False,
    coerce=True,
)


class PWDParcelsInputValidator(BaseValidator):
    """Validator for PWD parcels service input."""

    schema = None  # No schema validation for input

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class PWDParcelsOutputValidator(BaseValidator):
    """Validator for PWD parcels service output with comprehensive statistical validation."""

    schema = PWDParcelsSchema

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
        self.geometry_validation(gdf)
        geometry_time = time.time() - geometry_start

        # OPA validation
        opa_start = time.time()
        self.opa_validation(gdf)
        opa_time = time.time() - opa_start

        # Schema validation
        schema_start = time.time()
        if self.schema:
            try:
                self.schema.validate(gdf, lazy=True)
            except pa.errors.SchemaErrors as err:
                self.errors.append(err.failure_cases)
        schema_time = time.time() - schema_start

        # Custom validation with check_stats parameter
        custom_start = time.time()
        self._custom_validation(gdf, check_stats=check_stats)
        custom_time = time.time() - custom_start

        total_validate_time = time.time() - validate_start
        print(
            f"  [VALIDATE] {total_validate_time:.3f}s (geometry: {geometry_time:.3f}s, opa: {opa_time:.3f}s, schema: {schema_time:.3f}s, custom: {custom_time:.3f}s)"
        )

        return ValidationResult(success=not self.errors, errors=self.errors)

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        """
        Custom validation beyond the basic schema constraints.

        Args:
            gdf: GeoDataFrame to validate
            check_stats: Whether to run statistical checks (skip for unit tests with small data)
        """
        errors = []

        # Always run row-level checks
        self._row_level_validation(gdf, errors)

        # Only run statistical checks if requested and data is large enough
        if check_stats and len(gdf) > 100:
            self._statistical_validation(gdf, errors)
            self._print_statistical_summary(gdf)

        # Add all errors to the validator's error list
        self.errors.extend(errors)

    def _row_level_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Row-level validation that works with any dataset size."""

        # Check for required columns
        required_columns = ["is_condo_unit", "parcel_area_sqft", "opa_id"]
        missing_columns = [col for col in required_columns if col not in gdf.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {missing_columns}")

        # Validate is_condo_unit column
        if "is_condo_unit" in gdf.columns:
            # Check for null values
            null_condo = gdf["is_condo_unit"].isna().sum()
            if null_condo > 0:
                errors.append(
                    f"Found {null_condo} null values in 'is_condo_unit' column"
                )

            # Check for non-boolean values
            non_bool_condo = (~gdf["is_condo_unit"].isin([True, False])).sum()
            if non_bool_condo > 0:
                errors.append(
                    f"Found {non_bool_condo} non-boolean values in 'is_condo_unit' column"
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

        # Validate parcel_area_sqft column
        if "parcel_area_sqft" in gdf.columns:
            # Check for null values
            null_area = gdf["parcel_area_sqft"].isna().sum()
            if null_area > 0:
                errors.append(
                    f"Found {null_area} null values in 'parcel_area_sqft' column"
                )

            # Check for negative values
            negative_area = (gdf["parcel_area_sqft"] < 0).sum()
            if negative_area > 0:
                errors.append(
                    f"Found {negative_area} negative values in 'parcel_area_sqft' column"
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

        # 1. Condo unit percentage validation
        if "is_condo_unit" in gdf.columns:
            condo_count = gdf["is_condo_unit"].sum()
            total_count = len(gdf)
            condo_percentage = (condo_count / total_count) * 100

            # Expected range: 5-15% of properties should be condo units
            if not (5.0 <= condo_percentage <= 15.0):
                errors.append(
                    f"Condo unit percentage ({condo_percentage:.2f}%) outside expected range [5.0, 15.0]"
                )

        # 2. Geometry type distribution validation
        if "geometry" in gdf.columns:
            geometry_counts = gdf["geometry"].type.value_counts()

            # Check point count (condo units)
            point_count = geometry_counts.get("Point", 0)
            if not (30000 <= point_count <= 50000):
                errors.append(
                    f"Point geometry count ({point_count}) outside expected range [30000, 50000]"
                )

            # Check polygon/multipolygon count (non-condo units)
            polygon_count = geometry_counts.get("Polygon", 0) + geometry_counts.get(
                "MultiPolygon", 0
            )
            if not (500000 <= polygon_count <= 600000):
                errors.append(
                    f"Polygon/MultiPolygon geometry count ({polygon_count}) outside expected range [500000, 600000]"
                )

        # 3. Parcel area validation for non-condo units
        if "parcel_area_sqft" in gdf.columns and "is_condo_unit" in gdf.columns:
            non_condo_properties = gdf[~gdf["is_condo_unit"]]
            if len(non_condo_properties) > 0:
                area_stats = non_condo_properties["parcel_area_sqft"].describe()

                # Check maximum area (should be reasonable for Philadelphia parcels)
                if area_stats["max"] > 100000:  # 100K sq ft (about 2.3 acres)
                    errors.append(
                        f"Parcel area maximum ({area_stats['max']:,.0f} sq ft) exceeds reasonable threshold"
                    )

                # Check mean area (should be around 2,000-8,000 sq ft for typical Philly lots)
                mean_area = area_stats["mean"]
                if not (1000 <= mean_area <= 10000):
                    errors.append(
                        f"Parcel area mean ({mean_area:,.0f} sq ft) outside expected range [1000, 10000]"
                    )

        # 4. Condo unit area validation (should be 0.0)
        if "parcel_area_sqft" in gdf.columns and "is_condo_unit" in gdf.columns:
            condo_properties = gdf[gdf["is_condo_unit"]]
            if len(condo_properties) > 0:
                non_zero_condo_area = (condo_properties["parcel_area_sqft"] > 0).sum()
                if non_zero_condo_area > 0:
                    errors.append(
                        f"Found {non_zero_condo_area} condo units with non-zero parcel area (should be 0.0)"
                    )

        # 5. Geometry type consistency with condo flag
        if "geometry" in gdf.columns and "is_condo_unit" in gdf.columns:
            # Condo units should be points
            condo_properties = gdf[gdf["is_condo_unit"]]
            if len(condo_properties) > 0:
                non_point_condos = (condo_properties["geometry"].type != "Point").sum()
                if non_point_condos > 0:
                    errors.append(
                        f"Found {non_point_condos} condo units with non-point geometries"
                    )

            # Non-condo units should be polygons
            non_condo_properties = gdf[~gdf["is_condo_unit"]]
            if len(non_condo_properties) > 0:
                non_polygon_non_condos = (
                    ~non_condo_properties["geometry"].type.isin(
                        ["Polygon", "MultiPolygon"]
                    )
                ).sum()
                if non_polygon_non_condos > 0:
                    errors.append(
                        f"Found {non_polygon_non_condos} non-condo units with non-polygon geometries"
                    )

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print statistical summary for columns added by the PWD parcels service."""
        print("\n=== PWD Parcels Service Statistics ===")
        print(f"Total properties: {len(gdf):,}")

        # Only print stats for columns added by this service
        # is_condo_unit - Flag indicating if the property is a condominium unit
        if "is_condo_unit" in gdf.columns:
            condo_count = gdf["is_condo_unit"].sum()
            non_condo_count = (~gdf["is_condo_unit"]).sum()
            condo_percentage = (condo_count / len(gdf)) * 100
            print("\nCondo Unit Distribution:")
            print(f"  Condo units: {condo_count:,} ({condo_percentage:.1f}%)")
            print(
                f"  Non-condo units: {non_condo_count:,} ({100 - condo_percentage:.1f}%)"
            )

        # parcel_area_sqft - The area of the parcel in square feet
        if "parcel_area_sqft" in gdf.columns:
            area_stats = gdf["parcel_area_sqft"].describe()
            print("\nParcel Area Statistics (All Properties):")
            print(f"  Mean: {area_stats['mean']:,.0f} sq ft")
            print(f"  Median: {area_stats['50%']:,.0f} sq ft")
            print(f"  Std Dev: {area_stats['std']:,.0f} sq ft")
            print(f"  Q1: {area_stats['25%']:,.0f} sq ft")
            print(f"  Q3: {area_stats['75%']:,.0f} sq ft")
            print(f"  Max: {area_stats['max']:,.0f} sq ft")

            # Check for potential coordinate system issue
            if area_stats["max"] < 1.0:
                print("  ⚠️  WARNING: All parcel areas are very small (< 1 sq ft).")
                print(
                    "     This may indicate the geometries are in geographic coordinates (degrees)"
                )
                print(
                    "     and need to be projected to a local coordinate system before area calculation."
                )

            # Compare condo vs non-condo areas
            if "is_condo_unit" in gdf.columns:
                condo_properties = gdf[gdf["is_condo_unit"]]
                non_condo_properties = gdf[~gdf["is_condo_unit"]]

                if len(condo_properties) > 0:
                    condo_area_stats = condo_properties["parcel_area_sqft"].describe()
                    print("\nParcel Area Statistics (Condo Units):")
                    print(f"  Mean: {condo_area_stats['mean']:,.0f} sq ft")
                    print(f"  Median: {condo_area_stats['50%']:,.0f} sq ft")
                    print(f"  Std Dev: {condo_area_stats['std']:,.0f} sq ft")

                if len(non_condo_properties) > 0:
                    non_condo_area_stats = non_condo_properties[
                        "parcel_area_sqft"
                    ].describe()
                    print("\nParcel Area Statistics (Non-Condo Units):")
                    print(f"  Mean: {non_condo_area_stats['mean']:,.0f} sq ft")
                    print(f"  Median: {non_condo_area_stats['50%']:,.0f} sq ft")
                    print(f"  Std Dev: {non_condo_area_stats['std']:,.0f} sq ft")

        print("=" * 50)

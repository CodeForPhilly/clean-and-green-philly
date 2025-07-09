import geopandas as gpd
import pandera.pandas as pa

from .base import BaseValidator, row_count_check

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
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=False,
    coerce=False,
)

# Reference count for PWD parcels
PWD_PARCELS_REFERENCE_COUNT = 547351

PWDParcelsInputSchema = pa.DataFrameSchema(
    columns={
        "opa_id": pa.Column(pa.String, checks=pa.Check(lambda s: s.dropna() != "")),
        "geometry": pa.Column("geometry"),
    },
    checks=row_count_check(PWD_PARCELS_REFERENCE_COUNT, tolerance=0.05),
    strict=False,
)


class PWDParcelsInputValidator(BaseValidator):
    """Validator for PWD parcels service input."""

    schema = PWDParcelsInputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        pass


class PWDParcelsOutputValidator(BaseValidator):
    """Validator for PWD parcels service output with comprehensive statistical validation."""

    schema = PWDParcelsSchema
    min_stats_threshold = (
        100  # Only run statistical validation for datasets with >= 100 rows
    )

    def _row_level_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Row-level validation that works with any dataset size."""

        # Call parent class method to get empty dataframe check
        super()._row_level_validation(gdf, errors)

        # Check for required columns using helper method
        required_columns = ["is_condo_unit", "parcel_area_sqft", "opa_id"]
        self._validate_required_columns(gdf, required_columns, errors)

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

        # Skip statistical validation for small datasets
        if len(gdf) < self.min_stats_threshold:
            return

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

                # Check mean area (should be around 2,000-8,000 sq ft for typical Philly lots)
                mean_area = area_stats["mean"]
                if not (1000 <= mean_area <= 10000):
                    errors.append(
                        f"Parcel area mean ({mean_area:,.0f} sq ft) outside expected range [1000, 10000]"
                    )

        # 4. Duplicate geometry validation for non-condo units
        # Non-condo units should not have duplicate geometries (condos can have duplicates)
        # EXCEPT: Allow duplicate point geometries (multi-unit properties)
        if "geometry" in gdf.columns and "is_condo_unit" in gdf.columns:
            non_condo_properties = gdf[~gdf["is_condo_unit"]]
            if len(non_condo_properties) > 0:
                # Find duplicate geometries among non-condo units using unique()
                unique_geometries = non_condo_properties.geometry.unique()
                if len(unique_geometries) < len(non_condo_properties):
                    # There are duplicates - but let's check if they're legitimate
                    duplicate_mask = non_condo_properties.geometry.duplicated(
                        keep=False
                    )
                    duplicate_properties = non_condo_properties[duplicate_mask]

                    # Only flag duplicate polygon geometries as errors (point duplicates are usually legitimate)
                    polygon_duplicates = duplicate_properties[
                        duplicate_properties.geometry.type.isin(
                            ["Polygon", "MultiPolygon"]
                        )
                    ]

                    if len(polygon_duplicates) > 0:
                        print(
                            f"\n[DEBUG] Found {len(polygon_duplicates)} non-condo units with duplicate polygon geometries"
                        )
                        print(f"Total non-condo units: {len(non_condo_properties)}")
                        print(f"Unique geometries: {len(unique_geometries)}")
                        print(f"Total duplicates: {len(duplicate_properties)}")
                        print(
                            f"Point duplicates (allowed): {len(duplicate_properties) - len(polygon_duplicates)}"
                        )
                        print(f"Polygon duplicates (error): {len(polygon_duplicates)}")

                        # Show examples of polygon duplicates
                        print("\nExamples of duplicate polygon geometries:")
                        polygon_geom_examples = polygon_duplicates.geometry.unique()[:3]
                        for i, geom in enumerate(polygon_geom_examples):
                            props_with_geom = polygon_duplicates[
                                polygon_duplicates.geometry == geom
                            ]
                            if len(props_with_geom) > 1:
                                print(f"\nPolygon Geometry {i + 1}: {geom}")
                                print(
                                    f"Properties using this geometry ({len(props_with_geom)}):"
                                )
                                geom_cols = [
                                    "opa_id",
                                    "standardized_street_address",
                                    "building_code_description",
                                ]
                                available_geom_cols = [
                                    col
                                    for col in geom_cols
                                    if col in props_with_geom.columns
                                ]
                                print(
                                    props_with_geom[available_geom_cols].to_string(
                                        index=False
                                    )
                                )

                        errors.append(
                            f"Found {len(polygon_duplicates)} non-condo units with duplicate polygon geometries"
                        )
                    else:
                        print(
                            f"\n[DEBUG] All {len(duplicate_properties)} duplicate geometries are points (legitimate multi-unit properties)"
                        )
                        print("No validation errors for duplicate geometries!")

        # 5. Geometry type consistency with condo flag - more sophisticated validation
        if "geometry" in gdf.columns and "is_condo_unit" in gdf.columns:
            # Condo units can have either points or polygons (individual units within buildings)
            condo_properties = gdf[gdf["is_condo_unit"]]
            if len(condo_properties) > 0:
                # Check for invalid geometry types for condos (should be Point, Polygon, or MultiPolygon)
                invalid_condo_geoms = ~condo_properties["geometry"].type.isin(
                    ["Point", "Polygon", "MultiPolygon"]
                )
                invalid_condo_count = invalid_condo_geoms.sum()
                if invalid_condo_count > 0:
                    # Find the problematic condo units
                    problematic_condos = condo_properties[invalid_condo_geoms]
                    print(
                        f"\n[DEBUG] Found {len(problematic_condos)} condo units with invalid geometry types:"
                    )
                    print("First 10 problematic condo units:")
                    condo_cols = [
                        "opa_id",
                        "geometry",
                        "standardized_street_address",
                        "building_code_description",
                    ]
                    available_cols = [
                        col for col in condo_cols if col in problematic_condos.columns
                    ]
                    print(
                        problematic_condos[available_cols]
                        .head(10)
                        .to_string(index=False)
                    )

                    errors.append(
                        f"Found {invalid_condo_count} condo units with invalid geometry types"
                    )

            # Non-condo units can have points (for properties without parcel boundaries) or polygons
            non_condo_properties = gdf[~gdf["is_condo_unit"]]
            if len(non_condo_properties) > 0:
                # Check for invalid geometry types for non-condos (should be Point, Polygon, or MultiPolygon)
                invalid_non_condo_geoms = ~non_condo_properties["geometry"].type.isin(
                    ["Point", "Polygon", "MultiPolygon"]
                )
                invalid_non_condo_count = invalid_non_condo_geoms.sum()
                if invalid_non_condo_count > 0:
                    # Find the problematic non-condo units
                    problematic_non_condos = non_condo_properties[
                        invalid_non_condo_geoms
                    ]
                    print(
                        f"\n[DEBUG] Found {len(problematic_non_condos)} non-condo units with invalid geometry types:"
                    )
                    print("First 10 problematic non-condo units:")
                    non_condo_cols = [
                        "opa_id",
                        "geometry",
                        "standardized_street_address",
                        "building_code_description",
                    ]
                    available_cols = [
                        col
                        for col in non_condo_cols
                        if col in problematic_non_condos.columns
                    ]
                    print(
                        problematic_non_condos[available_cols]
                        .head(10)
                        .to_string(index=False)
                    )

                    errors.append(
                        f"Found {invalid_non_condo_count} non-condo units with invalid geometry types"
                    )

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print statistical summary for columns added by the PWD parcels service."""
        self._print_summary_header("PWD Parcels Service Statistics", gdf)

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

        self._print_summary_footer()

from datetime import datetime

import geopandas as gpd
import pandera.pandas as pa

from .base import BaseValidator

# Define the Vacant Properties DataFrame Schema
VacantPropertiesSchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # Vacant property flag - must be boolean with no NAs
        "vacant": pa.Column(
            bool, nullable=False, description="Indicates whether the property is vacant"
        ),
        # Property classification - must be specific values with no NAs
        "parcel_type": pa.Column(
            str,
            pa.Check.isin(["Land", "Building"]),
            nullable=False,
            description="Property type classification",
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


class VacantPropertiesInputValidator(BaseValidator):
    """Validator for vacant properties service input."""

    schema = None  # No schema validation for input

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class VacantPropertiesOutputValidator(BaseValidator):
    """Validator for vacant properties service output with comprehensive statistical validation."""

    schema = VacantPropertiesSchema

    def _row_level_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Row-level validation that works with any dataset size."""

        # Call parent class method to get empty dataframe check
        super()._row_level_validation(gdf, errors)

        # Check for required columns using helper method
        required_columns = ["vacant", "opa_id", "parcel_type"]
        self._validate_required_columns(gdf, required_columns, errors)

        # Validate vacant column
        if "vacant" in gdf.columns:
            # Check for null values
            null_vacant = gdf["vacant"].isna().sum()
            if null_vacant > 0:
                errors.append(f"Found {null_vacant} null values in 'vacant' column")

            # Check for non-boolean values
            non_bool_vacant = (~gdf["vacant"].isin([True, False])).sum()
            if non_bool_vacant > 0:
                errors.append(
                    f"Found {non_bool_vacant} non-boolean values in 'vacant' column"
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

        # Validate parcel_type column
        if "parcel_type" in gdf.columns:
            # Check for null values
            null_parcel = gdf["parcel_type"].isna().sum()
            if null_parcel > 0:
                errors.append(
                    f"Found {null_parcel} null values in 'parcel_type' column"
                )

            # Check for invalid values
            valid_parcel_types = ["Land", "Building"]
            invalid_parcel = (~gdf["parcel_type"].isin(valid_parcel_types)).sum()
            if invalid_parcel > 0:
                errors.append(
                    f"Found {invalid_parcel} invalid values in 'parcel_type' column (must be one of {valid_parcel_types})"
                )

    def _statistical_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Statistical validation that requires larger datasets."""

        # 1. Vacant property percentage validation
        if "vacant" in gdf.columns:
            vacant_count = gdf["vacant"].sum()
            total_count = len(gdf)
            vacant_percentage = (vacant_count / total_count) * 100

            # Expected range: 10-15% of properties should be vacant
            if not (10.0 <= vacant_percentage <= 15.0):
                errors.append(
                    f"Vacant property percentage ({vacant_percentage:.2f}%) outside expected range [10.0, 15.0]"
                )

        # 2. Parcel type distribution validation
        if "parcel_type" in gdf.columns:
            parcel_counts = gdf["parcel_type"].value_counts()

            # Check building count (should be roughly 500,000)
            building_count = parcel_counts.get("Building", 0)
            if not (450000 <= building_count <= 550000):
                errors.append(
                    f"Building count ({building_count}) outside expected range [450000, 550000]"
                )

            # Check land count (should be roughly 40,000)
            land_count = parcel_counts.get("Land", 0)
            if not (30000 <= land_count <= 50000):
                errors.append(
                    f"Land count ({land_count}) outside expected range [30000, 50000]"
                )

        # 3. Vacant property parcel type distribution
        if "vacant" in gdf.columns and "parcel_type" in gdf.columns:
            vacant_properties = gdf[gdf["vacant"]]
            if len(vacant_properties) > 0:
                vacant_parcel_counts = vacant_properties["parcel_type"].value_counts()

                # Check vacant building count (should be majority of vacant properties)
                vacant_building_count = vacant_parcel_counts.get("Building", 0)
                vacant_land_count = vacant_parcel_counts.get("Land", 0)
                total_vacant = len(vacant_properties)

                if total_vacant > 0:
                    vacant_building_percentage = (
                        vacant_building_count / total_vacant
                    ) * 100
                    (vacant_land_count / total_vacant) * 100

                    # Most vacant properties should be buildings (roughly 70-90%)
                    if not (70.0 <= vacant_building_percentage <= 90.0):
                        errors.append(
                            f"Vacant building percentage ({vacant_building_percentage:.2f}%) outside expected range [70.0, 90.0]"
                        )

        # 4. ZIP code validation for vacant properties
        if "vacant" in gdf.columns and "zip_code" in gdf.columns:
            vacant_properties = gdf[gdf["vacant"]]
            if len(vacant_properties) > 0:
                unique_zip_count = vacant_properties["zip_code"].nunique()
                # Vacant properties should be distributed across most ZIP codes
                if not (40 <= unique_zip_count <= 60):
                    errors.append(
                        f"Vacant properties ZIP code unique count ({unique_zip_count}) outside expected range [40, 60]"
                    )

        # 5. Market value validation for vacant vs non-vacant properties
        if "vacant" in gdf.columns and "market_value" in gdf.columns:
            vacant_properties = gdf[gdf["vacant"]]
            non_vacant_properties = gdf[~gdf["vacant"]]

            if len(vacant_properties) > 0 and len(non_vacant_properties) > 0:
                vacant_mv_mean = vacant_properties["market_value"].mean()
                non_vacant_mv_mean = non_vacant_properties["market_value"].mean()

                # Vacant properties should generally have lower market values
                if vacant_mv_mean > non_vacant_mv_mean:
                    errors.append(
                        f"Vacant properties have higher average market value ({vacant_mv_mean:,.0f}) than non-vacant properties ({non_vacant_mv_mean:,.0f})"
                    )

        # 6. Zoning validation for vacant properties
        if "vacant" in gdf.columns and "zoning" in gdf.columns:
            vacant_properties = gdf[gdf["vacant"]]
            if len(vacant_properties) > 0:
                # Count non-empty zoning values
                non_empty_zoning = vacant_properties["zoning"].str.strip().ne("")
                unique_zoning_count = vacant_properties.loc[
                    non_empty_zoning, "zoning"
                ].nunique()

                if not (30 <= unique_zoning_count <= 50):
                    errors.append(
                        f"Vacant properties zoning unique count ({unique_zoning_count}) outside expected range [30, 50]"
                    )

                # Report empty zoning strings
                empty_zoning_count = (~non_empty_zoning).sum()
                if empty_zoning_count > 0:
                    print(
                        f"Warning: Found {empty_zoning_count} vacant properties with empty zoning values"
                    )

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print comprehensive statistical summary of the vacant properties data."""
        self._print_summary_header("Vacant Properties Statistical Summary", gdf)

        # Vacant vs non-vacant distribution
        if "vacant" in gdf.columns:
            vacant_count = gdf["vacant"].sum()
            non_vacant_count = (~gdf["vacant"]).sum()
            vacant_percentage = (vacant_count / len(gdf)) * 100
            print("\nVacant Property Distribution:")
            print(f"  Vacant: {vacant_count:,} ({vacant_percentage:.1f}%)")
            print(
                f"  Non-vacant: {non_vacant_count:,} ({100 - vacant_percentage:.1f}%)"
            )

        # Parcel type distribution
        if "parcel_type" in gdf.columns:
            parcel_dist = gdf["parcel_type"].value_counts()
            print("\nParcel Type Distribution:")
            for ptype, count in parcel_dist.items():
                pct = (count / len(gdf)) * 100
                print(f"  {ptype}: {count:,} ({pct:.1f}%)")

        # Vacant property parcel type distribution
        if "vacant" in gdf.columns and "parcel_type" in gdf.columns:
            vacant_properties = gdf[gdf["vacant"]]
            if len(vacant_properties) > 0:
                vacant_parcel_dist = vacant_properties["parcel_type"].value_counts()
                print("\nVacant Properties by Parcel Type:")
                for ptype, count in vacant_parcel_dist.items():
                    pct = (count / len(vacant_properties)) * 100
                    print(f"  {ptype}: {count:,} ({pct:.1f}%)")

        # ZIP code and zoning counts
        if "zip_code" in gdf.columns:
            print(f"\nUnique ZIP codes: {gdf['zip_code'].nunique()}")
            if "vacant" in gdf.columns:
                vacant_properties = gdf[gdf["vacant"]]
                if len(vacant_properties) > 0:
                    print(
                        f"Unique ZIP codes (vacant properties): {vacant_properties['zip_code'].nunique()}"
                    )

        if "zoning" in gdf.columns:
            non_empty_zoning = gdf["zoning"].str.strip().ne("")
            print(
                f"Unique zoning classifications: {gdf.loc[non_empty_zoning, 'zoning'].nunique()}"
            )
            print(f"Properties with empty zoning: {(~non_empty_zoning).sum():,}")

            if "vacant" in gdf.columns:
                vacant_properties = gdf[gdf["vacant"]]
                if len(vacant_properties) > 0:
                    vacant_non_empty_zoning = (
                        vacant_properties["zoning"].str.strip().ne("")
                    )
                    print(
                        f"Vacant properties with empty zoning: {(~vacant_non_empty_zoning).sum():,}"
                    )

        # Financial statistics
        if "market_value" in gdf.columns:
            mv_stats = gdf["market_value"].describe()
            print("\nMarket Value Statistics (All Properties):")
            print(f"  Mean: ${mv_stats['mean']:,.0f}")
            print(f"  Median: ${mv_stats['50%']:,.0f}")
            print(f"  Std Dev: ${mv_stats['std']:,.0f}")
            print(f"  Q1: ${mv_stats['25%']:,.0f}")
            print(f"  Q3: ${mv_stats['75%']:,.0f}")
            print(f"  Max: ${mv_stats['max']:,.0f}")

            # Compare vacant vs non-vacant
            if "vacant" in gdf.columns:
                vacant_properties = gdf[gdf["vacant"]]
                non_vacant_properties = gdf[~gdf["vacant"]]

                if len(vacant_properties) > 0:
                    vacant_mv_stats = vacant_properties["market_value"].describe()
                    print("\nMarket Value Statistics (Vacant Properties):")
                    print(f"  Mean: ${vacant_mv_stats['mean']:,.0f}")
                    print(f"  Median: ${vacant_mv_stats['50%']:,.0f}")
                    print(f"  Std Dev: ${vacant_mv_stats['std']:,.0f}")

                if len(non_vacant_properties) > 0:
                    non_vacant_mv_stats = non_vacant_properties[
                        "market_value"
                    ].describe()
                    print("\nMarket Value Statistics (Non-Vacant Properties):")
                    print(f"  Mean: ${non_vacant_mv_stats['mean']:,.0f}")
                    print(f"  Median: ${non_vacant_mv_stats['50%']:,.0f}")
                    print(f"  Std Dev: ${non_vacant_mv_stats['std']:,.0f}")

        if "sale_price" in gdf.columns:
            sale_non_null = gdf["sale_price"].dropna()
            if len(sale_non_null) > 0:
                sale_stats = sale_non_null.describe()
                non_null_pct = (len(sale_non_null) / len(gdf)) * 100
                print(f"\nSale Price Statistics (non-null: {non_null_pct:.2f}%):")
                print(f"  Mean: ${sale_stats['mean']:,.0f}")
                print(f"  Median: ${sale_stats['50%']:,.0f}")
                print(f"  Std Dev: ${sale_stats['std']:,.0f}")
                print(f"  Q1: ${sale_stats['25%']:,.0f}")
                print(f"  Q3: ${sale_stats['75%']:,.0f}")
                print(f"  Max: ${sale_stats['max']:,.0f}")

        # Address uniqueness
        if "standardized_street_address" in gdf.columns:
            unique_addresses = gdf["standardized_street_address"].nunique()
            print(f"\nUnique standardized addresses: {unique_addresses:,}")

        self._print_summary_footer()

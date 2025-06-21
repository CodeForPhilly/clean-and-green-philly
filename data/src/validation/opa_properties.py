from datetime import datetime

import geopandas as gpd
import pandas as pd
import pandera.pandas as pa

from .base import BaseValidator

# Define the OPA Properties DataFrame Schema
OPAPropertiesSchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # Geographic fields
        "zip_code": pa.Column(
            str, nullable=False, description="ZIP code of the property"
        ),
        "zoning": pa.Column(str, nullable=False, description="Zoning classification"),
        # Property classification
        "parcel_type": pa.Column(
            str,
            pa.Check.isin(["Land", "Building"]),
            nullable=False,
            description="Property type classification",
        ),
        # Address fields
        "standardized_street_address": pa.Column(
            str, nullable=False, description="Standardized street address"
        ),
        "standardized_mailing_address": pa.Column(
            str, nullable=False, description="Standardized mailing address"
        ),
        # Financial fields
        "market_value": pa.Column(
            float,
            pa.Check.greater_than_or_equal_to(0),
            nullable=False,
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
        # Additional fields that may be present
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


class OPAPropertiesInputValidator(BaseValidator):
    """Validator for opa properties service input."""

    schema = None  # No schema validation for input

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class OPAPropertiesOutputValidator(BaseValidator):
    """Validator for opa properties service output with comprehensive statistical validation."""

    schema = OPAPropertiesSchema

    def _row_level_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Row-level validation that works with any dataset size."""

        # Call parent class method to get empty dataframe check
        super()._row_level_validation(gdf, errors)

        # Check for future sale dates (row-level check)
        if "sale_date" in gdf.columns:
            sale_dates = gdf["sale_date"].dropna()
            if len(sale_dates) > 0:
                # Convert to timezone-naive for comparison if needed
                if sale_dates.dt.tz is not None:
                    sale_dates = sale_dates.dt.tz_localize(None)

                # Check for future dates
                future_dates = sale_dates > pd.Timestamp.now()
                future_count = future_dates.sum()
                if future_count > 0:
                    errors.append(
                        f"Found {future_count} properties with sale dates in the future"
                    )

    def _statistical_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Statistical validation that requires larger datasets."""

        # 1. ZIP code validation - between 50 and 60 unique values
        if "zip_code" in gdf.columns:
            unique_zip_count = gdf["zip_code"].nunique()
            if not (50 <= unique_zip_count <= 60):
                errors.append(
                    f"ZIP code unique count ({unique_zip_count}) outside expected range [50, 60]"
                )

        # 2. Zoning validation - between 40 and 50 unique values, handle empty strings
        if "zoning" in gdf.columns:
            # Count non-empty zoning values
            non_empty_zoning = gdf["zoning"].str.strip().ne("")
            unique_zoning_count = gdf.loc[non_empty_zoning, "zoning"].nunique()

            if not (40 <= unique_zoning_count <= 50):
                errors.append(
                    f"Zoning unique count ({unique_zoning_count}) outside expected range [40, 50]"
                )

            # Report empty zoning strings
            empty_zoning_count = (~non_empty_zoning).sum()
            if empty_zoning_count > 0:
                print(
                    f"Warning: Found {empty_zoning_count} properties with empty zoning values"
                )

        # 3. Parcel type distribution validation
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

        # 4. Standardized address uniqueness validation
        if "standardized_street_address" in gdf.columns:
            unique_address_count = gdf["standardized_street_address"].nunique()
            if unique_address_count < 450000:
                errors.append(
                    f"Unique standardized addresses ({unique_address_count}) below expected minimum (450000)"
                )

        # 5. Market value statistical validation
        if "market_value" in gdf.columns:
            market_stats = gdf["market_value"].describe()

            # Check maximum value
            if market_stats["max"] > 500000000:  # 500M
                errors.append(
                    f"Market value maximum ({market_stats['max']:,.0f}) exceeds reasonable threshold"
                )

            # Check mean value (should be around 395,531)
            mean_value = market_stats["mean"]
            if not (300000 <= mean_value <= 500000):
                errors.append(
                    f"Market value mean ({mean_value:,.0f}) outside expected range [300000, 500000]"
                )

            # Check standard deviation (should be around 3,080,696)
            std_value = market_stats["std"]
            if not (2000000 <= std_value <= 4000000):
                errors.append(
                    f"Market value std ({std_value:,.0f}) outside expected range [2000000, 4000000]"
                )

        # 6. Sale price statistical validation
        if "sale_price" in gdf.columns:
            # Check non-null percentage (should be around 99.71%)
            non_null_pct = (gdf["sale_price"].notna().sum() / len(gdf)) * 100
            if not (99.0 <= non_null_pct <= 100.0):
                errors.append(
                    f"Sale price non-null percentage ({non_null_pct:.2f}%) outside expected range [99.0, 100.0]"
                )

            # Only validate statistics for non-null values
            sale_price_non_null = gdf["sale_price"].dropna()
            if len(sale_price_non_null) > 0:
                sale_stats = sale_price_non_null.describe()

                # Check maximum value
                if sale_stats["max"] > 1000000000:  # 1B
                    errors.append(
                        f"Sale price maximum ({sale_stats['max']:,.0f}) exceeds reasonable threshold"
                    )

                # Check mean value (should be around 315,032)
                mean_sale = sale_stats["mean"]
                if not (250000 <= mean_sale <= 400000):
                    errors.append(
                        f"Sale price mean ({mean_sale:,.0f}) outside expected range [250000, 400000]"
                    )

        # 7. Sale date validation - flag extreme dates
        if "sale_date" in gdf.columns:
            sale_dates = gdf["sale_date"].dropna()
            if len(sale_dates) > 0:
                # Convert to timezone-naive for comparison if needed
                if sale_dates.dt.tz is not None:
                    sale_dates = sale_dates.dt.tz_localize(None)

                # Check for dates before 1700 (historic properties)
                historic_dates = sale_dates < pd.Timestamp("1700-01-01")
                historic_count = historic_dates.sum()
                if historic_count > 0:
                    print(
                        f"Warning: Found {historic_count} properties with sale dates before 1700 (historic properties)"
                    )

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print comprehensive statistical summary of the OPA properties data."""
        self._print_summary_header("OPA Properties Statistical Summary", gdf)

        # Parcel type distribution
        if "parcel_type" in gdf.columns:
            parcel_dist = gdf["parcel_type"].value_counts()
            print("\nParcel Type Distribution:")
            for ptype, count in parcel_dist.items():
                pct = (count / len(gdf)) * 100
                print(f"  {ptype}: {count:,} ({pct:.1f}%)")

        # ZIP code and zoning counts
        if "zip_code" in gdf.columns:
            print(f"\nUnique ZIP codes: {gdf['zip_code'].nunique()}")

        if "zoning" in gdf.columns:
            non_empty_zoning = gdf["zoning"].str.strip().ne("")
            print(
                f"Unique zoning classifications: {gdf.loc[non_empty_zoning, 'zoning'].nunique()}"
            )
            print(f"Properties with empty zoning: {(~non_empty_zoning).sum():,}")

        # Financial statistics
        if "market_value" in gdf.columns:
            mv_stats = gdf["market_value"].describe()
            print("\nMarket Value Statistics:")
            print(f"  Mean: ${mv_stats['mean']:,.0f}")
            print(f"  Median: ${mv_stats['50%']:,.0f}")
            print(f"  Std Dev: ${mv_stats['std']:,.0f}")
            print(f"  Q1: ${mv_stats['25%']:,.0f}")
            print(f"  Q3: ${mv_stats['75%']:,.0f}")
            print(f"  Max: ${mv_stats['max']:,.0f}")

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

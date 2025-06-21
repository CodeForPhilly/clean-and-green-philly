import geopandas as gpd
import pandera.pandas as pa

from .base import BaseValidator

# Define the Council Districts DataFrame Schema
CouncilDistrictsSchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # Council district - must be string with no NAs, values 1-10
        "district": pa.Column(
            str,
            pa.Check.isin(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]),
            nullable=False,
            description="Council district identifier (1-10)",
        ),
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=False,
    coerce=True,
)


class CouncilDistrictsInputValidator(BaseValidator):
    """Validator for council districts service input."""

    schema = None  # No schema validation for input

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        pass


class CouncilDistrictsOutputValidator(BaseValidator):
    """Validator for council districts service output with statistical validation."""

    schema = CouncilDistrictsSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        """
        Custom validation beyond the basic schema constraints.

        Args:
            gdf: GeoDataFrame to validate
            check_stats: Whether to run statistical checks (skip for unit tests with small data)
        """
        # District count validation - should be exactly 10 unique values
        if check_stats and "district" in gdf.columns:
            unique_district_count = gdf["district"].nunique()
            if unique_district_count != 10:
                self.errors.append(
                    f"District unique count ({unique_district_count}) should be exactly 10"
                )

        # Only run statistical checks if requested and data is large enough
        if check_stats and len(gdf) > 100:
            self._statistical_validation(gdf)
            self._print_statistical_summary(gdf)

    def _statistical_validation(self, gdf: gpd.GeoDataFrame):
        """Statistical validation that requires larger datasets."""
        # No additional statistical validation needed - district count is handled in _custom_validation
        pass

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print statistical summary of the council districts data."""
        print("\n=== Council Districts Statistical Summary ===")
        print(f"Total properties: {len(gdf):,}")

        # District distribution
        if "district" in gdf.columns:
            district_dist = gdf["district"].value_counts().sort_index()
            print("\nDistrict Distribution:")
            for district, count in district_dist.items():
                pct = (count / len(gdf)) * 100
                print(f"  District {district}: {count:,} ({pct:.1f}%)")

            # Unique district count
            unique_district_count = gdf["district"].nunique()
            print(f"Unique districts: {unique_district_count}")

            # Print the actual district values
            unique_districts = gdf["district"].dropna().unique()
            print(f"District values: {sorted(unique_districts)}")

        print("=" * 50)

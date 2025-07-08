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

CouncilDistrictsInputSchema = pa.DataFrameSchema(
    columns={
        "district": pa.Column(
            str,
            nullable=True,
        ),
        "geometry": pa.Column("geometry"),
    },
    # district should contain 10 records of strings 1-10
    checks=pa.Check(
        lambda df: set(df["district"].dropna().unique())
        == {str(i) for i in range(1, 11)}
    ),
    strict=False,
)


class CouncilDistrictsInputValidator(BaseValidator):
    """Validator for council districts service input."""

    schema = CouncilDistrictsInputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        pass


class CouncilDistrictsOutputValidator(BaseValidator):
    """Validator for council districts service output with statistical validation."""

    schema = CouncilDistrictsSchema

    def _row_level_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Row-level validation that works with any dataset size."""
        # Call parent class method to get empty dataframe check
        super()._row_level_validation(gdf, errors)
        # No additional row-level validation needed for council districts

    def _statistical_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Statistical validation that requires larger datasets."""
        # District count validation - should be exactly 10 unique values
        if "district" in gdf.columns:
            self._validate_unique_count(gdf, "district", errors, expected_count=10)

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print statistical summary of the council districts data."""
        self._print_summary_header("Council Districts Statistical Summary", gdf)

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

        self._print_summary_footer()

import geopandas as gpd
import pandera.pandas as pa

from .base import BaseValidator

# Define the Neighborhoods DataFrame Schema
NeighborhoodsSchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # Neighborhood - must be string with no NAs
        "neighborhood": pa.Column(str, nullable=False, description="Neighborhood name"),
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=True,
    coerce=False,
)


class NeighborhoodsInputValidator(BaseValidator):
    """Validator for neighborhoods service input."""

    schema = None  # No schema validation for input

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class NeighborhoodsOutputValidator(BaseValidator):
    """Validator for neighborhoods service output with statistical validation."""

    schema = NeighborhoodsSchema

    def _row_level_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Row-level validation that works with any dataset size."""
        # Call parent class method to get empty dataframe check
        super()._row_level_validation(gdf, errors)
        # No additional row-level validation needed for neighborhoods

    def _statistical_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Statistical validation that requires larger datasets."""
        # Neighborhood count validation - should be around 160 unique values
        if "neighborhood" in gdf.columns:
            self._validate_unique_count(
                gdf, "neighborhood", errors, min_count=150, max_count=170
            )

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print statistical summary of the neighborhoods data."""
        self._print_summary_header("Neighborhoods Statistical Summary", gdf)

        # Neighborhood distribution
        if "neighborhood" in gdf.columns:
            neighborhood_dist = gdf["neighborhood"].value_counts().sort_index()
            print("\nNeighborhood Distribution (Top 20):")
            for neighborhood, count in neighborhood_dist.head(20).items():
                pct = (count / len(gdf)) * 100
                print(f"  {neighborhood}: {count:,} ({pct:.1f}%)")

            # Unique neighborhood count
            unique_neighborhood_count = gdf["neighborhood"].nunique()
            print(f"\nUnique neighborhoods: {unique_neighborhood_count}")

            # Show total number of neighborhoods if more than 20
            if len(neighborhood_dist) > 20:
                print(f"Total neighborhoods: {len(neighborhood_dist)}")

        self._print_summary_footer()

import geopandas as gpd
import pandera.pandas as pa

from .base import BaseValidator

# Define the City Owned Properties DataFrame Schema
CityOwnedPropertiesSchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # City owner agency - must be string, can be nullable
        "city_owner_agency": pa.Column(
            str, nullable=True, description="The agency that owns the city property"
        ),
        # Side yard eligible flag - must be boolean, can be nullable
        "side_yard_eligible": pa.Column(
            bool,
            nullable=True,
            description="Indicates if the property is eligible for the side yard program",
        ),
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=False,
    coerce=True,
)

# Expecting ~7,796 records returned (within ±20% tolerance).
# This is checked in CityOwnedPropertiesInputSchema
expected = 7796
lower = int(expected * 0.8)
upper = int(expected * 1.2)

CityOwnedPropertiesInputSchema = pa.DataFrameSchema(
    columns={
        "opa_id": pa.Column(pa.Int, checks=pa.Check(lambda s: s.dropna() != "")),
        "agency": pa.Column(pa.String, nullable=True),
        "sideyardeligible": pa.Column(
            pa.Category, nullable=True, checks=pa.Check.isin(["Yes", "No"])
        ),
        "geometry": pa.Column("geometry"),
    },
    checks=pa.Check(lambda df: lower <= df.shape[0] <= upper),
    strict=True,
)


class CityOwnedPropertiesInputValidator(BaseValidator):
    """
    Validator for the city-owned properties dataset input.
    schema and _custom_validation() are used by validate() in the parent class.
    """

    schema = CityOwnedPropertiesInputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class CityOwnedPropertiesOutputValidator(BaseValidator):
    """
    Validator for the city-owned properties dataset output.
    schema and _custom_validation() are used by validate() in the parent class.
    """

    schema = CityOwnedPropertiesSchema

    def _row_level_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Row-level validation that works with any dataset size."""

        # Call parent class method to get empty dataframe check
        super()._row_level_validation(gdf, errors)

        # Check for required columns using helper method
        required_columns = ["opa_id", "city_owner_agency", "side_yard_eligible"]
        self._validate_required_columns(gdf, required_columns, errors)

        # Only proceed with column-specific validation if all required columns are present
        if all(col in gdf.columns for col in required_columns):
            # Validate city_owner_agency column
            # Check for non-string values (excluding nulls)
            non_null_agency = gdf["city_owner_agency"].dropna()
            if len(non_null_agency) > 0:
                non_string_agency = (
                    ~non_null_agency.apply(lambda x: isinstance(x, str))
                ).sum()
                if non_string_agency > 0:
                    errors.append(
                        f"Found {non_string_agency} non-string values in 'city_owner_agency' column"
                    )

            # Validate side_yard_eligible column
            # Check for non-boolean values (excluding nulls)
            non_null_eligible = gdf["side_yard_eligible"].dropna()
            if len(non_null_eligible) > 0:
                non_bool_eligible = (
                    ~non_null_eligible.apply(lambda x: isinstance(x, bool))
                ).sum()
                if non_bool_eligible > 0:
                    errors.append(
                        f"Found {non_bool_eligible} non-boolean values in 'side_yard_eligible' column"
                    )

    def _statistical_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Statistical validation that requires larger datasets."""

        # Only run statistical validation for datasets with sufficient size
        if len(gdf) < self.min_stats_threshold:
            return

        # 1. City owner agency distribution validation
        if "city_owner_agency" in gdf.columns:
            non_null_agency = gdf["city_owner_agency"].dropna()
            if len(non_null_agency) > 0:
                agency_counts = non_null_agency.value_counts()

                # Check for reasonable number of unique agencies (should be between 5 and 20)
                unique_agency_count = len(agency_counts)
                if not (5 <= unique_agency_count <= 20):
                    errors.append(
                        f"City owner agency unique count ({unique_agency_count}) outside expected range [5, 20]"
                    )

                # Check that most common agencies are reasonable
                most_common_agency = agency_counts.index[0]
                most_common_count = agency_counts.iloc[0]
                total_city_owned = len(non_null_agency)

                # Most common agency should not be more than 80% of all city-owned properties
                if most_common_count / total_city_owned > 0.8:
                    errors.append(
                        f"Most common city owner agency '{most_common_agency}' represents {most_common_count / total_city_owned * 100:.1f}% of all city-owned properties (exceeds 80%)"
                    )

        # 2. Side yard eligible validation
        if "side_yard_eligible" in gdf.columns:
            non_null_eligible = gdf["side_yard_eligible"].dropna()
            if len(non_null_eligible) > 0:
                eligible_count = non_null_eligible.sum()
                total_eligible_properties = len(non_null_eligible)

                # Side yard eligible should not be more than 50% of city-owned properties
                if eligible_count / total_eligible_properties > 0.5:
                    errors.append(
                        f"Side yard eligible properties ({eligible_count}/{total_eligible_properties}) exceed 50% of city-owned properties"
                    )

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print comprehensive statistical summary of the city owned properties data."""
        self._print_summary_header("City Owned Properties Statistical Summary", gdf)

        # City owner agency distribution
        if "city_owner_agency" in gdf.columns:
            non_null_agency = gdf["city_owner_agency"].dropna()
            if len(non_null_agency) > 0:
                agency_dist = non_null_agency.value_counts()
                print("\nCity Owner Agency Distribution:")
                for agency, count in agency_dist.items():
                    pct = (count / len(non_null_agency)) * 100
                    print(f"  {agency}: {count:,} ({pct:.1f}%)")

                print(f"\nTotal city-owned properties: {len(non_null_agency):,}")
                print(f"Unique agencies: {len(agency_dist)}")
            else:
                print("\nNo city-owned properties found in dataset")

        # Side yard eligible statistics
        if "side_yard_eligible" in gdf.columns:
            non_null_eligible = gdf["side_yard_eligible"].dropna()
            if len(non_null_eligible) > 0:
                eligible_count = non_null_eligible.sum()
                total_eligible_properties = len(non_null_eligible)
                eligible_pct = (eligible_count / total_eligible_properties) * 100

                print("\nSide Yard Eligible Statistics:")
                print(
                    f"  Eligible properties: {eligible_count:,} ({eligible_pct:.1f}%)"
                )
                print(
                    f"  Non-eligible properties: {total_eligible_properties - eligible_count:,}"
                )
                print(
                    f"  Total properties with eligibility data: {total_eligible_properties:,}"
                )

        self._print_summary_footer()

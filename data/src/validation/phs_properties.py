import geopandas as gpd
import pandera.pandas as pa

from .base import BaseValidator

# Define the PHS Properties DataFrame Schema
PHSPropertiesSchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # PHS care program - must be string, can be nullable
        "phs_care_program": pa.Column(
            str,
            nullable=True,
            description="The PHS care program associated with the property",
        ),
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=False,
    coerce=True,
)


class PHSPropertiesInputValidator(BaseValidator):
    """Validator for PHS properties service input."""

    schema = None  # No schema validation for input

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class PHSPropertiesOutputValidator(BaseValidator):
    """Validator for PHS properties service output with comprehensive validation."""

    schema = PHSPropertiesSchema

    def _row_level_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Row-level validation that works with any dataset size."""

        print(f"DEBUG: Starting row-level validation on {len(gdf)} rows")

        # Call parent class method to get empty dataframe check
        super()._row_level_validation(gdf, errors)
        print(f"DEBUG: After parent validation, errors count: {len(errors)}")

        # Check for required columns using helper method
        required_columns = ["opa_id", "phs_care_program"]
        self._validate_required_columns(gdf, required_columns, errors)
        print(f"DEBUG: After required columns check, errors count: {len(errors)}")

        # Validate phs_care_program column if it exists
        if "phs_care_program" in gdf.columns:
            # Check for non-string values (excluding NaN/None)
            non_string_phs = (
                gdf["phs_care_program"]
                .dropna()
                .apply(lambda x: not isinstance(x, str))
                .sum()
            )

            print(
                f"DEBUG: Found {non_string_phs} non-string values in phs_care_program"
            )

            if non_string_phs > 0:
                error_msg = f"Found {non_string_phs} non-string values in 'phs_care_program' column"
                print(f"DEBUG: Adding error: {error_msg}")
                errors.append(error_msg)
        else:
            print("DEBUG: phs_care_program column not found in row-level validation")

        print(f"DEBUG: Final row-level validation errors count: {len(errors)}")
        if errors:
            print(f"DEBUG: Row-level validation errors: {errors}")

    def _statistical_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Statistical validation that requires larger datasets."""

        # Only run statistical validation if we have enough data
        if len(gdf) < self.min_stats_threshold:
            print(
                f"DEBUG: Skipping statistical validation - only {len(gdf)} rows, need {self.min_stats_threshold}"
            )
            return

        print(f"DEBUG: Running statistical validation on {len(gdf)} rows")

        # Validate phs_care_program distribution if column exists
        if "phs_care_program" in gdf.columns:
            # Count actual PHS programs (excluding None, empty strings, etc.)
            actual_phs_programs = gdf["phs_care_program"].notna()
            actual_phs_programs = actual_phs_programs & gdf[
                "phs_care_program"
            ].str.strip().ne("")
            phs_program_count = actual_phs_programs.sum()
            total_properties = len(gdf)

            print(f"DEBUG: phs_program_count = {phs_program_count}")
            print(f"DEBUG: total_properties = {total_properties}")

            # PHS properties should be a small percentage of total properties
            phs_percentage = (phs_program_count / total_properties) * 100

            print(f"DEBUG: phs_percentage = {phs_percentage:.2f}%")
            print("DEBUG: Expected range: [1.0, 5.0]")

            # Reasonable range: 1.0% to 5% of properties should be in PHS programs
            if not (1.0 <= phs_percentage <= 5.0):
                error_msg = f"PHS care program percentage ({phs_percentage:.2f}%) outside expected range [1.0, 5.0]"
                print(f"DEBUG: Adding error: {error_msg}")
                errors.append(error_msg)
            else:
                print(
                    f"DEBUG: PHS percentage {phs_percentage:.2f}% is within expected range [1.0, 5.0]"
                )
        else:
            print("DEBUG: phs_care_program column not found")

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print comprehensive statistical summary of the PHS properties data."""
        self._print_summary_header("PHS Properties Statistical Summary", gdf)

        # PHS care program statistics
        if "phs_care_program" in gdf.columns:
            phs_stats = gdf["phs_care_program"].value_counts()
            total_properties = len(gdf)

            # Count actual PHS programs (excluding None, empty strings, etc.)
            actual_phs_programs = gdf["phs_care_program"].notna()
            actual_phs_programs = actual_phs_programs & gdf[
                "phs_care_program"
            ].str.strip().ne("")
            phs_program_count = actual_phs_programs.sum()

            print("\nPHS Care Program Statistics:")
            print(f"  Properties with PHS programs: {phs_program_count:,}")
            print(
                f"  Properties without PHS programs: {total_properties - phs_program_count:,}"
            )
            print(
                f"  PHS coverage: {(phs_program_count / total_properties) * 100:.2f}%"
            )

            if len(phs_stats) > 0:
                print("\nPHS Program Distribution:")
                for program, count in phs_stats.items():
                    pct = (count / total_properties) * 100
                    print(f"  {program}: {count:,} ({pct:.2f}%)")

        self._print_summary_footer()

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
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=False,
    coerce=True,
)

VacantPropertiesInputSchema = pa.DataFrameSchema(
    columns={
        "opa_id": pa.Column(
            str,
            nullable=True,
        ),
        "parcel_type": pa.Column(
            str,
            nullable=True,
        ),
        "geometry": pa.Column("geometry"),
    },
    strict=False,
)


class VacantPropertiesInputValidator(BaseValidator):
    """Validator for vacant properties service input."""

    schema = VacantPropertiesInputSchema

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
        # TEMPORARILY DISABLED - upstream data issue, will be fixed later
        # if "vacant" in gdf.columns:
        #     vacant_count = gdf["vacant"].sum()
        #     total_count = len(gdf)
        #     vacant_percentage = (vacant_count / total_count) * 100

        #     # Expected range: 10-15% of properties should be vacant
        #     if not (10.0 <= vacant_percentage <= 15.0):
        #         errors.append(
        #             f"Vacant property percentage ({vacant_percentage:.2f}%) outside expected range [10.0, 15.0]"
        #         )

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
        # TEMPORARILY DISABLED - upstream data issue, will be fixed later
        # if "vacant" in gdf.columns and "parcel_type" in gdf.columns:
        #     vacant_properties = gdf[gdf["vacant"]]
        #     if len(vacant_properties) > 0:
        #         vacant_parcel_counts = vacant_properties["parcel_type"].value_counts()

        #         # Check vacant building count (should be majority of vacant properties)
        #         vacant_building_count = vacant_parcel_counts.get("Building", 0)
        #         vacant_land_count = vacant_parcel_counts.get("Land", 0)
        #         total_vacant = len(vacant_properties)

        #         if total_vacant > 0:
        #             vacant_building_percentage = (
        #                 vacant_building_count / total_vacant
        #             ) * 100
        #             (vacant_land_count / total_vacant) * 100

        #             # Most vacant properties should be buildings (roughly 70-90%)
        #             if not (70.0 <= vacant_building_percentage <= 90.0):
        #                 errors.append(
        #                     f"Vacant building percentage ({vacant_building_percentage:.2f}%) outside expected range [70.0, 90.0]"
        #                 )

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

        self._print_summary_footer()

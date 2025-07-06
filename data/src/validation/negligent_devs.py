import geopandas as gpd
import pandera.pandas as pa

from .base import BaseValidator


class NegligentDevsOutputValidator(BaseValidator):
    """Validator for negligent devs service output."""

    @property
    def schema(self):
        """Return schema with conditional statistical validation."""
        # Base schema without statistical checks
        base_schema = pa.DataFrameSchema(
            {
                # Core identifier - must be unique string with no NAs
                "opa_id": pa.Column(
                    str,
                    unique=True,
                    nullable=False,
                    description="OPA property identifier",
                ),
                # Negligent developer flag
                "negligent_dev": pa.Column(
                    bool, nullable=False, description="Flag for negligent developers"
                ),
                # Total properties owned by the developer
                "n_total_properties_owned": pa.Column(
                    int,
                    nullable=False,
                    checks=[
                        pa.Check(
                            lambda s: s >= 0,
                            error="n_total_properties_owned cannot be negative",
                        ),
                    ],
                    description="Total number of properties owned by the developer",
                ),
                # Vacant properties owned by the developer
                "n_vacant_properties_owned": pa.Column(
                    int,
                    nullable=False,
                    checks=[
                        pa.Check(
                            lambda s: s >= 0,
                            error="n_vacant_properties_owned cannot be negative",
                        ),
                    ],
                    description="Number of vacant properties owned by the developer",
                ),
                # Average violations per property
                "avg_violations_per_property": pa.Column(
                    float,
                    nullable=False,
                    checks=[
                        pa.Check(
                            lambda s: s >= 0,
                            error="avg_violations_per_property cannot be negative",
                        ),
                    ],
                    description="Average violations per property for the developer",
                ),
                # Geometry field - using Pandera's GeoPandas integration
                "geometry": pa.Column(
                    "geometry", nullable=False, description="Property geometry"
                ),
            },
            strict=False,
        )
        return base_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        """Custom validation for negligent devs data."""
        errors = []

        # Business logic validation (always runs)
        if (
            "n_vacant_properties_owned" in gdf.columns
            and "n_total_properties_owned" in gdf.columns
        ):
            # Check that vacant properties <= total properties
            invalid_mask = (
                gdf["n_vacant_properties_owned"] > gdf["n_total_properties_owned"]
            )
            if invalid_mask.any():
                invalid_count = invalid_mask.sum()
                errors.append(
                    f"Found {invalid_count} records where vacant properties > total properties"
                )

        # Only run statistical validation for large datasets when check_stats is True
        if check_stats and len(gdf) >= self.min_stats_threshold:
            # Statistical validation for n_total_properties_owned
            if "n_total_properties_owned" in gdf.columns:
                non_null_data = gdf["n_total_properties_owned"].dropna()
                if len(non_null_data) > 0:
                    max_val = non_null_data.max()
                    mean_val = non_null_data.mean()
                    std_val = non_null_data.std()
                    q1_val = non_null_data.quantile(0.25)
                    q3_val = non_null_data.quantile(0.75)

                    if max_val > 6000:
                        errors.append(
                            f"n_total_properties_owned maximum value ({max_val}) exceeds 6000"
                        )
                    if mean_val < 53.6 or mean_val > 80.3:
                        errors.append(
                            f"n_total_properties_owned mean ({mean_val:.2f}) outside expected range [53.6, 80.3]"
                        )
                    if std_val < 393.3 or std_val > 589.9:
                        errors.append(
                            f"n_total_properties_owned standard deviation ({std_val:.2f}) outside expected range [393.3, 589.9]"
                        )
                    if q1_val < 0.8 or q1_val > 1.2:
                        errors.append(
                            f"n_total_properties_owned Q1 ({q1_val:.2f}) outside expected range [0.8, 1.2]"
                        )
                    if q3_val < 0.8 or q3_val > 1.2:
                        errors.append(
                            f"n_total_properties_owned Q3 ({q3_val:.2f}) outside expected range [0.8, 1.2]"
                        )

            # Statistical validation for n_vacant_properties_owned
            if "n_vacant_properties_owned" in gdf.columns:
                non_null_data = gdf["n_vacant_properties_owned"].dropna()
                if len(non_null_data) > 0:
                    max_val = non_null_data.max()
                    mean_val = non_null_data.mean()
                    std_val = non_null_data.std()
                    q1_val = non_null_data.quantile(0.25)
                    q3_val = non_null_data.quantile(0.75)

                    if max_val > 1300:
                        errors.append(
                            f"n_vacant_properties_owned maximum value ({max_val}) exceeds 1300"
                        )
                    if mean_val < 15.1 or mean_val > 22.6:
                        errors.append(
                            f"n_vacant_properties_owned mean ({mean_val:.2f}) outside expected range [15.1, 22.6]"
                        )
                    if std_val < 104.4 or std_val > 156.5:
                        errors.append(
                            f"n_vacant_properties_owned standard deviation ({std_val:.2f}) outside expected range [104.4, 156.5]"
                        )
                    if q1_val < 0.0 or q1_val > 0.0:
                        errors.append(
                            f"n_vacant_properties_owned Q1 ({q1_val:.2f}) outside expected range [0.0, 0.0]"
                        )
                    if q3_val < 0.0 or q3_val > 0.0:
                        errors.append(
                            f"n_vacant_properties_owned Q3 ({q3_val:.2f}) outside expected range [0.0, 0.0]"
                        )

            # Statistical validation for avg_violations_per_property
            if "avg_violations_per_property" in gdf.columns:
                non_null_data = gdf["avg_violations_per_property"].dropna()
                if len(non_null_data) > 0:
                    max_val = non_null_data.max()
                    mean_val = non_null_data.mean()
                    std_val = non_null_data.std()
                    q1_val = non_null_data.quantile(0.25)
                    q3_val = non_null_data.quantile(0.75)

                    if max_val > 17.0:
                        errors.append(
                            f"avg_violations_per_property maximum value ({max_val}) exceeds 17.0"
                        )
                    if mean_val < 0.055 or mean_val > 0.083:
                        errors.append(
                            f"avg_violations_per_property mean ({mean_val:.4f}) outside expected range [0.055, 0.083]"
                        )
                    if std_val < 0.278 or std_val > 0.416:
                        errors.append(
                            f"avg_violations_per_property standard deviation ({std_val:.4f}) outside expected range [0.278, 0.416]"
                        )
                    if q1_val < 0.0 or q1_val > 0.0:
                        errors.append(
                            f"avg_violations_per_property Q1 ({q1_val:.4f}) outside expected range [0.0, 0.0]"
                        )
                    if q3_val < 0.0 or q3_val > 0.0:
                        errors.append(
                            f"avg_violations_per_property Q3 ({q3_val:.4f}) outside expected range [0.0, 0.0]"
                        )

        # Print actual statistics for debugging
        if "avg_violations_per_property" in gdf.columns:
            non_null_data = gdf["avg_violations_per_property"].dropna()
            if len(non_null_data) > 0:
                print("[DEBUG] negligent_devs validation: Actual statistics:")
                print(f"  Count: {len(non_null_data)}")
                print(f"  Min: {non_null_data.min()}")
                print(f"  Max: {non_null_data.max()}")
                print(f"  Mean: {non_null_data.mean()}")
                print(f"  Std: {non_null_data.std()}")
                print(f"  Q1: {non_null_data.quantile(0.25)}")
                print(f"  Q3: {non_null_data.quantile(0.75)}")
                print(f"  Sample values: {non_null_data.head(10).tolist()}")

        if "n_total_properties_owned" in gdf.columns:
            non_null_data = gdf["n_total_properties_owned"].dropna()
            if len(non_null_data) > 0:
                print(
                    "[DEBUG] negligent_devs validation: n_total_properties_owned statistics:"
                )
                print(f"  Count: {len(non_null_data)}")
                print(f"  Min: {non_null_data.min()}")
                print(f"  Max: {non_null_data.max()}")
                print(f"  Mean: {non_null_data.mean()}")
                print(f"  Std: {non_null_data.std()}")
                print(f"  Q1: {non_null_data.quantile(0.25)}")
                print(f"  Q3: {non_null_data.quantile(0.75)}")

        if "n_vacant_properties_owned" in gdf.columns:
            non_null_data = gdf["n_vacant_properties_owned"].dropna()
            if len(non_null_data) > 0:
                print(
                    "[DEBUG] negligent_devs validation: n_vacant_properties_owned statistics:"
                )
                print(f"  Count: {len(non_null_data)}")
                print(f"  Min: {non_null_data.min()}")
                print(f"  Max: {non_null_data.max()}")
                print(f"  Mean: {non_null_data.mean()}")
                print(f"  Std: {non_null_data.std()}")
                print(f"  Q1: {non_null_data.quantile(0.25)}")
                print(f"  Q3: {non_null_data.quantile(0.75)}")

        self.errors.extend(errors)

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print comprehensive statistical summary of the negligent devs data."""
        self._print_summary_header("Negligent Devs Statistical Summary", gdf)

        # Total record count
        total_records = len(gdf)
        print(f"\nTotal properties: {total_records:,}")

        # Coverage statistics for each column
        columns_to_check = [
            "negligent_dev",
            "n_total_properties_owned",
            "n_vacant_properties_owned",
            "avg_violations_per_property",
        ]

        print("\nColumn Coverage Statistics:")
        for col in columns_to_check:
            if col in gdf.columns:
                non_null_count = gdf[col].notna().sum()
                coverage_pct = (
                    (non_null_count / total_records) * 100 if total_records > 0 else 0
                )
                print(f"  {col}: {non_null_count:,} ({coverage_pct:.1f}%)")

        # Statistical summaries for numeric columns
        numeric_columns = [
            "n_total_properties_owned",
            "n_vacant_properties_owned",
            "avg_violations_per_property",
        ]
        for col in numeric_columns:
            if col in gdf.columns:
                non_null_data = gdf[col].dropna()
                if len(non_null_data) > 0:
                    stats = non_null_data.describe()
                    print(f"\n{col} statistics (non-null values):")
                    print(f"  Mean: {stats['mean']:.4f}")
                    print(f"  Std:  {stats['std']:.4f}")
                    print(f"  Min:  {stats['min']:.4f}")
                    print(f"  Max:  {stats['max']:.4f}")
                    print(f"  Q1:   {stats['25%']:.4f}")
                    print(f"  Q3:   {stats['75%']:.4f}")
                else:
                    print(f"\n{col}: No valid data found")

        # Boolean column summary
        if "negligent_dev" in gdf.columns:
            value_counts = gdf["negligent_dev"].value_counts()
            print("\nnegligent_dev distribution:")
            for value, count in value_counts.items():
                pct = (count / total_records) * 100
                print(f"  {value}: {count:,} ({pct:.1f}%)")

        self._print_summary_footer()

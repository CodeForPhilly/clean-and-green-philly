import geopandas as gpd

from .base import BaseValidator


class DrugCrimesOutputValidator(BaseValidator):
    """
    Validator for Drug Crime KDE outputs.

    Validates drug crime density calculations with application-specific ranges:
    - drug_crimes_density: typically very small values (e-10 to e-7 range)
    - drug_crimes_density_zscore: roughly normal distribution around 0, std ~1
    - drug_crimes_density_percentile: 0-100 range (validated by base class)
    """

    def _row_level_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Row-level validation for drug crime KDE outputs."""
        # Call parent class method to get empty dataframe check
        super()._row_level_validation(gdf, errors)

        # Check for required KDE columns with actual names
        required_columns = [
            "drug_crimes_density_label",
            "drug_crimes_density",
            "drug_crimes_density_zscore",
            "drug_crimes_density_percentile",
        ]
        self._validate_required_columns(gdf, required_columns, errors)

        # Validate density ranges (application-specific)
        self._validate_density_ranges(gdf, errors)

        # Validate application-specific requirements
        self._validate_application_specific(gdf, errors)

    def _statistical_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Statistical validation for drug crime KDE outputs."""
        # Check percentile distribution (should be roughly uniform 0-100)
        if "drug_crimes_density_percentile" in gdf.columns:
            percentiles = gdf["drug_crimes_density_percentile"]

            # Check that percentiles span a reasonable range
            min_percentile = percentiles.min()
            max_percentile = percentiles.max()

            if min_percentile < 0 or max_percentile > 100:
                errors.append(
                    f"Percentile values outside expected range [0, 100]: "
                    f"min={min_percentile:.2f}, max={max_percentile:.2f}"
                )

            # Check that we have a reasonable distribution (not all same value)
            unique_percentiles = percentiles.nunique()
            if unique_percentiles < 10:  # Arbitrary threshold
                errors.append(
                    f"Percentile distribution appears too narrow: "
                    f"only {unique_percentiles} unique values"
                )

    def _validate_density_ranges(self, gdf: gpd.GeoDataFrame, errors: list):
        """
        Validate drug crime density and zscore ranges.

        Based on actual observed statistics:
        - density: max ~2.78e-07, mean ~6.38e-10, std ~6.37e-09
        - zscore: max ~43.51, mean ~0, std ~1
        """
        # Validate density values (drug crime densities can be larger than gun crimes)
        if "drug_crimes_density" in gdf.columns:
            density = gdf["drug_crimes_density"]

            # Check for reasonable upper bound (allowing flexibility based on actual data)
            max_density = density.max()
            if max_density > 1e-6:  # Allow up to 1e-6 (higher than observed max)
                errors.append(
                    f"Drug crime density values appear too high: max={max_density:.2e} "
                    f"(expected < 1e-6)"
                )

            # Check for reasonable lower bound (should be non-negative)
            min_density = density.min()
            if min_density < 0:
                errors.append(
                    f"Drug crime density values should be non-negative: min={min_density:.2e}"
                )

            # Check for reasonable mean (should be in e-10 to e-9 range)
            mean_density = density.mean()
            if mean_density > 1e-7 or mean_density < 1e-12:
                errors.append(
                    f"Drug crime density mean appears outside expected range: "
                    f"mean={mean_density:.2e} (expected ~1e-10 to 1e-9)"
                )

        # Validate z-score values (should be roughly normal distribution)
        if "drug_crimes_density_zscore" in gdf.columns:
            zscore = gdf["drug_crimes_density_zscore"]

            # Check z-score mean (should be close to 0)
            mean_zscore = zscore.mean()
            if abs(mean_zscore) > 0.1:  # Allow some deviation from 0
                errors.append(
                    f"Drug crime z-score mean appears too far from 0: "
                    f"mean={mean_zscore:.4f} (expected ~0)"
                )

            # Check z-score standard deviation (should be close to 1)
            std_zscore = zscore.std()
            if std_zscore < 0.5 or std_zscore > 2.0:  # Allow reasonable range
                errors.append(
                    f"Drug crime z-score standard deviation appears outside expected range: "
                    f"std={std_zscore:.4f} (expected ~1.0)"
                )

            # Check for extreme outliers (z-scores beyond ±75 are suspicious, based on actual data)
            extreme_outliers = zscore[(zscore < -75) | (zscore > 75)]
            if len(extreme_outliers) > 0:
                errors.append(
                    f"Found {len(extreme_outliers)} extreme z-score outliers "
                    f"(beyond ±75): min={zscore.min():.2f}, max={zscore.max():.2f}"
                )

    def _validate_application_specific(self, gdf: gpd.GeoDataFrame, errors: list):
        """
        Validate drug crime-specific requirements.
        """
        # Check that we have a reasonable number of high-density areas
        if "drug_crimes_density_percentile" in gdf.columns:
            high_density_count = len(gdf[gdf["drug_crimes_density_percentile"] >= 90])
            total_count = len(gdf)

            # Expect roughly 10% of areas to be in top 10% (with some flexibility)
            expected_high_density = total_count * 0.1
            if (
                high_density_count < expected_high_density * 0.5
                or high_density_count > expected_high_density * 2.0
            ):
                errors.append(
                    f"Drug crime high-density areas (≥90th percentile) count appears unusual: "
                    f"{high_density_count} out of {total_count} ({high_density_count / total_count * 100:.1f}%) "
                    f"(expected ~10%)"
                )

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print drug crime KDE-specific statistical summary."""
        self._print_summary_header("Drug Crime KDE Output Statistics", gdf)

        if "drug_crimes_density" in gdf.columns:
            density_stats = gdf["drug_crimes_density"].describe()
            print("Drug Crime Density statistics:")
            print(f"  Mean: {density_stats['mean']:.4e}")
            print(f"  Std:  {density_stats['std']:.4e}")
            print(f"  Min:  {density_stats['min']:.4e}")
            print(f"  Max:  {density_stats['max']:.4e}")

        if "drug_crimes_density_zscore" in gdf.columns:
            zscore_stats = gdf["drug_crimes_density_zscore"].describe()
            print("Drug Crime Z-score statistics:")
            print(f"  Mean: {zscore_stats['mean']:.4f}")
            print(f"  Std:  {zscore_stats['std']:.4f}")
            print(f"  Min:  {zscore_stats['min']:.4f}")
            print(f"  Max:  {zscore_stats['max']:.4f}")

        if "drug_crimes_density_percentile" in gdf.columns:
            percentile_stats = gdf["drug_crimes_density_percentile"].describe()
            print("Drug Crime Percentile statistics:")
            print(f"  Mean: {percentile_stats['mean']:.2f}")
            print(f"  Std:  {percentile_stats['std']:.2f}")
            print(f"  Min:  {percentile_stats['min']:.2f}")
            print(f"  Max:  {percentile_stats['max']:.2f}")

        self._print_summary_footer()

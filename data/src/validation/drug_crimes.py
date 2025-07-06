import geopandas as gpd

from .base import BaseKDEValidator


class DrugCrimesOutputValidator(BaseKDEValidator):
    """
    Validator for Drug Crime KDE outputs.

    Validates drug crime density calculations with application-specific ranges:
    - drug_crimes_density: typically very small values (e-10 to e-7 range)
    - drug_crimes_density_zscore: roughly normal distribution around 0, std ~1
    - drug_crimes_density_percentile: 0-100 range (validated by base class)
    """

    @property
    def density_label_column(self) -> str:
        return "drug_crimes_density_label"

    @property
    def density_column(self) -> str:
        return "drug_crimes_density"

    @property
    def density_zscore_column(self) -> str:
        return "drug_crimes_density_zscore"

    @property
    def density_percentile_column(self) -> str:
        return "drug_crimes_density_percentile"

    def _validate_density_ranges(self, gdf: gpd.GeoDataFrame, errors: list):
        """
        Validate drug crime density and zscore ranges.

        Based on actual observed statistics:
        - density: max ~2.78e-07, mean ~6.38e-10, std ~6.37e-09
        - zscore: max ~43.51, mean ~0, std ~1
        """
        # Validate density values (drug crime densities can be larger than gun crimes)
        if self.density_column in gdf.columns:
            density = gdf[self.density_column]

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
        if self.density_zscore_column in gdf.columns:
            zscore = gdf[self.density_zscore_column]

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
        if self.density_percentile_column in gdf.columns:
            high_density_count = len(gdf[gdf[self.density_percentile_column] >= 90])
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

        if self.density_column in gdf.columns:
            density_stats = gdf[self.density_column].describe()
            print("Drug Crime Density statistics:")
            print(f"  Mean: {density_stats['mean']:.4e}")
            print(f"  Std:  {density_stats['std']:.4e}")
            print(f"  Min:  {density_stats['min']:.4e}")
            print(f"  Max:  {density_stats['max']:.4e}")

        if self.density_zscore_column in gdf.columns:
            zscore_stats = gdf[self.density_zscore_column].describe()
            print("Drug Crime Z-score statistics:")
            print(f"  Mean: {zscore_stats['mean']:.4f}")
            print(f"  Std:  {zscore_stats['std']:.4f}")
            print(f"  Min:  {zscore_stats['min']:.4f}")
            print(f"  Max:  {zscore_stats['max']:.4f}")

        if self.density_percentile_column in gdf.columns:
            percentile_stats = gdf[self.density_percentile_column].describe()
            print("Drug Crime Percentile statistics:")
            print(f"  Mean: {percentile_stats['mean']:.2f}")
            print(f"  Std:  {percentile_stats['std']:.2f}")
            print(f"  Min:  {percentile_stats['min']:.2f}")
            print(f"  Max:  {percentile_stats['max']:.2f}")

        self._print_summary_footer()

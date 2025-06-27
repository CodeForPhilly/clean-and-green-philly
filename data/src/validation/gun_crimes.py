import geopandas as gpd

from .base import BaseKDEValidator


class GunCrimesOutputValidator(BaseKDEValidator):
    """
    Validator for Gun Crime KDE outputs.

    Validates gun crime density calculations with application-specific ranges:
    - gun_crimes_density: typically very small values (e-10 to e-9 range)
    - gun_crimes_density_zscore: roughly normal distribution around 0, std ~1
    - gun_crimes_density_percentile: 0-100 range (validated by base class)
    """

    # Override schema to use actual column names
    schema = None  # We'll handle column validation in _row_level_validation

    def _row_level_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Row-level validation for gun crime KDE outputs."""
        # Call the grandparent's _row_level_validation (BaseValidator, not BaseKDEValidator)
        super(BaseKDEValidator, self)._row_level_validation(gdf, errors)

        # Check for required KDE columns with actual names
        required_columns = [
            "gun_crimes_density_label",
            "gun_crimes_density",
            "gun_crimes_density_zscore",
            "gun_crimes_density_percentile",
        ]
        self._validate_required_columns(gdf, required_columns, errors)

        # Validate density ranges (application-specific)
        self._validate_density_ranges(gdf, errors)

        # Validate application-specific requirements
        self._validate_application_specific(gdf, errors)

    def _validate_density_ranges(self, gdf: gpd.GeoDataFrame, errors: list):
        """
        Validate gun crime density and zscore ranges.

        Based on actual observed statistics:
        - density: max ~3.5e-09, mean ~1.3e-10, std ~1e-10
        - zscore: max ~7.15, mean ~0, std ~1
        """
        # Validate density values (gun crime densities are typically very small)
        if "gun_crimes_density" in gdf.columns:
            density = gdf["gun_crimes_density"]

            # Check for reasonable upper bound (allowing flexibility based on actual data)
            max_density = density.max()
            if max_density > 1e-8:  # Allow up to 1e-8 (much higher than observed max)
                errors.append(
                    f"Gun crime density values appear too high: max={max_density:.2e} "
                    f"(expected < 1e-8)"
                )

            # Check for reasonable lower bound (should be non-negative)
            min_density = density.min()
            if min_density < 0:
                errors.append(
                    f"Gun crime density values should be non-negative: min={min_density:.2e}"
                )

            # Check for reasonable mean (should be in e-10 to e-11 range)
            mean_density = density.mean()
            if mean_density > 1e-8 or mean_density < 1e-12:
                errors.append(
                    f"Gun crime density mean appears outside expected range: "
                    f"mean={mean_density:.2e} (expected ~1e-10 to 1e-11)"
                )

        # Validate z-score values (should be roughly normal distribution)
        if "gun_crimes_density_zscore" in gdf.columns:
            zscore = gdf["gun_crimes_density_zscore"]

            # Check z-score mean (should be close to 0)
            mean_zscore = zscore.mean()
            if abs(mean_zscore) > 0.1:  # Allow some deviation from 0
                errors.append(
                    f"Gun crime z-score mean appears too far from 0: "
                    f"mean={mean_zscore:.4f} (expected ~0)"
                )

            # Check z-score standard deviation (should be close to 1)
            std_zscore = zscore.std()
            if std_zscore < 0.5 or std_zscore > 2.0:  # Allow reasonable range
                errors.append(
                    f"Gun crime z-score standard deviation appears outside expected range: "
                    f"std={std_zscore:.4f} (expected ~1.0)"
                )

            # Check for extreme outliers (z-scores beyond ±10 are suspicious, based on actual data)
            extreme_outliers = zscore[(zscore < -10) | (zscore > 10)]
            if len(extreme_outliers) > 0:
                errors.append(
                    f"Found {len(extreme_outliers)} extreme z-score outliers "
                    f"(beyond ±10): min={zscore.min():.2f}, max={zscore.max():.2f}"
                )

    def _validate_application_specific(self, gdf: gpd.GeoDataFrame, errors: list):
        """
        Validate gun crime-specific requirements.
        """
        # Check that we have a reasonable number of high-density areas
        if "gun_crimes_density_percentile" in gdf.columns:
            high_density_count = len(gdf[gdf["gun_crimes_density_percentile"] >= 90])
            total_count = len(gdf)

            # Expect roughly 10% of areas to be in top 10% (with some flexibility)
            expected_high_density = total_count * 0.1
            if (
                high_density_count < expected_high_density * 0.5
                or high_density_count > expected_high_density * 2.0
            ):
                errors.append(
                    f"Gun crime high-density areas (≥90th percentile) count appears unusual: "
                    f"{high_density_count} out of {total_count} ({high_density_count / total_count * 100:.1f}%) "
                    f"(expected ~10%)"
                )

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print gun crime KDE-specific statistical summary."""
        self._print_summary_header("Gun Crime KDE Output Statistics", gdf)

        if "gun_crimes_density" in gdf.columns:
            density_stats = gdf["gun_crimes_density"].describe()
            print("Gun Crime Density statistics:")
            print(f"  Mean: {density_stats['mean']:.4e}")
            print(f"  Std:  {density_stats['std']:.4e}")
            print(f"  Min:  {density_stats['min']:.4e}")
            print(f"  Max:  {density_stats['max']:.4e}")

        if "gun_crimes_density_zscore" in gdf.columns:
            zscore_stats = gdf["gun_crimes_density_zscore"].describe()
            print("Gun Crime Z-score statistics:")
            print(f"  Mean: {zscore_stats['mean']:.4f}")
            print(f"  Std:  {zscore_stats['std']:.4f}")
            print(f"  Min:  {zscore_stats['min']:.4f}")
            print(f"  Max:  {zscore_stats['max']:.4f}")

        if "gun_crimes_density_percentile" in gdf.columns:
            percentile_stats = gdf["gun_crimes_density_percentile"].describe()
            print("Gun Crime Percentile statistics:")
            print(f"  Mean: {percentile_stats['mean']:.2f}")
            print(f"  Std:  {percentile_stats['std']:.2f}")
            print(f"  Min:  {percentile_stats['min']:.2f}")
            print(f"  Max:  {percentile_stats['max']:.2f}")

        self._print_summary_footer()

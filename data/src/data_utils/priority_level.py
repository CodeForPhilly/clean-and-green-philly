import geopandas as gpd
import pandas as pd


def priority_level(dataset: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Determines priority levels for properties based on gun crime density,
    violations, tree canopy gaps, and PHS Landcare status.

    Args:
        dataset (FeatureLayer): A feature layer containing property data.

    Returns:
        FeatureLayer: The input feature layer with an added "priority_level" column,
        indicating the priority for each property as "Low", "Medium", or "High".

    Columns Added:
        priority_level (str): The priority level ( "Low", "Medium", or "High") of the property
            based on gun crime density, violations, tree canopy gaps, and PHS Landcare status.

    Tagline:
        Add priority levels

    Source:
        gun_crimes_density_zscore, all_violations_past_year, l_and_i_complaints_density_zscore,
        tree_canopy_gap, phs_care_program columns in the primary feature layer.
    """
    priority_levels = []
    for idx, row in dataset.iterrows():
        priority_level = ""

        # Decision Points
        guncrime_density_zscore = row["gun_crimes_density_zscore"]
        in_phs_landcare = pd.notna(row["phs_care_program"])
        has_violation_or_high_density = (
            float(row["all_violations_past_year"]) > 0
            or row["l_and_i_complaints_density_zscore"] > 0  # above the mean
        )
        very_low_tree_canopy = row["tree_canopy_gap"] >= 0.3

        # Logic for priority levels
        if guncrime_density_zscore <= 0:
            # Low Gun Crime Density (below the mean)
            priority_level = "Low"

        elif guncrime_density_zscore > 1:
            # High Gun Crime Density (more than 1 std above the mean)
            if has_violation_or_high_density:
                priority_level = "High"
            else:
                if in_phs_landcare:
                    if very_low_tree_canopy:
                        priority_level = "High"
                    else:
                        priority_level = "Medium"
                else:
                    priority_level = "High"

        else:
            # Medium Gun Crime Density (between the mean and 1 std above the mean)
            if has_violation_or_high_density:
                if in_phs_landcare:
                    priority_level = "Medium"
                else:
                    if very_low_tree_canopy:
                        priority_level = "High"
                    else:
                        priority_level = "Medium"
            else:
                priority_level = "Low"

        priority_levels.append(priority_level)

    dataset["priority_level"] = priority_levels

    return dataset

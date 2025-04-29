def priority_level(dataset):
    priority_levels = []
    for _, row in dataset.gdf.iterrows():
        priority_level = ""

        # Decision Points
        guncrime_density_percentile = row["gun_crimes_density_percentile"]
        in_phs_landcare = row["phs_care_program"] == "yes"
        has_li_complaint_or_violation = (
            row["li_complaints"] is not None
            and float(row["all_violations_past_year"]) > 0
        )
        very_low_tree_canopy = row["tree_canopy_gap"] >= 0.3

        # Updated logic based on percentile values
        if guncrime_density_percentile <= 50:
            # Low Gun Crime Density (Bottom 50%)
            priority_level = "Low"

        elif guncrime_density_percentile > 75:
            # High Gun Crime Density (Top 25%)

            if has_li_complaint_or_violation:
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
            # Medium Gun Crime Density (Between 50% and 75%)
            if has_li_complaint_or_violation:
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

    dataset.gdf["priority_level"] = priority_levels

    return dataset

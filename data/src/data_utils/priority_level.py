def priority_level(dataset):
    priority_levels = []
    for idx, row in dataset.gdf.iterrows():
        priority_level = ""

        # Decision Points
        guncrime_density = row["guncrime_density"]
        in_phs_landcare = row["phs_partner_agency"] == 'PHS'
        has_li_complaint_or_violation = row["li_complaints"] is not None and float(
            row["all_violations_past_year"]) > 0
        very_low_tree_canopy = row["tree_canopy_gap"] >= 0.3

        if guncrime_density == 'Bottom 50%':
            # Low Gun Crime Density
            priority_level = "Low"

        elif guncrime_density in ["Top 25%", "Top 10%", "Top 5%", "Top 1%"]:
            # High Gun Crime Density

            if has_li_complaint_or_violation:
                priority_level = "High"
            else:
                if in_phs_landcare:
                    if very_low_tree_canopy:
                        priority_level = "High"
                    else:
                        priority_level = "Medium"
                else:
                    priority_level = 'High'

        else:
            # Medium Gun Crime Density
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

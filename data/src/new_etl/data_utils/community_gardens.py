from ..classes.featurelayer import FeatureLayer
from ..constants.services import COMMUNITY_GARDENS_TO_LOAD
from config.config import USE_CRS


def community_gardens(primary_featurelayer: FeatureLayer) -> FeatureLayer:
    """
    Updates the 'vacant' column in the primary feature layer to ensure community gardens
    are marked as not vacant. This protects known community gardens from being categorized
    as vacant, preventing potential predatory development.
    """
    if "vacant" not in primary_featurelayer.gdf.columns:
        raise ValueError("The 'vacant' column is missing in the primary feature layer.")

    # Load community gardens
    community_gardens = FeatureLayer(
        name="Community Gardens", esri_rest_urls=COMMUNITY_GARDENS_TO_LOAD
    )

    # Ensure both layers are in the same CRS
    if community_gardens.gdf.crs != USE_CRS:
        print(
            f"Transforming community gardens from {community_gardens.gdf.crs} to {USE_CRS}"
        )
        community_gardens.gdf = community_gardens.gdf.to_crs(USE_CRS)

    # Identify problematic gardens
    geom_types = community_gardens.gdf.geometry.geom_type.value_counts()

    if len(geom_types) > 1:
        print("\nGardens with non-Point geometries:")
        non_point_gardens = community_gardens.gdf[
            community_gardens.gdf.geometry.geom_type != "Point"
        ]
        print(f"Total non-Point geometries: {len(non_point_gardens)}")
        print("\nSample of problematic records:")
        print(non_point_gardens[["site_name", "geometry"]].head())

        # Convert any non-point geometries to points using centroid
        print("\nConverting non-Point geometries to points using centroids...")
        community_gardens.gdf.loc[
            community_gardens.gdf.geometry.geom_type != "Point", "geometry"
        ] = community_gardens.gdf[
            community_gardens.gdf.geometry.geom_type != "Point"
        ].geometry.centroid

    # Verify all geometries are now points
    if not all(community_gardens.gdf.geometry.geom_type == "Point"):
        raise ValueError("Failed to convert all geometries to points")

    # Limit the community gardens data to relevant columns
    community_gardens.gdf = community_gardens.gdf[["site_name", "geometry"]]

    print(f"\nTotal community gardens: {len(community_gardens.gdf)}")

    # Use 'contains' predicate since we want the parcel that contains each point
    joined_gdf = primary_featurelayer.gdf.sjoin(
        community_gardens.gdf, predicate="contains", how="inner"
    )

    # Count matches per garden
    matches_per_garden = joined_gdf.groupby("site_name").size()

    # Print details for gardens with unusually high matches
    # Gardens with high number of matches
    if matches_per_garden.max() > 1:  # arbitrary threshold
        print("\nGardens with high number of matches:")
        high_matches = matches_per_garden[matches_per_garden > 1]
        print(high_matches)

        # Print concise details about properties matching these gardens
        print("\nSummary of matched properties for high-match gardens:")
        for garden_name in high_matches.index:
            matched_properties = joined_gdf[joined_gdf["site_name"] == garden_name]
            print(f"\nGarden: {garden_name}")
            print("Matched parcels:")
            print(
                matched_properties[["opa_id"]]
                .drop_duplicates()
                .head(5)
                .to_string(index=False)
            )
            print(
                f"...and {len(matched_properties) - 5} more matches."
                if len(matched_properties) > 5
                else ""
            )

    # Get unique parcels that contain garden points
    garden_parcels = set(joined_gdf["opa_id"])
    print(f"\nUnique parcels containing gardens: {len(garden_parcels)}")

    if len(garden_parcels) > len(community_gardens.gdf):
        print(
            "\nWARNING: More matching parcels than gardens. This suggests possible data issues."
        )

    # Update vacant status for parcels containing gardens
    mask = primary_featurelayer.gdf["opa_id"].isin(garden_parcels)
    primary_featurelayer.gdf.loc[mask, "vacant"] = False

    print(f"\nTotal parcels updated: {mask.sum()}")

    return primary_featurelayer

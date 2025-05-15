import geopandas as gpd
import pandas as pd

from ..classes.featurelayer import FeatureLayer
from ..constants.services import COUNCIL_DISTRICTS_TO_LOAD
from ..metadata.metadata_utils import provide_metadata

pd.set_option("future.no_silent_downcasting", True)


@provide_metadata()
def council_dists(primary_featurelayer: FeatureLayer) -> FeatureLayer:
    """
    Associates properties in the primary feature layer with council districts
    using a spatial join. For properties without a district assignment,
    uses the most common district among the 3 nearest neighbors.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.

    Returns:
        FeatureLayer: The input feature layer with properties spatially joined
        to council districts, ensuring no duplicate entries.

    Tagline:
        Assigns council districts

    Columns added:
        district (str): The council district associated with the property.

    Primary Feature Layer Columns Referenced:
        opa_id, geometry
    """
    # Load council districts
    council_dists = FeatureLayer(
        name="Council Districts", esri_rest_urls=COUNCIL_DISTRICTS_TO_LOAD
    )

    # Check that the required columns exist in the DataFrame
    required_columns = ["district", "geometry"]
    missing_columns = [
        col for col in required_columns if col not in council_dists.gdf.columns
    ]
    if missing_columns:
        raise KeyError(
            f"Missing required columns in council districts data: {', '.join(missing_columns)}"
        )

    # Use only the required columns
    council_dists.gdf = council_dists.gdf[required_columns].copy()
    council_dists.rebuild_gdf()

    # Perform spatial join
    primary_featurelayer.spatial_join(council_dists)

    # Drop duplicates in the primary feature layer
    primary_featurelayer.gdf.drop_duplicates(inplace=True)
    primary_featurelayer.rebuild_gdf()

    # Handle missing district values using nearest neighbors
    missing_mask = primary_featurelayer.gdf["district"].isna()
    if missing_mask.any():
        print(f"\nFound {missing_mask.sum()} properties without district assignments")
        print("Imputing missing districts using nearest neighbors...")

        # Get properties with missing districts
        missing_props = primary_featurelayer.gdf[missing_mask].copy()

        # Get properties with valid districts
        valid_props = primary_featurelayer.gdf[~missing_mask].copy()

        # Find nearest neighbors for each missing property
        nearest = gpd.sjoin_nearest(
            missing_props,
            valid_props[["district", "geometry"]],
            how="left",
            max_distance=1000,  # 1000 feet max distance
            distance_col="distance",
        )

        # Print column names for debugging
        print("Available columns:", nearest.columns.tolist())

        # Group by the original index and get the most common district
        # Use district_right since that's from the valid properties
        imputed_districts = nearest.groupby(level=0)["district_right"].agg(
            lambda x: x.mode().iloc[0] if not x.empty else None
        )

        # Update the missing values
        primary_featurelayer.gdf.loc[imputed_districts.index, "district"] = (
            imputed_districts
        )

        # Print results
        imputed_count = imputed_districts.notna().sum()
        print(f"Successfully imputed districts for {imputed_count} properties")

        # Check if any properties still have missing districts
        remaining_missing = primary_featurelayer.gdf["district"].isna().sum()
        if remaining_missing > 0:
            print(
                f"Warning: {remaining_missing} properties still have missing districts"
            )

    return primary_featurelayer

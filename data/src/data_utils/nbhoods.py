from typing import Tuple

import geopandas as gpd

from src.validation.base import ValidationResult, validate_output
from src.validation.nbhoods import NeighborhoodsOutputValidator

from ..classes.loaders import GdfLoader
from ..constants.services import NBHOODS_URL
from ..utilities import spatial_join


@validate_output(NeighborhoodsOutputValidator)
def nbhoods(input_gdf: gpd.GeoDataFrame) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Adds neighborhood information to the input GeoDataFrame by performing a spatial join
    with a neighborhoods dataset.

    Args:
        input_gdf (GeoDataFrame): The GeoDataFrame containing property data.

    Returns:
        GeoDataFrame: The input GeoDataFrame with an added "neighborhood" column,
        containing the name of the neighborhood for each property.

    Tagline:
        Assigns neighborhoods

    Columns added:
        neighborhood (str): The name of the neighborhood associated with the property.

    Columns Referenced:
        opa_id, geometry

    Source:
        https://raw.githubusercontent.com/opendataphilly/open-geo-data/master/philadelphia-neighborhoods/philadelphia-neighborhoods.geojson
    """

    loader = GdfLoader(name="Neighborhoods", input=NBHOODS_URL, cols=["mapname"])
    phl_nbhoods, input_validation = loader.load_or_fetch()

    # Correct the column name to lowercase if needed
    if "mapname" in phl_nbhoods.columns:
        phl_nbhoods.rename(columns={"mapname": "neighborhood"}, inplace=True)

    merged_gdf = spatial_join(input_gdf, phl_nbhoods, predicate="within")

    # Check for properties without neighborhood assignments and use nearest neighbor
    if "neighborhood" in merged_gdf.columns:
        null_neighborhood_count = merged_gdf["neighborhood"].isna().sum()
        if null_neighborhood_count > 0:
            print(
                f"\n[DEBUG] Found {null_neighborhood_count} properties without neighborhood assignments"
            )
            print("Assigning neighborhoods using nearest neighbor...")

            # For properties without neighborhoods, assign based on nearest neighborhood
            null_neighborhood_mask = merged_gdf["neighborhood"].isna()
            properties_without_neighborhoods = merged_gdf[null_neighborhood_mask]

            if len(properties_without_neighborhoods) > 0:
                # Use nearest neighbor to assign neighborhoods
                for idx in properties_without_neighborhoods.index:
                    property_geom = merged_gdf.loc[idx, "geometry"]
                    # Find the nearest neighborhood boundary
                    distances = phl_nbhoods.geometry.distance(property_geom)
                    nearest_neighborhood_idx = distances.idxmin()
                    nearest_neighborhood = phl_nbhoods.loc[
                        nearest_neighborhood_idx, "neighborhood"
                    ]
                    merged_gdf.loc[idx, "neighborhood"] = nearest_neighborhood

                print(
                    f"Assigned neighborhoods to {null_neighborhood_count} properties using nearest neighbor"
                )

            # Final check
            final_null_count = merged_gdf["neighborhood"].isna().sum()
            if final_null_count > 0:
                print(
                    f"WARNING: {final_null_count} properties still have null neighborhood values"
                )

    return merged_gdf, input_validation

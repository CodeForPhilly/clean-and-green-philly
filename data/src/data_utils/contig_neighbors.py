import warnings
from typing import Tuple

import geopandas as gpd
import networkx as nx
import numpy as np
from libpysal.weights import Queen

from src.validation.base import ValidationResult, validate_output
from src.validation.contig_neighbors import ContigNeighborsOutputValidator

from ..utilities import opa_join


@validate_output(ContigNeighborsOutputValidator)
def contig_neighbors(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Calculates the number of contiguous vacant neighbors for each property in a feature layer.

    Args:
        primary_featurelayer (FeatureLayer): A feature layer containing property data in a GeoDataFrame (`gdf`).

    Returns:
        FeatureLayer: The input feature layer with an added "n_contiguous" column indicating
        the number of contiguous vacant neighbors for each property.

    Tagline:
        Count vacant neighbors

    Columns Added:
        n_contiguous (int): The number of contiguous vacant neighbors for each property.

    Primary Feature Layer Columns Referenced:
        opa_id, vacant
    """
    print(f"[DEBUG] contig_neighbors: Starting with {len(input_gdf)} properties")
    print(f"[DEBUG] contig_neighbors: Vacant properties: {input_gdf['vacant'].sum()}")

    # Debug geometry types
    geometry_types = input_gdf.geometry.type.value_counts()
    print(
        f"[DEBUG] contig_neighbors: Geometry types in dataset: {dict(geometry_types)}"
    )

    # Debug vacant properties geometry types
    vacant_gdf = input_gdf[input_gdf["vacant"]]
    if len(vacant_gdf) > 0:
        vacant_geometry_types = vacant_gdf.geometry.type.value_counts()
        print(
            f"[DEBUG] contig_neighbors: Vacant properties geometry types: {dict(vacant_geometry_types)}"
        )
    else:
        print("[DEBUG] contig_neighbors: No vacant properties found")

    # Create a filtered dataframe with only vacant properties and polygon geometries
    vacant_parcels = input_gdf.loc[
        (input_gdf["vacant"])
        & (input_gdf.geometry.type.isin(["Polygon", "MultiPolygon"])),
        ["opa_id", "geometry"],
    ]

    print(
        f"[DEBUG] contig_neighbors: Vacant parcels with valid geometry: {len(vacant_parcels)}"
    )

    if vacant_parcels.empty:
        print("No vacant properties found in the dataset.")
        input_gdf["n_contiguous"] = np.nan
        print("[DEBUG] contig_neighbors: Returning single value (should be tuple)")
        result = input_gdf, ValidationResult(True)
        print(f"[DEBUG] contig_neighbors: Return type: {type(result)}")
        print(f"[DEBUG] contig_neighbors: Return length: {len(result)}")
        return result

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)
        warnings.filterwarnings(
            "ignore",
            category=UserWarning,
            message="The weights matrix is not fully connected",
        )

        # Create a spatial weights matrix for vacant parcels
        w = Queen.from_dataframe(vacant_parcels)

    # Convert the spatial weights matrix to a NetworkX graph
    g = w.to_networkx()

    # Calculate the number of contiguous vacant properties for each vacant parcel
    n_contiguous = {
        node: len(nx.node_connected_component(g, node)) - 1 for node in g.nodes
    }

    # Debug: Check what values we're getting
    print(
        f"[DEBUG] contig_neighbors: n_contiguous values calculated: {len(n_contiguous)}"
    )
    if len(n_contiguous) > 0:
        sample_values = list(n_contiguous.values())[:10]
        print(f"[DEBUG] contig_neighbors: Sample n_contiguous values: {sample_values}")
        print(
            f"[DEBUG] contig_neighbors: n_contiguous value types: {[type(v) for v in sample_values]}"
        )

    # Assign the contiguous neighbor count to the filtered vacant parcels
    vacant_parcels["n_contiguous"] = vacant_parcels.index.map(n_contiguous)

    # Debug: Check what's in vacant_parcels after assignment
    print(
        f"[DEBUG] contig_neighbors: vacant_parcels n_contiguous column: {vacant_parcels['n_contiguous'].dtype}"
    )
    print(
        f"[DEBUG] contig_neighbors: vacant_parcels n_contiguous sample: {vacant_parcels['n_contiguous'].head().tolist()}"
    )
    print(
        f"[DEBUG] contig_neighbors: vacant_parcels n_contiguous null count: {vacant_parcels['n_contiguous'].isna().sum()}"
    )

    # Debug: Check for boolean values in vacant_parcels
    bool_mask = vacant_parcels["n_contiguous"].apply(lambda x: isinstance(x, bool))
    if bool_mask.any():
        print(
            f"[DEBUG] contig_neighbors: Found {bool_mask.sum()} boolean values in vacant_parcels!"
        )
        print(
            f"[DEBUG] contig_neighbors: Boolean values: {vacant_parcels.loc[bool_mask, 'n_contiguous'].tolist()}"
        )

    # Debug: Check opa_id matching
    print(
        f"[DEBUG] contig_neighbors: vacant_parcels opa_id sample: {vacant_parcels['opa_id'].head().tolist()}"
    )
    print(
        f"[DEBUG] contig_neighbors: input_gdf opa_id sample: {input_gdf['opa_id'].head().tolist()}"
    )
    print(
        f"[DEBUG] contig_neighbors: vacant_parcels opa_id type: {vacant_parcels['opa_id'].dtype}"
    )
    print(
        f"[DEBUG] contig_neighbors: input_gdf opa_id type: {input_gdf['opa_id'].dtype}"
    )

    # Merge the results back to the primary feature layer
    input_gdf = opa_join(input_gdf, vacant_parcels[["opa_id", "n_contiguous"]])

    # Debug: Check what's in input_gdf after join
    print(
        f"[DEBUG] contig_neighbors: input_gdf n_contiguous column: {input_gdf['n_contiguous'].dtype}"
    )
    print(
        f"[DEBUG] contig_neighbors: input_gdf n_contiguous sample: {input_gdf['n_contiguous'].head().tolist()}"
    )
    print(
        f"[DEBUG] contig_neighbors: input_gdf n_contiguous null count: {input_gdf['n_contiguous'].isna().sum()}"
    )

    # Debug: Check for boolean values in input_gdf
    bool_mask = input_gdf["n_contiguous"].apply(lambda x: isinstance(x, bool))
    if bool_mask.any():
        print(
            f"[DEBUG] contig_neighbors: Found {bool_mask.sum()} boolean values in input_gdf!"
        )
        print(
            f"[DEBUG] contig_neighbors: Boolean values: {input_gdf.loc[bool_mask, 'n_contiguous'].tolist()}"
        )

    # Debug: Check if any non-null values exist
    non_null_mask = input_gdf["n_contiguous"].notna()
    if non_null_mask.any():
        print(
            f"[DEBUG] contig_neighbors: Found {non_null_mask.sum()} non-null n_contiguous values"
        )
        print(
            f"[DEBUG] contig_neighbors: Non-null sample: {input_gdf.loc[non_null_mask, 'n_contiguous'].head().tolist()}"
        )
    else:
        print(
            "[DEBUG] contig_neighbors: No non-null n_contiguous values found after join"
        )

    # Assign NA for non-vacant properties
    input_gdf.loc[~input_gdf["vacant"], "n_contiguous"] = np.nan

    # Final check: Ensure no boolean values remain
    final_bool_mask = input_gdf["n_contiguous"].apply(lambda x: isinstance(x, bool))
    if final_bool_mask.any():
        print(
            f"[DEBUG] contig_neighbors: WARNING - Found {final_bool_mask.sum()} boolean values in final result!"
        )
        print("[DEBUG] contig_neighbors: Converting boolean values to numeric...")
        # Convert boolean False to 0, True to 1
        input_gdf.loc[final_bool_mask, "n_contiguous"] = input_gdf.loc[
            final_bool_mask, "n_contiguous"
        ].astype(int)

    print("[DEBUG] contig_neighbors: Returning tuple with ValidationResult")
    result = input_gdf, ValidationResult(True)
    print(f"[DEBUG] contig_neighbors: Return type: {type(result)}")
    print(f"[DEBUG] contig_neighbors: Return length: {len(result)}")
    return result

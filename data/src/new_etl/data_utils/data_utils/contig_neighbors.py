import warnings
import networkx as nx
from libpysal.weights import Queen
import numpy as np


def contig_neighbors(primary_featurelayer):
    # Create a filtered dataframe with only vacant properties and polygon geometries
    vacant_parcels = primary_featurelayer.gdf.loc[
        (primary_featurelayer.gdf["vacant"])
        & (primary_featurelayer.gdf.geometry.type.isin(["Polygon", "MultiPolygon"])),
        ["opa_id", "geometry"],
    ]

    if vacant_parcels.empty:
        print("No vacant properties found in the dataset.")
        primary_featurelayer.gdf["n_contiguous"] = np.nan
        return primary_featurelayer

    print(f"Found {len(vacant_parcels)} vacant properties.")

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)
        warnings.filterwarnings(
            "ignore",
            category=UserWarning,
            message="The weights matrix is not fully connected",
        )

        # Create a spatial weights matrix for vacant parcels
        print("Creating spatial weights matrix for vacant parcels...")
        w = Queen.from_dataframe(vacant_parcels)

    # Convert the spatial weights matrix to a NetworkX graph
    print("Converting spatial weights matrix to NetworkX graph...")
    g = w.to_networkx()

    # Calculate the number of contiguous vacant properties for each vacant parcel
    print("Calculating number of contiguous vacant neighbors for each property...")
    n_contiguous = {
        node: len(nx.node_connected_component(g, node)) - 1 for node in g.nodes
    }

    # Assign the contiguous neighbor count to the filtered vacant parcels
    vacant_parcels["n_contiguous"] = vacant_parcels.index.map(n_contiguous)

    # Merge the results back to the primary feature layer
    primary_featurelayer.gdf = primary_featurelayer.gdf.merge(
        vacant_parcels[["opa_id", "n_contiguous"]], on="opa_id", how="left"
    )

    # Assign NA for non-vacant properties
    primary_featurelayer.gdf.loc[
        ~primary_featurelayer.gdf["vacant"], "n_contiguous"
    ] = np.nan

    print("Process completed. Returning updated primary feature layer.")
    return primary_featurelayer

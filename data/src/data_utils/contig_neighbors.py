import warnings
import networkx as nx
from libpysal.weights import Queen


def contig_neighbors(primary_featurelayer):
    # Filter the parcels to only consider vacant properties
    parcels = primary_featurelayer.gdf[primary_featurelayer.gdf["vacant"] == 1]

    if parcels.empty:
        print("No vacant properties found in the dataset.")
        primary_featurelayer.gdf["n_contiguous"] = 0
        return primary_featurelayer

    print(f"Found {len(parcels)} vacant properties.")

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)
        warnings.filterwarnings(
            "ignore",
            category=UserWarning,
            message="The weights matrix is not fully connected",
        )

        # Create a spatial weights matrix for vacant parcels
        print("Creating spatial weights matrix for vacant parcels...")
        w = Queen.from_dataframe(parcels)

    print("Converting spatial weights matrix to NetworkX graph...")
    g = w.to_networkx()

    # Calculate the number of contiguous neighbors for each vacant property
    print("Calculating number of contiguous vacant neighbors for each property...")
    n_contiguous = {
        node: len(nx.node_connected_component(g, node)) - 1 for node in g.nodes
    }

    # Assign the number of contiguous vacant neighbors to vacant properties
    parcels["n_contiguous"] = parcels.index.map(n_contiguous).fillna(0).astype(int)

    print("Joining results back to primary feature layer...")
    primary_featurelayer.gdf = primary_featurelayer.gdf.merge(
        parcels[["opa_id", "n_contiguous"]], on="opa_id", how="left"
    )

    # For non-vacant properties, set the number of contiguous vacant neighbors to 0
    primary_featurelayer.gdf["n_contiguous"].fillna(0, inplace=True)

    print("Process completed. Returning updated primary feature layer.")
    return primary_featurelayer

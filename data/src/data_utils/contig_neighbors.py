import warnings

import networkx as nx
from libpysal.weights import Queen


def contig_neighbors(primary_featurelayer):
    parcels = primary_featurelayer.gdf

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)
        warnings.filterwarnings(
            "ignore",
            category=UserWarning,
            message="The weights matrix is not fully connected",
        )

        w = Queen.from_dataframe(parcels)

    g = w.to_networkx()

    # Calculate the number of contiguous neighbors for each feature in parcels
    n_contiguous = [len(nx.node_connected_component(g, i)) for i in range(len(parcels))]

    primary_featurelayer.gdf["n_contiguous"] = n_contiguous

    return primary_featurelayer

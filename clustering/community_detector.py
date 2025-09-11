# community/community_detector.py
import networkx as nx
import igraph as ig
try:
    import leidenalg
except ImportError:
    leidenalg = None
try:
    import community as community_louvain  # python-louvain package
except ImportError:
    community_louvain = None

from igraph_converter import convert_networkx_to_igraph_via_graphml


def detect_communities(G: nx.Graph, method: str = 'louvain', seed = None, weight="weight") -> dict:
    """
    Detecta comunidades en el grafo de similitud de pacientes.

    :param G: Grafo de NetworkX con nodos de pacientes y aristas ponderadas por similitud.
    :param method: Algoritmo a utilizar: 'louvain' o 'label_propagation'.
    :return: Diccionario { patient_id: community_id }
    """
    if method == 'louvain':
        if community_louvain is None:
            raise ImportError("El paquete 'community' (python-louvain) no está instalado.")
        partition = community_louvain.best_partition(G, weight='weight', random_state=seed, resolution=1)

    elif method == 'label_propagation':
        communities = nx.algorithms.community.asyn_lpa_communities(G, weight='weight')
        partition = {}
        for idx, comm in enumerate(communities):
            for node in comm:
                partition[node] = idx

    elif method == 'leiden':
        # Convert NetworkX graph to igraph via GraphML round-trip
        ig_graph = convert_networkx_to_igraph_via_graphml(G)

        # Run Leiden algorithm on the igraph graph
        partition_obj = leidenalg.find_partition(
            ig_graph,
            leidenalg.ModularityVertexPartition,
            weights=weight,
            seed=seed
        )

        # Map igraph vertex names back to community IDs
        membership = partition_obj.membership
        node_names = ig_graph.vs['name']
        return { node_names[i]: membership[i] for i in range(len(node_names)) }

    else:
        raise ValueError(f"Método desconocido: {method}. Use 'louvain' o 'label_propagation'.")

    return partition


def evaluate_modularity(G: nx.Graph, partition: dict) -> float:
    """
    Calcula la modularidad de la partición dada en el grafo.

    :param G: Grafo de NetworkX.
    :param partition: Diccionario { node: community_id }.
    :return: Valor de modularidad (float).
    """
    community_dict = {}
    for node, comm_id in partition.items():
        community_dict.setdefault(comm_id, set()).add(node)
    communities = list(community_dict.values())
    return nx.algorithms.community.modularity(G, communities, weight='weight')

def calculate_community_modularity(partition, G, weight='weight'):

    modularity_score = community_louvain.modularity(partition, G, weight='weight')
    return modularity_score
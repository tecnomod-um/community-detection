# feature_builder/graph_builder.py
import networkx as nx
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity


def build_similarity_graph(feature_vectors: np.ndarray,
                           patient_ids: list,
                           threshold: float = None) -> nx.Graph:
    """
    Construye un grafo de similitud a partir de la matriz de características.

    :param feature_vectors: Matriz NumPy de forma (n_pacientes, n_características)
    :param patient_ids: Lista de identificadores de pacientes, de longitud n_pacientes
    :param threshold: Umbral opcional para crear aristas. Si None, se crea grafo completo ponderado.
    :return: Grafo de NetworkX con nodos etiquetados por patient_ids y aristas ponderadas por similitud.
    """
    G = nx.Graph()

    # Agregar nodos de pacientes
    for pid in patient_ids:
        G.add_node(pid)

    # Calcular similitud entre vectores (coseno)
    sim_matrix = cosine_similarity(feature_vectors)

    # Agregar aristas según umbral
    n = len(patient_ids)
    for i in range(n):
        for j in range(i + 1, n):
            weight = sim_matrix[i, j]
            if weight > 0 and (threshold is None or weight >= threshold):
                G.add_edge(patient_ids[i], patient_ids[j], weight=weight)

    return G
# community_detection_main.py
from feature_builder.vectorizer import build_feature_vectors
from feature_builder.graph_builder import build_similarity_graph
from clustering.community_detector import detect_communities, evaluate_modularity, calculate_community_modularity
import argparse
from clustering.community_visualization import visualize_communities
import random
import numpy as np


def community_detection_main(ttl_path: str,
                             similarity_threshold: float = None,
                             method: str = 'louvain',
                             seed_random = None) -> dict:
    """
    Función principal para ejecutar el pipeline completo de detección de comunidades.

    Pasos:
      1. Carga y vectorización de características.
      2. Construcción del grafo de similitud.
      3. Detección de comunidades.
      4. Evaluación de la modularidad.
      5. Visualización básica de comunidades.

    :param ttl_path: Ruta al archivo .ttl con el grafo RDF
    :param similarity_threshold: Umbral de similitud para filtrar aristas (None = grafo completo)
    :param method: Algoritmo de detección de comunidades ('louvain' o 'label_propagation')
    :return: Diccionario { paciente_id: comunidad_id }
    """
    print("[DEBUG] Iniciando community_detection_main", flush=True)
    # Paso 1: Construir vectores de características
    feature_vectors, patient_ids = build_feature_vectors(ttl_path)
    print(f"[1] Características extraídas: {len(patient_ids)} pacientes, {feature_vectors.shape[1]} dimensiones.", flush=True)

    # Paso 2: Construir grafo de similitud
    G = build_similarity_graph(feature_vectors, patient_ids, threshold=similarity_threshold)
    print(f"[2] Grafo construido: {G.number_of_nodes()} nodos, {G.number_of_edges()} aristas.", flush=True)

    # Paso 3: Detectar comunidades
    partition = detect_communities(G, method=method, seed=seed_random)
    n_comms = len(set(partition.values()))
    print(f"[3] Comunidades detectadas ({method}): {n_comms} comunidades.", flush=True)

    # Paso 4: Evaluar modularidad
    modularity = evaluate_modularity(G, partition)
    print(f"[4] Modularidad de la partición: {modularity:.4f}", flush=True)

    # Paso 5: Mostrar comunidades formadas
    communities = {}
    for patient, comm_id in partition.items():
        communities.setdefault(comm_id, []).append(patient)
    print("[5] Detalle de comunidades:", flush=True)
    for comm_id, members in communities.items():
        print(f"  Comunidad {comm_id} ({len(members)} pacientes):")
        for pid in members:
            print(f"    - {pid}")
    print("[Done] Visualización de comunidades completada.", flush=True)

    return partition, G


if __name__ == '__main__':

    SEED = 42

    random.seed(SEED)
    np.random.seed(SEED)


    parser = argparse.ArgumentParser(description='Pipeline de Community Detection para pacientes RDF')
    parser.add_argument('ttl_path', help='Ruta al archivo .ttl con el grafo RDF')
    parser.add_argument('--threshold', type=float, default=None,
                        help='Umbral de similitud para filtrar aristas (entre 0 y 1)')
    parser.add_argument('--method', choices=['louvain', 'label_propagation'], default='louvain',
                        help='Método de detección de comunidades')
    args = parser.parse_args()

    partition, G = community_detection_main(
        ttl_path=args.ttl_path,
        similarity_threshold=args.threshold,
        method=args.method,
        seed_random=SEED
    )

    visualize_communities(G, partition, "visualization_output/communitiesGuttman", False)

    import community as community_louvain

    modularity_score = calculate_community_modularity(partition, G, weight='weight')
    print(f"Modularity score: {modularity_score:.4f}")

    # --- Save communities to a TXT file ---
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_txt = f"communities_{timestamp}.txt"

    # Group patients by community
    communities = {}
    for patient_id, comm_id in partition.items():
        communities.setdefault(comm_id, []).append(patient_id)

    # Write out
    with open(output_txt, 'w') as f:
        for comm_id, members in communities.items():
            f.write(f"Community {comm_id} ({len(members)} patients):\n")
            for pid in members:
                f.write(f"  {pid}\n")
            f.write("\n")

    print(f"Communities successfully saved to: {output_txt}")


# consensus_communities.py
import argparse
import numpy as np
import pandas as pd

from feature_builder.vectorizer import build_feature_vectors
from feature_builder.graph_builder import build_similarity_graph
from clustering.community_detector import detect_communities


def main(ttl_path: str,
         similarity_threshold: float,
         method: str,
         runs: int,
         output_csv: str,
         trim_names: bool = True):
    """
    Performs community detection multiple times and builds a co-occurrence matrix.

    :param ttl_path: Path to the RDF .ttl file containing patient data.
    :param similarity_threshold: Threshold to filter similarity graph edges.
    :param method: Community detection method ('louvain' or 'label_propagation').
    :param runs: Number of times to run community detection.
    :param output_csv: Path to save the co-occurrence matrix CSV.
    """
    # Step 1: Build feature vectors and similarity graph
    feature_vectors, patient_ids = build_feature_vectors(ttl_path)
    G = build_similarity_graph(feature_vectors, patient_ids, threshold=similarity_threshold)

    # Determine display names (trim after last '#')
    if trim_names:
        display_ids = [pid.split('#')[-1] for pid in patient_ids]
    else:
        display_ids = list(patient_ids)

    # Map original patient_id to index
    n = len(patient_ids)
    cooc_matrix = np.zeros((n, n), dtype=int)
    id_to_index = {pid: idx for idx, pid in enumerate(patient_ids)}

    # Step 2: Run community detection multiple times
    for run in range(runs):
        partition = detect_communities(G, method=method)
        communities = {}
        for pid, comm_id in partition.items():
            communities.setdefault(comm_id, []).append(pid)
        for members in communities.values():
            for i in range(len(members)):
                for j in range(i + 1, len(members)):
                    idx_i = id_to_index[members[i]]
                    idx_j = id_to_index[members[j]]
                    cooc_matrix[idx_i, idx_j] += 1
                    cooc_matrix[idx_j, idx_i] += 1

    # Step 3: Save to CSV
    df = pd.DataFrame(cooc_matrix, index=display_ids, columns=display_ids)
    df.to_csv(output_csv)
    print(f"Co-occurrence matrix ({runs} runs) saved to: {output_csv}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Compute consensus co-occurrence matrix over multiple community detection runs.'
    )
    parser.add_argument('ttl_path', help='Path to the RDF .ttl file')
    parser.add_argument('--threshold', type=float, default=None,
                        help='Similarity threshold to filter edges (default: None)')
    parser.add_argument('--method', choices=['louvain', 'label_propagation'], default='louvain',
                        help='Community detection algorithm (default: louvain)')
    parser.add_argument('--runs', type=int, default=20,
                        help='Number of runs for consensus (default: 20)')
    parser.add_argument('--output', default='cooccurrence_matrix.csv',
                        help='Output CSV path (default: cooccurrence_matrix.csv)')
    args = parser.parse_args()

    main(
        ttl_path=args.ttl_path,
        similarity_threshold=args.threshold,
        method=args.method,
        runs=args.runs,
        output_csv=args.output
    )

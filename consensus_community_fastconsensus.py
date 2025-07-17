#!/usr/bin/env python3
"""
run_pipeline.py

Orchestrates the full patient‐community pipeline:
  1) Extract features from an RDF Turtle file
  2) Build a weighted NetworkX similarity graph
  3) (Optionally) export the NX graph to GraphML
  4) Convert NX → igraph via GraphML
  5) Detect communities (Louvain or Leiden)
  6) Save community assignments to TXT
"""

import argparse
import networkx as nx
from datetime import datetime

from feature_builder.vectorizer import build_feature_vectors
from feature_builder.graph_builder import build_similarity_graph
from igraph_converter import convert_networkx_to_igraph_via_graphml
from clustering.community_detector import detect_communities
from fastconsensus.core import fast_consensus_clustering
from utils import group_partition_into_communities


def save_communities_txt(partition: dict, out_path: str):
    """
    Write communities (patient → community) into a human‐readable TXT file.
    """
    # Group by community
    communities = {}
    for pid, cid in partition.items():
        communities.setdefault(cid, []).append(pid)

    with open(out_path, 'w') as f:
        for cid, members in sorted(communities.items()):
            f.write(f"Community {cid} ({len(members)} patients):\n")
            for pid in members:
                f.write(f"  {pid}\n")
            f.write("\n")


def main():
    parser = argparse.ArgumentParser(
        description="Full pipeline: TTL → features → NX graph → igraph → communities"
    )
    parser.add_argument("ttl_path",
                        help="Path to the RDF Turtle file with ClinicalCase data")
    parser.add_argument("--threshold", type=float, default=None,
                        help="Similarity threshold (0–1) to filter edges; if omitted, keep all >0")
    parser.add_argument("--method", choices=["louvain", "leiden"], default="louvain",
                        help="Community detection method")
    parser.add_argument("--export-graphml",
                        help="Optional path to save the NX graph as GraphML")
    parser.add_argument("--output-txt", default=None,
                        help="Path to save community assignments (TXT). "
                             "Default: communities_<timestamp>.txt")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for Leiden (ignored by Louvain)")
    args = parser.parse_args()

    # Step 1: feature vectors
    print("[1] Extracting feature vectors...", flush=True)
    feature_vectors, patient_ids = build_feature_vectors(args.ttl_path)
    print(f"    → {len(patient_ids)} patients, {feature_vectors.shape[1]} features", flush=True)

    # Step 2: build NX similarity graph
    print("[2] Building similarity graph...", flush=True)
    nx_graph = build_similarity_graph(feature_vectors, patient_ids, threshold=args.threshold)
    print(f"    → {nx_graph.number_of_nodes()} nodes, {nx_graph.number_of_edges()} edges", flush=True)

    # Optional export to GraphML
    if args.export_graphml:
        print(f"[3] Exporting NX graph to GraphML at {args.export_graphml}", flush=True)
        nx.write_graphml(nx_graph, args.export_graphml)

    # Step 3: convert to igraph
    print("[4] Converting to igraph via GraphML...", flush=True)
    ig_graph = convert_networkx_to_igraph_via_graphml(nx_graph)

    partition = fast_consensus_clustering(ig_graph, n_partitions=20, threshold=0.2)

    # Save the communities to a TXT file
    output_path = args.output_txt or f"communities_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    save_communities_txt(partition, output_path)
    print(f"    → Communities saved to {output_path}", flush=True)

    print("Done.", flush=True)


if __name__ == "__main__":
    main()

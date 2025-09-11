#!/usr/bin/env python3
# miniscript_clustering.py

import argparse
import sys
import rdflib

from clustering.clustering import clustering_apply
import csv
import os
from datetime import datetime

def load_rdf_graph(ttl_path: str) -> rdflib.Graph:
    """Carga un grafo RDF desde un fichero .ttl."""
    g = rdflib.Graph()
    g.parse(ttl_path, format="turtle")
    return g

def main():
    parser = argparse.ArgumentParser(
        description="Mini-driver para elegir enfoque de clustering sobre un RDF TTL."
    )
    parser.add_argument("ttl_path", help="Ruta al fichero .ttl con el grafo RDF")
    parser.add_argument(
        "-m", "--method",
        choices=["kmeans"],
        required=True,
        help="Método a ejecutar"
    )
    parser.add_argument(
        "-n", "--nclusters",
        type=int,
        default=5,
        help="(Optional) Number of clusters (default=5)"
    )
    args = parser.parse_args()

    try:
        graph = load_rdf_graph(args.ttl_path)
    except Exception as e:
        print(f"[ERROR] No se pudo cargar el TTL ({args.ttl_path}): {e}", file=sys.stderr)
        sys.exit(1)

    clusters = clustering_apply(graph, args.method, args.nclusters)

    for cluster in clusters:
        print(f"Cluster {cluster}:")
        #for patient in clusters[cluster]:
        #    print(f"  - {patient}")
        #print()

    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    today_str = datetime.today().strftime("%Y%m%d")
    output_file = os.path.join(
        output_dir,
        f"{today_str}_{args.method}_{args.nclusters}.csv"
    )

    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Cluster", "PatientID"])
        for cluster in clusters:
            for patient in clusters[cluster]:
                writer.writerow([cluster, patient])
    print(f"CSV file saved to {output_file}")


if __name__ == "__main__":
    main()

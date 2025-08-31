#!/usr/bin/env python3
# miniscript_clustering.py

import argparse
import sys
import rdflib

from clustering.ward_clustering import run_ward
from clustering.spectral_clustering import run_spectral

def load_rdf_graph(ttl_path: str) -> rdflib.Graph:
    """Carga un grafo RDF desde un fichero .ttl."""
    g = rdflib.Graph()
    g.parse(ttl_path, format="turtle")
    return g

def main():
    parser = argparse.ArgumentParser(
        description="Mini-driver para elegir enfoque de clustering (WARD / SPECTRAL) sobre un RDF TTL."
    )
    parser.add_argument("ttl_path", help="Ruta al fichero .ttl con el grafo RDF")
    parser.add_argument(
        "-m", "--method",
        choices=["ward", "spectral"],
        required=True,
        help="Método a ejecutar"
    )
    args = parser.parse_args()

    try:
        graph = load_rdf_graph(args.ttl_path)
    except Exception as e:
        print(f"[ERROR] No se pudo cargar el TTL ({args.ttl_path}): {e}", file=sys.stderr)
        sys.exit(1)

    if args.method == "ward":
        run_ward(graph)
    elif args.method == "spectral":
        run_spectral(graph)
    else:
        print("[ERROR] Método no soportado.", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()

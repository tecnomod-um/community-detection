# clutering/ward_clustering.py

from typing import Tuple, List, Optional
import logging
import rdflib
import numpy as np

log = logging.getLogger(__name__)


def run_ward(graph: rdflib.Graph,
             n_clusters: Optional[int] = None,
             max_clusters: int = 15) -> None:
    """
    Orquesta el pipeline Ward:
    1) extrae la matriz de características desde el RDF,
    2) ejecuta el clustering Ward,
    3) muestra un resumen del resultado.

    Parámetros:
      - graph: grafo RDF ya cargado.
      - n_clusters: nº de clusters a usar. Si None, se decidirá internamente.
      - max_clusters: tope superior (solo se usa si n_clusters es None).
    """
    log.info("Ejecutando WARD")

    # 1) Extraer matriz de características (stub por ahora)
    feature_matrix, patient_ids = _extract_feature_matrix(graph)

    # 2) Ejecutar Ward (stub por ahora)
    labels, model, used_k = _perform_ward_clustering(
        feature_matrix,
        n_clusters=n_clusters,
        max_clusters=max_clusters
    )

    # 3) Resumen (stub por ahora)
    _print_ward_summary(labels, patient_ids, used_k)


# -----------------------
# Helpers internos (stubs)
# -----------------------

def _extract_feature_matrix(graph: rdflib.Graph) -> Tuple[np.ndarray, List[str]]:
    """
    Devuelve (feature_matrix, patient_ids) a partir del RDF.
      - feature_matrix: array (n_pacientes, n_features)
      - patient_ids: lista alineada con las filas de feature_matrix
    """
    raise NotImplementedError(
        "_extract_feature_matrix: pendiente de implementar. "
        "Debe construir la matriz de características y los IDs."
    )


def _perform_ward_clustering(feature_matrix: np.ndarray,
                             n_clusters: Optional[int],
                             max_clusters: int) -> Tuple[np.ndarray, object, int]:
    """
    Ejecuta el clustering jerárquico (Ward).
    Si n_clusters es None, debe elegir k (p.ej., por silhouette) en [2..max_clusters].

    Devuelve:
      - labels: np.ndarray de enteros (cluster por paciente)
      - model: objeto del modelo ajustado (para inspección)
      - used_k: entero con el nº de clusters finalmente usado
    """
    raise NotImplementedError(
        "_perform_ward_clustering: pendiente de implementar. "
        "Debe devolver (labels, model, used_k)."
    )


def _print_ward_summary(labels: np.ndarray,
                        patient_ids: List[str],
                        n_clusters_used: int) -> None:
    """
    Muestra un resumen legible (tamaños por cluster, ejemplos de IDs, etc.).
    """
    raise NotImplementedError(
        "_print_ward_summary: pendiente de implementar. "
        "Debe imprimir un breve resumen del resultado."
    )

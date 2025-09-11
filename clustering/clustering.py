from feature_builder.graph_analyzer import extract_patient_features, extract_patient_nodes, filter_features
from clustering.preprocess import preprocess_data_clustering
import argparse
from sklearn.cluster import KMeans
from clustering.community_detector import evaluate_modularity
import networkx as nx
import numpy as np
from sklearn.metrics import (
    silhouette_score, silhouette_samples,
    calinski_harabasz_score, davies_bouldin_score,
)

def clustering_apply(graph, method, nclusters=5):
    if method == "kmeans":
        preprocessed_df, patient_nodes = _clustering_apply_preprocess(graph)
        labels = kmeans_apply(preprocessed_df, nclusters)
        patient_labels = dict(zip(patient_nodes, labels))

        print("[DEBUG] K-means quick report:", flush=True)
        print(kmeans_quick_report(preprocessed_df, labels), flush=True)

        return reorganize_clusters(patient_labels)
    else:
        raise ValueError(f"Unknown clustering method: {method}. Use 'kmeans'.")

def _clustering_apply_preprocess(graph):
    ## Load RDF graph and extract patient features
    patient_nodes = extract_patient_nodes(graph)
    features_by_patient = extract_patient_features(graph, patient_nodes)
    
    filtered_features_by_patient = filter_features(features_by_patient)

    return preprocess_data_clustering(filtered_features_by_patient), patient_nodes # Receives dict, returns dataframe

def kmeans_apply(preprocessed_df, nclusters):
    kmeans = KMeans(n_clusters=nclusters, random_state=42)
    kmeans.fit(preprocessed_df)

    return kmeans.labels_

def reorganize_clusters(patient_labels):
    clusters = {}
    for patient, label in patient_labels.items():
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(patient)
    return clusters


def kmeans_quick_report(X, labels):
    """
    X: matriz/df de features (ya preprocesado)
    labels: array de clusters devuelto por k-means
    louvain_labels (opcional): array de comunidades de Louvain (mismo orden) para comparar
    """
    X = np.asarray(X)
    labels = np.asarray(labels)
    k = int(len(np.unique(labels)))
    out = {"n_samples": int(len(labels)), "n_clusters": k}

    # Métricas internas (solo si hay >=2 clusters y < n_samples)
    if 2 <= k < len(labels):
        s = silhouette_score(X, labels)
        s_samples = silhouette_samples(X, labels)
        out["silhouette"] = round(float(s), 3)
        out["silhouette_pct_negative"] = round(float((s_samples < 0).mean()), 3)
        out["calinski_harabasz"] = round(float(calinski_harabasz_score(X, labels)), 1)
        out["davies_bouldin"] = round(float(davies_bouldin_score(X, labels)), 3)
    else:
        out.update({
            "silhouette": None,
            "silhouette_pct_negative": None,
            "calinski_harabasz": None,
            "davies_bouldin": None
        })

    # Tamaños de cluster
    sizes = np.bincount(labels)  # k-means usa 0..k-1
    out.update({
        "sizes": sizes.tolist(),
        "min_cluster_size": int(sizes.min()),
        "max_cluster_size": int(sizes.max()),
        "largest_share_pct": round(100 * sizes.max() / sizes.sum(), 1),
    })

    return out
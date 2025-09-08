from feature_builder.graph_analyzer import extract_patient_features, extract_patient_nodes, filter_features
from clustering.preprocess import preprocess_data_clustering
import argparse
from sklearn.cluster import KMeans

def clustering_apply(graph, method, nclusters=5):
    if method == "kmeans":
        preprocessed_df, patient_nodes = _clustering_apply_preprocess(graph)
        labels = kmeans_apply(preprocessed_df, nclusters)

        patient_labels = dict(zip(patient_nodes, labels))
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
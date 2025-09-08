# feature_builder/vectorizer.py
import numpy as np
import pandas as pd
from .config import NAMESPACES
from sklearn.preprocessing import StandardScaler
from rdflib import URIRef
from feature_builder.graph_analyzer import extract_patient_nodes, extract_patient_features, load_rdf_graph


def build_feature_vectors(ttl_path):
    """
    Construye los vectores de características de los pacientes a partir del archivo RDF.

    :param ttl_path: Ruta al archivo .ttl con el grafo RDF
    :return: (feature_vectors, patient_ids)
    """
    graph = load_rdf_graph(ttl_path)
    patient_nodes = extract_patient_nodes(graph)
    patient_features = extract_patient_features(graph, patient_nodes)
    feature_vectors, patient_ids = _vectorize_features(patient_features)

    # if sort:
    #    patient_ids = sorted(patient_ids)
        
    return feature_vectors, patient_ids


def _vectorize_features(patient_features):
    """
    Convierte el diccionario de características en una matriz numérica y lista de IDs.
    :param patient_features: dict { patient_uri: [(feature_uri, value), ...] }
    :return: (feature_vectors (np.ndarray), patient_ids (list))
    """
    # Preparar filas de datos y lista de pacientes
    rows = []
    patient_ids = []
    for patient, features in patient_features.items():
        row = {}
        for feature_uri, value in features:
            if value is True:
                row[feature_uri] = 1
            else:
                try:
                    row[feature_uri] = float(value)
                except ValueError:
                    row[feature_uri] = str(value)
        rows.append(row)
        patient_ids.append(patient)

    # Crear DataFrame con pacientes como índice
    df = pd.DataFrame(rows, index=patient_ids).fillna(0)

    # Separar columnas por tipo
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    # Codificar categóricas con one-hot
    if categorical_cols:
        df_cat = pd.get_dummies(df[categorical_cols], prefix=categorical_cols, prefix_sep=':')
        df = pd.concat([df[numeric_cols], df_cat], axis=1)

    # Escalar columnas numéricas
    if numeric_cols:
        scaler = StandardScaler()
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    # Matriz de características y lista de IDs
    feature_vectors = df.values
    return feature_vectors, patient_ids

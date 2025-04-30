# feature_builder/vectorizer.py
import rdflib
import numpy as np
import pandas as pd
from .config import NAMESPACES
from sklearn.preprocessing import StandardScaler

# Cargar namespaces dinámicamente desde config
NS1 = rdflib.Namespace(NAMESPACES['ns1'])
NS2 = rdflib.Namespace(NAMESPACES['ns2'])
NS3 = rdflib.Namespace(NAMESPACES['ns3'])

# Predicado local para diagnosticar "hasValue"
def _is_has_value(predicate):
    pred_str = str(predicate)
    return pred_str.endswith("hasValue") or pred_str.split("/")[-1] == "hasValue" or pred_str.split("#")[-1] == "hasValue"


def build_feature_vectors(ttl_path, sort=True):
    """
    Construye los vectores de características de los pacientes a partir del archivo RDF.

    :param ttl_path: Ruta al archivo .ttl con el grafo RDF
    :return: (feature_vectors, patient_ids)
    """
    graph = _load_rdf_graph(ttl_path)
    patient_nodes = _extract_patient_nodes(graph)
    patient_features = _extract_patient_features(graph, patient_nodes)
    feature_vectors, patient_ids = _vectorize_features(patient_features)

    if sort:
        patient_ids = sorted(patient_ids)
        
    return feature_vectors, patient_ids


def _load_rdf_graph(ttl_path):
    graph = rdflib.Graph()
    graph.parse(ttl_path, format="turtle")
    return graph


def _extract_patient_nodes(graph):
    """
    Extrae todos los nodos de tipo ClinicalCase (ns3:ClinicalCase).
    """
    patient_nodes = set()
    for s in graph.subjects(rdflib.RDF.type, NS3.ClinicalCase):
        patient_nodes.add(s)
    return list(patient_nodes)


def _extract_patient_features(graph, patient_nodes):
    """
    Para cada paciente, recorre sus ns1:hasPart y extrae:
      - Observaciones (ns1:hasObservable + ns1:hasObservableValue → valor)
      - Situaciones clínicas (ns1:representsSituation como booleano True)
    Devuelve un dict { patient_uri: [(feature_uri, value), ...] }
    """
    features_by_patient = {}
    for patient in patient_nodes:
        features = []
        for part in graph.objects(patient, NS1.hasPart):
            # Observaciones
            for observable in graph.objects(part, NS1.hasObservable):
                value = None
                for val_node in graph.objects(part, NS1.hasObservableValue):
                    # Literal directo
                    if isinstance(val_node, rdflib.Literal):
                        value = str(val_node)
                    else:
                        # Nodo intermedio: buscar cualquier hasValue
                        for p, o in graph.predicate_objects(val_node):
                            if _is_has_value(p):
                                value = str(o)
                if value is not None:
                    features.append((str(observable), value))
            # Situaciones clínicas
            for situation in graph.objects(part, NS1.representsSituation):
                features.append((str(situation), True))
        features_by_patient[str(patient)] = features
    return features_by_patient


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

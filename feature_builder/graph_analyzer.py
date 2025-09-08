import rdflib
from .config import NAMESPACES
from rdflib import URIRef


# Cargar namespaces dinámicamente desde config
NS1 = rdflib.Namespace(NAMESPACES['ns1'])
NS2 = rdflib.Namespace(NAMESPACES['ns2'])
NS3 = rdflib.Namespace(NAMESPACES['ns3'])


def load_rdf_graph(ttl_path):
    graph = rdflib.Graph()
    graph.parse(ttl_path, format="turtle")
    return graph


def _extract_patient_nodes_namespace(graph):
    """
    NOT CURRENTLY USED.
    Extrae todos los nodos de tipo ClinicalCase (ns3:ClinicalCase).
    """
    patient_nodes = set()
    for s in graph.subjects(rdflib.RDF.type, NS3.ClinicalCase):
        patient_nodes.add(s)
    return list(patient_nodes)


def extract_patient_nodes(graph):
    """
    Extrae todos los nodos que son instancias de "ClinicalCase",
    sin depender de namespaces.
    Busca triples (?s rdf:type ?o) donde el nombre local de ?o sea "ClinicalCase".
    Retorna una lista de sujetos.
    """
    patient_nodes = set()
    for subj, _, obj in graph.triples((None, rdflib.RDF.type, None)):
        if isinstance(obj, URIRef):
            # Obtener el fragmento tras '#' o '/', para comparar el nombre local
            local_name = obj.split('#')[-1].split('/')[-1]
            if local_name == 'ClinicalCase':
                patient_nodes.add(subj)
    return list(patient_nodes)

def extract_patient_features(graph, patient_nodes):
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

# Predicado local para diagnosticar "hasValue"
def _is_has_value(predicate):
    pred_str = str(predicate)
    return pred_str.endswith("hasValue") or pred_str.split("/")[-1] == "hasValue" or pred_str.split("#")[-1] == "hasValue"


def filter_features(features):
    """
    Extracts the relevant part of the feature. Suited for certain preprocessings.
    For example, transforms:
    Patient: URI/PatientID
        Feature: (SnomedCT concept for Ischemic), Value: True
        Feature: (SnomedCT concept for Age), Value: 35
        Feature: (SnomedCT concept for AdmissionBarthel), Value: 75
        Feature: (SnomedCT concept for DischargeBarthel), Value: 80

    into:

    Patient: [(SnomedCT concept for Ischemic), 35, 75, 80]
    """

    filtered = {}

    for patient in features:
        if patient not in filtered.keys(): # We prioritize the first ocurrence
            patient_features = features[patient]
            patient_filtered_features = []

            for feature, value in patient_features:
                if value == True or value == False:
                    patient_filtered_features.append(str(feature)+"_"+str(value))
                else:
                    patient_filtered_features.append(value)
            
            filtered[patient] = patient_filtered_features

    return filtered

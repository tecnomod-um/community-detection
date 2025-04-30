from feature_builder.vectorizer import build_feature_vectors

def community_detection_main(ttl_path):
    """
    Función principal para ejecutar el proceso de community detection completo.
    - Carga el archivo .ttl con el grafo RDF.
    - Extrae y construye los vectores de características de los pacientes.
    - (Los siguientes pasos se implementarán en módulos adicionales más adelante)

    :param ttl_path: Ruta al archivo .ttl con el grafo RDF
    """

    # Paso 1: Construir los vectores de características desde el grafo RDF
    feature_vectors, patient_ids = build_feature_vectors(ttl_path)

    # Aquí, más adelante, se delegará la construcción del grafo de similitud,
    # la detección de comunidades y su evaluación

    print("Vectores de características construidos para", len(patient_ids), "pacientes.")
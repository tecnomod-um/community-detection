from feature_builder.vectorizer import build_feature_vectors

ttl_path = "RDF_guttman.ttl"
try:
    feature_vectors, patient_ids = build_feature_vectors(ttl_path)
    print(f"Pacientes encontrados: {len(patient_ids)}")
    print(f"Primeros pacientes: {patient_ids[:5]}")
except Exception as e:
    print("Error durante el procesamiento:", e)
# compare_patients.py

from feature_builder.vectorizer import build_feature_vectors
from sklearn.metrics.pairwise import cosine_similarity


def main():
    # Definir ruta al archivo TTL
    ttl_path = "file.ttl"

    # Construir matriz de características y lista de IDs de pacientes
    feature_vectors, patient_ids = build_feature_vectors(ttl_path)

    # Definir los pacientes a comparar (URI o identificador tal como aparece en patient_ids)
    pacienteA = "http://stratifai#Case_1"
    pacienteB = "http://stratifai#Case_2"

    # Obtener índices de los pacientes
    try:
        idxA = patient_ids.index(pacienteA)
        idxB = patient_ids.index(pacienteB)
    except ValueError as e:
        print(f"Error: no se encontró uno de los pacientes en la lista de IDs: {e}")
        return

    # Extraer vectores y calcular similitud coseno
    vecA = feature_vectors[idxA].reshape(1, -1)
    vecB = feature_vectors[idxB].reshape(1, -1)
    sim = cosine_similarity(vecA, vecB)[0][0]

    print(f"Similitud coseno entre {pacienteA} y {pacienteB}: {sim:.4f}")


if __name__ == "__main__":
    main()

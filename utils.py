def group_partition_into_communities(partition: dict) -> dict:
    """
    Agrupa los pacientes por comunidad a partir de la partición dada.

    :param partition: Diccionario { patient_id: community_id }
    :return: Diccionario { community_id: [patient_ids] }
    """
    communities = {}
    for patient, comm_id in partition.items():
        communities.setdefault(comm_id, []).append(patient)
    
    return communities
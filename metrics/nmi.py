from sklearn.metrics import normalized_mutual_info_score

def nmi_communities(array_of_dicts: list) -> float:
    
    # Check input validity
    if array_of_dicts is None or len(array_of_dicts) < 2:
        raise ValueError("NMI requires at least two partitions to compare.")

    # Convert list of dicts to list of lists
    all_nodes = set()
    for partition in array_of_dicts:
        all_nodes.update(partition.keys())
    all_nodes = sorted(all_nodes)

    # Contains a list of community labels for each partition
    label_lists = []
    for partition in array_of_dicts:
        labels = [partition.get(node, -1) for node in all_nodes]
        label_lists.append(labels)

    # Calculate pairwise NMI and average
    nmi_values = []
    for i in range(len(label_lists)):
        print("...Calculating NMI for partition", i)
        for j in range(i + 1, len(label_lists)):
            nmi = normalized_mutual_info_score(label_lists[i], label_lists[j])
            nmi_values.append(nmi)

    average_nmi = sum(nmi_values) / len(nmi_values) if nmi_values else 0.0
    return average_nmi
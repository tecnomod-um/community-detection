import csv
from sklearn.metrics import normalized_mutual_info_score

def read_results(file_path, id_column, label_column):
    results = {}
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            results[row[id_column]] = row[label_column]
    return results

def compare_clusterings(file_path1, file_path2, id_column1, id_column2, label_column1, label_column2):
    clustering1 = read_results(file_path1, id_column1, label_column1)
    clustering2 = read_results(file_path2, id_column2, label_column2)

    all_ids = set(clustering1.keys()).union(set(clustering2.keys()))

    labels1 = []
    labels2 = []

    for id in all_ids:
        labels1.append(clustering1.get(id, -1))
        labels2.append(clustering2.get(id, -1))

    nmi = normalized_mutual_info_score(labels1, labels2)
    return nmi

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Compara dos resultados de clustering usando NMI.')
    parser.add_argument('file1', help='Ruta al primer archivo CSV')
    parser.add_argument('file2', help='Ruta al segundo archivo CSV')
    parser.add_argument('--id_column1', default='patient_id', help='Nombre de la columna de IDs en el primer archivo')
    parser.add_argument('--id_column2', default='patient_id', help='Nombre de la columna de IDs en el segundo archivo')
    parser.add_argument('--label_column1', default='community_id', help='Nombre de la columna de etiquetas en el primer archivo')
    parser.add_argument('--label_column2', default='community_id', help='Nombre de la columna de etiquetas en el segundo archivo')
    args = parser.parse_args()

    nmi_score = compare_clusterings(
        args.file1,
        args.file2,
        args.id_column1,
        args.id_column2,
        args.label_column1,
        args.label_column2
    )

    print(f"NMI entre los dos clusterings: {nmi_score:.4f}")
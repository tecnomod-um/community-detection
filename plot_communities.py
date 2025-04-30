#!/usr/bin/env python3
import matplotlib.pyplot as plt

def read_communities(file_path):
    """
    Lee el archivo communities.txt y devuelve un diccionario
    donde la clave es el ID de la comunidad y el valor es el número de miembros.
    
    Se asume que el archivo tiene el formato:
      Comunidad <id>:
        <nodo>
        <nodo>
      Comunidad <id>:
        <nodo>
        ...
    """
    communities = {}
    current_comm = None
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("Comunidad"):
                # Extraer el identificador de la comunidad (se espera el formato "Comunidad <id>:")
                parts = line.split()
                if len(parts) >= 2:
                    comm_id = parts[1].strip(":")
                    current_comm = comm_id
                    communities[current_comm] = 0
            elif line and current_comm is not None:
                # Cada línea que no esté vacía y esté indentada se considera un nodo de la comunidad actual.
                communities[current_comm] += 1
            elif not line:
                # Línea en blanco: fin de la sección de una comunidad.
                current_comm = None
    return communities

def plot_communities(communities):
    """
    Genera un gráfico de barras con la cantidad de miembros por comunidad.
    """
    # Extraer IDs y sus respectivos conteos
    comm_ids = list(communities.keys())
    counts = [communities[comm] for comm in comm_ids]

    # Crear el gráfico de barras
    plt.figure(figsize=(10, 6))
    plt.bar(comm_ids, counts, color='skyblue')
    plt.xlabel("Comunidad")
    plt.ylabel("Número de miembros")
    plt.title("Cantidad de miembros por comunidad")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("communities_count.png")
    plt.show()

def main():
    file_path = "communities.txt"
    communities = read_communities(file_path)
    print("Cantidad de miembros por comunidad:")
    for comm, count in communities.items():
        print(f"Comunidad {comm}: {count} miembros")
    plot_communities(communities)

if __name__ == "__main__":
    main()

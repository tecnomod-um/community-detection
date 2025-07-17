# Patient Community Detection Pipeline

This repository provides a modular pipeline for detecting and analyzing patient communities from RDF-based clinical data. It includes tools for feature extraction, graph construction, community detection, consensus analysis, and visualization.

---

## Requirements

- **Python 3.8+**
- rdflib
- pandas
- numpy
- scikit-learn
- networkx
- python-louvain (`community`)
- matplotlib

You can install the required packages via:

```
pip install rdflib pandas numpy scikit-learn networkx python-louvain matplotlib
```

---

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/your_org/patient-community-detection.git
   cd patient-community-detection
   ```
2. Install dependencies:
   ```
   pip install rdflib pandas numpy scikit-learn networkx python-louvain matplotlib
   ```

---

## Usage

All scripts assume you have an RDF Turtle file containing patient data, e.g. `patients.ttl`.

### 1. community_detection_main.py
Runs the full pipeline (vectors → similarity graph → communities → modularity → save results):

```
python community_detection_main.py patients.ttl --threshold 0.5 --method louvain
```

- **ttl_path**: Path to `.ttl` file  
- **--threshold**: Similarity threshold for graph edges. Edges between patients with lesser similarity values are ignored. 
- **--method**: `louvain`

Outputs:
- Console logs for each step  
- `communities_<timestamp>.txt` with community assignments  

### 2. compare_patients.py
Compute pairwise similarity between two specified patients:

```
python compare_patients.py
```

Edit `compare_patients.py` to set:
```
pacienteA = "...#Case_1"
pacienteB = "...#Case_2"
```
and run:
```
python compare_patients.py
```

### 3. consensus_communities.py
Builds a co-occurrence matrix over multiple runs to assess stability:

```bash
python consensus_communities.py data/patients.ttl --threshold 0.5 --method louvain --runs 20 --output consensus.csv
```

- **--runs**: Number of iterations (default: 20)  
- **--output**: Output CSV path  

Generates a CSV where each cell `(i,j)` counts the number of times two patients co-occur in the same community.

### 4. community/visualization.py
Visualize communities as a network graph:

```
from community.visualization import visualize_communities
visualize_communities(G, partition, output_path='coms.png', show_edges=False)
```

- **show_edges**: Toggle edge drawing for clarity  
- **output_path**: File path for PNG output  

---

## Module Overview

### feature_builder/
- **config.py**: Namespace URIs for RDF parsing  
- **vectorizer.py**: `build_feature_vectors(ttl_path)` → extracts patient features and vectorizes into a NumPy matrix  
- **graph_builder.py**: `build_similarity_graph(feature_vectors, patient_ids, threshold)` → builds a weighted NetworkX graph based on cosine similarity  

### community/
- **community_detector.py**: `detect_communities(G, method)` → Louvain method; `evaluate_modularity(G, partition)` → computes modularity  
- **visualization.py**: `visualize_communities(G, partition, output_path, show_edges, figsize)` → renders and saves a graph image  

| Script                        | Description                                                      |
|-------------------------------|------------------------------------------------------------------|
| `community_detection_main.py` | Full pipeline: vectorize → graph → detect → evaluate → save txt  |
| `compare_patients.py`         | Compute and print cosine similarity between two patients         |
| `consensus_communities.py`    | Run multiple community detections and export co-occurrence CSV   |

---

import tempfile
import os
import networkx as nx
import igraph as ig

def convert_networkx_to_igraph_via_graphml(nx_graph: nx.Graph) -> ig.Graph:
    """
    Convert a NetworkX graph into an igraph Graph by round-tripping through GraphML.

    :param nx_graph: A NetworkX Graph or DiGraph with node and edge attributes.
    :return: An igraph Graph with the same structure and edge weights.
    """
    # 1. Create a temporary file to hold the GraphML export
    tmp_file = tempfile.NamedTemporaryFile(suffix=".graphml", delete=False)
    tmp_path = tmp_file.name
    tmp_file.close()

    try:
        # 2. Write the NetworkX graph to GraphML
        nx.write_graphml(nx_graph, tmp_path)

        # 3. Read the GraphML file into igraph
        ig_graph = ig.Graph.Read_GraphML(tmp_path)
        if "id" in ig_graph.vs.attribute_names():
            ig_graph.vs["name"] = ig_graph.vs["id"]

    finally:
        # 4. Remove the temporary file
        os.remove(tmp_path)

    return ig_graph

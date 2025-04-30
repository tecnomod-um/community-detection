# community/visualization.py
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from datetime import datetime


def visualize_communities(G: nx.Graph,
                          partition: dict,
                          output_path: str = None,
                          show_edges: bool = True,
                          figsize: tuple = (10, 10)):
    """
    Generates a plot of patient communities within the graph.

    :param G: NetworkX graph with patient nodes.
    :param partition: Dictionary { patient_id: community_id }.
    :param output_path: Path to save the image. If None, it automatically saves as 'communities_<timestamp>.png'.
    :param show_edges: If False, edges are not drawn for clarity.
    :param figsize: Figure size (width, height).
    """
    # Compute node positions
    pos = nx.spring_layout(G, seed=42)

    # Node colors by community
    node_colors = [partition.get(node, 0) for node in G.nodes()]
    unique_communities = sorted(set(node_colors))
    color_map = cm.get_cmap('viridis', max(unique_communities) + 1)

    # Create figure
    plt.figure(figsize=figsize)

    # Draw edges optionally
    if show_edges:
        nx.draw_networkx_edges(G, pos,
                               alpha=0.2,
                               edge_color='gray')

    # Draw nodes
    nodes = nx.draw_networkx_nodes(G, pos,
                                   node_color=node_colors,
                                   cmap=color_map,
                                   node_size=50,
                                   alpha=0.9)

    # Create legend
    for community in unique_communities:
        plt.scatter([], [], c=[color_map(community)], label=f'Community {community}', s=50)

    plt.legend(scatterpoints=1, frameon=False, labelspacing=0.5, title="Communities")

    plt.title("Patient Communities")
    plt.axis('off')

    # Automatic name if no output_path
    if not output_path:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"communities_{timestamp}.png"

    # Save figure
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"Graph saved at: {output_path}")
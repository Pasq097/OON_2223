import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


def connectivity_matrix_graph(list_of_connected_nodes):
    # Get the unique nodes
    counter = {}
    for conn in list_of_connected_nodes:
        if conn in counter:
            counter[conn] += 1
        else:
            counter[conn] = 1
    print(counter)
    nodes = set([node[0] for node in list_of_connected_nodes] + [node[1] for node in list_of_connected_nodes])
    nodes = sorted(list(nodes))
    print(nodes)

    # Create a matrix to store the frequency of each connection
    conn_matrix = np.zeros((len(nodes), len(nodes)))

    # Fill the matrix with the frequency of each connection
    for node1, node2 in list_of_connected_nodes:
        i = nodes.index(node1)
        j = nodes.index(node2)
        conn_matrix[i, j] += 1

    conn_matrix_norm = conn_matrix / conn_matrix.max()

    # Plot the matrix in 3D

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x, y = np.meshgrid(range(conn_matrix_norm.shape[0]), range(conn_matrix_norm.shape[1]))
    color = cm.viridis((conn_matrix_norm.flatten() - np.min(conn_matrix_norm)) / (np.max(conn_matrix_norm) - np.min(conn_matrix_norm)))
    surf = ax.bar3d(x.flatten(), y.flatten(), np.zeros(conn_matrix_norm.size), 0.5, 0.5, conn_matrix_norm.flatten(), color=color)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    # A StrMethodFormatter is used automaticall
    plt.title('connectivity matrix graph')
    plt.xlabel('input nodes')
    plt.ylabel('output nodes')

    ax.set_zlabel('intensity')
    ax.set_xticks(range(len(nodes)))
    ax.set_xticklabels(nodes)
    ax.set_yticks(range(len(nodes)))
    ax.set_yticklabels(nodes)
    plt.show()

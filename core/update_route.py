import numpy as np


def update_route(path, lines, nodes):
    # This function rebuild all the route space from scratch
    result = np.ones(10, dtype=int)
    state = []
    blocks = []
    lines_of_path = [''.join(pair) for pair in zip(path[:-1], path[1:])]
    for temporary in lines_of_path:
        state.append(lines[temporary].state)
    nodes_for_swm = path.lstrip(path[0]).rstrip(path[-1])
    for n_swm in nodes_for_swm:
        index_swm = path.index(n_swm)
        blocks.append(nodes[n_swm].switching_matrix[path[index_swm - 1]][path[index_swm + 1]])
    for arr in state:
        if len(blocks) != 0:
            for block in blocks:
                x = arr
                y = block
                result = result * x * y
        else:
            x = arr
            # print(x)
            result = result*x

    return result

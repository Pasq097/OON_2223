
def checking_ch(dict, nodes_swm, dict_nodes, path_of_cu_iter):
    # for each path it has to check the CH availability for each line
    # e.g. A->C->D check free CH on AC and free CH on CD
    # dict = {'AB': [0, 1, 0, 1], 'BC': [0, 1, 1, 0], 'CD':[0 ,1 ,1 ,1]}
    # print(dict)
    flag = 0
    # print('node_swm_are' + nodes_swm)
    # print(dict)
    list_of_channels = list(dict.values())
    # print(list_of_channels)
    blocks = []
    # print(path_of_cu_iter)
    if nodes_swm == '':
        for k in range(0, 10):
            a = [item[k] for item in list_of_channels]
            if all(ele == a[0] and ele == 1 for ele in a):
                flag = 1
                break
            else:
                flag = 0
    else:

        for swm in nodes_swm:
            index_swm = path_of_cu_iter.index(swm)
            block = (dict_nodes[swm].switching_matrix[path_of_cu_iter[index_swm - 1]][path_of_cu_iter[index_swm + 1]])
            blocks.append(block)
        # print(blocks)
        for k in range(0, 10):
            a = [item[k] for item in list_of_channels]
            b = [item[k] for item in blocks]
            # print(a)

            if all(ele == a[0] and ele == 1 for ele in a) and all(ele2 == b[0] and ele2 == 1 for ele2 in b):
                flag = 1
                break
            else:
                flag = 0
    # print('kis '+ str(k))
    return flag, k

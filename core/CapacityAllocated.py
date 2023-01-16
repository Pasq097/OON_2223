import matplotlib.pyplot as plt


def total_capacity_allocated(route_space):
    # search all the two nodes paths
    res = list(route_space[0].index)

    list_of_path = []
    for a in res:
        if len(a) == 4:
            list_of_path.append(a)
    list_of_ch = []
    for x in list_of_path:
        h = list(route_space[0].loc[x])
        list_of_ch.append(h)
    print(list_of_ch)
    occurrences = []
    for var in list_of_ch:
        x = var.count(0)
        occurrences.append(x)
    print(len(occurrences))
    plt.bar(list_of_path, occurrences, width=0.8, bottom=None, align='center', data=None)
    plt.title('total capacity allocated into the network')
    plt.ylabel('total channels allocated')
    plt.xlabel('line')

    plt.show()

    return list_of_ch
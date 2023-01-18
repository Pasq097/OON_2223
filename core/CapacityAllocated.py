import matplotlib.pyplot as plt


def total_capacity_allocated(route_space):
    # search all the two nodes paths
    res = list(route_space[0].index)
    zeros_list = []
    list_of_path = []
    for a in res:
        if len(a) == 4:
            list_of_path.append(a)

    for df in route_space:
        zeros_count = [df.loc[path].eq(0).sum() for path in list_of_path]
        zeros_list.append(zeros_count)
    average_list = []
    for i in range(len(zeros_list[0])):
        values = [sub_list[i] for sub_list in zeros_list]
        average = sum(values)/len(values)
        average_list.append(average)
    plt.bar(list_of_path, average_list, width=0.8, bottom=None, align='center', data=None)
    plt.title('total capacity allocated into the network')
    plt.ylabel('total channels allocated')
    plt.xlabel('line')

    plt.show()


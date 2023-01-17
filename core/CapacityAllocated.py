import matplotlib.pyplot as plt


def total_capacity_allocated(route_space):
    # search all the two nodes paths
    print(route_space)
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
    # print(average_list)
    # print(len(average_list))
    #
    # print(zeros_list)
    # print(len(zeros_list[0]))
    #
    # print(res)
    # print(len(res))
    # occurrences = []
    # tot = []
    # for i in route_space:
    #     for x in res:
    #         h = list(i.loc[x])
    #         xx = h.count(0)
    #         occurrences.append(xx)
    #     tot.append(occurrences)
    # list_of_path = []
    # for a in res:
    #     if len(a) == 4:
    #         list_of_path.append(a)
    # list_of_ch = []
    # for x in list_of_path:
    #     h = list(route_space[0].loc[x])
    #     list_of_ch.append(h)
    # #print(list_of_ch)
    # occurrences = []
    # for var in list_of_ch:
    #     x = var.count(0)
    #     occurrences.append(x)
    # print(len(occurrences))
    plt.bar(list_of_path, average_list, width=0.8, bottom=None, align='center', data=None)
    plt.title('total capacity allocated into the network')
    plt.ylabel('total channels allocated')
    plt.xlabel('line')

    plt.show()

    #return list_of_ch
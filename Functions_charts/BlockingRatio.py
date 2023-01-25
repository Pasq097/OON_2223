import matplotlib.pyplot as plt


def blocking_ratio_hist(all_blocked_connections, all_conn_request, M):
    x = M
    blocking_ratio = []
    for x, y in zip(all_blocked_connections, all_conn_request):
        blocking_ratio.append((x / y) * 100)
    x_axis = list(range(x + 1))
    average = sum(blocking_ratio[x:]) / len(blocking_ratio[x:])
    y_axis = blocking_ratio[:x] + [average for i in range(x, len(x_axis))]
    plt.title("Blocking ratio respect to M")
    plt.ylabel('blocking ratio [%]', fontweight='bold')
    plt.xlabel('M', fontweight='bold')
    plt.plot(x_axis, y_axis)

    # spl = splrep(x_axis, y_axis)
    # new_points = 1000
    # new_x = np.linspace(min(x_axis), max(x_axis), new_points)
    # new_y = splev(new_x, spl)
    # plt.plot(new_x, new_y, '-')



    return plt

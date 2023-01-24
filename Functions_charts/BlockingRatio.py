import matplotlib.pyplot as plt


def blocking_ratio_hist(all_blocked_connections, all_conn_request, M):
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

    return plt

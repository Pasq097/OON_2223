import matplotlib.pyplot as plt


def block_conn(M, y):
    x = M
    x_axis = list(range(x + 1))
    average = sum(y[x:]) / len(y[x:])
    y_axis = y[:x] + [average for i in range(x, len(x_axis))]
    plt.title("Average of blocked connections with increasing M value")
    plt.ylabel('blocked connections', fontweight='bold')
    plt.xlabel('M', fontweight='bold')
    plt.plot(x_axis, y_axis)
    plt.show()

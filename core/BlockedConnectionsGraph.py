import matplotlib.pyplot as plt


def block_conn(x, y):
    x_axis = list(range(x+1))
    print(x_axis)
    plt.plot(x_axis[:x], y[:x], 'bo')
    average = sum(y[x:]/len(y[x:]))
    plt.plot(x_axis[x:], [average for i in x_axis[x:]], 'ro')

    plt.show()

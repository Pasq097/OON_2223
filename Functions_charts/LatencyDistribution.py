import matplotlib.pyplot as plt


def latency_hist(list_of_latency):
    res = list(filter(lambda item: item is not None, list_of_latency))
    plt.xlabel('latency', fontweight='bold')
    plt.ylabel('occurrences', fontweight='bold')
    plt.title("Latency distribution")
    plt.hist(res, bins=12)
    plt.show()

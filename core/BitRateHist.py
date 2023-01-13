import matplotlib.pyplot as plt
from statistics import mean


def bit_rate_hist(bit_rate_list):
    bit_rate_avg = mean(bit_rate_list)
    plt.title("Bit rate distribution")
    plt.ylabel('occurrences', fontweight='bold')
    plt.xlabel('bit-rate', fontweight='bold')
    plt.hist(bit_rate_list, bins=12)
    plt.axvline(bit_rate_avg, color='k', linestyle='dashed', linewidth=1)
    plt.show()

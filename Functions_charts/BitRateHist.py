import matplotlib.pyplot as plt
from statistics import mean


def bit_rate_hist(bit_rate_list):
    bit_rate_list_avg = []
    for list2 in bit_rate_list:
        bit_rate_avg = mean(list2)
        bit_rate_list_avg.append(bit_rate_avg)
    bit_rate_avg = mean(bit_rate_list_avg)
    plt.title("Bit rate distribution")
    plt.ylabel('occurrences', fontweight='bold')
    plt.xlabel('bit-rate', fontweight='bold')
    plt.hist(bit_rate_list_avg, bins=12)
    plt.axvline(bit_rate_avg, color='k', linestyle='dashed', linewidth=1)
    return plt

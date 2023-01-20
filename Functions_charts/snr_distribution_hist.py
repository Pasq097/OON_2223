import matplotlib.pyplot as plt
from statistics import mean


def snr_hist(list_snr):
    list_of_avg = []
    for val in list_snr:
        snr_rate_avg = mean(val)
        list_of_avg.append(snr_rate_avg)
    # avg = mean(list_of_avg)
    res = list(filter(lambda item: item != 0, list_snr))
    plt.xlabel('SNR [dB]', fontweight='bold')
    plt.ylabel('occurrences', fontweight='bold')
    plt.title("SNR distribution")
    plt.hist(res, bins=18)
    plt.show()

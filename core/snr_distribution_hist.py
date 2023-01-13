import matplotlib.pyplot as plt


def snr_hist(list_snr):
    res = list(filter(lambda item: item != 0, list_snr))
    plt.xlabel('SNR [dB]', fontweight='bold')
    plt.ylabel('occurrences', fontweight='bold')
    plt.title("SNR distribution")
    plt.hist(res, bins=12)
    plt.show()

import matplotlib.pyplot as plt


def snr_mc(list_snr_tot):
    plt.title("SNR MONTE CARLO")
    plt.ylabel('occurrences', fontweight='bold')
    plt.xlabel('SNR avarage [dB] ', fontweight='bold')
    plt.hist(list_snr_tot, bins=30)
    # plt.axvline(bit_rate_avg, color='k', linestyle='dashed', linewidth=1)
    plt.show()


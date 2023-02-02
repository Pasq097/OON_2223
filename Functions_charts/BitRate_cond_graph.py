import matplotlib.pyplot as plt


def bit_rate_cond():
    x1 = 13.88
    x2 = 17.79
    x3 = 20.62
    x = [0, x1, x2, x3, x3 + 1]
    y = [0, 0, 100, 200, 400]
    plt.xlabel('GSNR [dB]')
    plt.ylabel('bit-rate [Gbps]')
    plt.step(x, y)
    plt.show()


bit_rate_cond()

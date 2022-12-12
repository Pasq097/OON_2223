
def checking_ch(dict):
    # for each path it has to check the CH availability for each line
    # e.g. A->C->D check free CH on AC and free CH on CD
    # dict = {'AB': [0, 1, 0, 1], 'BC': [0, 1, 1, 0], 'CD':[0 ,1 ,1 ,1]}
    flag = 0
    # print(dict)
    list_of_channels = list(dict.values())
    # print(list_of_channels)
    for k in range(0, 10):
        a = [item[k] for item in list_of_channels]
        if all(ele == a[0] and ele == 1 for ele in a):
            flag = 1
            break
        else:
            flag = 0
    return flag, k

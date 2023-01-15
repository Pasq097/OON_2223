import matplotlib.pyplot as plt


def allocation_per_link(mtrx_start, mtrx_fin):
    result = {}
    # print('ciao')
    # print(mtrx_start)
    # print('ciao')
    # print(mtrx_fin)
    for mtrx_fin in mtrx_fin:
        for key, value in mtrx_start.items():
            result[key] = {}
            for sub_key, sub_value in value.items():
                result[key][sub_key] = mtrx_start[key][sub_key] - mtrx_fin[key][sub_key]
    # print(result)
    new_dictionary = {str((k, k1)): v1 for k, v in result.items() for k1, v1 in v.items()}
    plt.figure(figsize=(30, 200))
    plt.bar(new_dictionary.keys(), new_dictionary.values(), width=0.5, color='g')

    return plt

import matplotlib.pyplot as plt


def allocation_per_link(mtrx_start, mtrx_fin):
    result = {}
    total_result = {}
    count = len(mtrx_fin)
    for mtrx_fin in mtrx_fin:
        for key, value in mtrx_start.items():
            result[key] = {}
            for sub_key, sub_value in value.items():
                result[key][sub_key] = mtrx_start[key][sub_key] - mtrx_fin[key][sub_key]
                if key not in total_result:
                    total_result[key] = {}
                if sub_key not in total_result[key]:
                    total_result[key][sub_key] = 0
                total_result[key][sub_key] += result[key][sub_key]
    average_result = {key: {sub_key: value/count for sub_key, value in sub_dict.items()} for key, sub_dict in
                      total_result.items()}
    fig, ax = plt.subplots()
    plt.title("Data allocated for the possible connection")
    plt.ylabel('100 * M [Gbps]', fontweight='bold')
    new_dictionary_2 = {str((k, k1)): v1 for k, v in mtrx_start.items() for k1, v1 in v.items()}
    ax.bar(new_dictionary_2.keys(), new_dictionary_2.values(), width=0.5, color='r', label='mtrx_start')
    new_dictionary = {str((k, k1)): v1 for k, v in average_result.items() for k1, v1 in v.items()}
    # plt.figure(fig-size=(30, 200))
    ax.bar(new_dictionary.keys(), new_dictionary.values(), width=0.5, color='g')

    return plt

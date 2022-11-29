
def checking_ch(dict):
    # for each path it has to check the CH availability for each line
    # e.g. A->C->D check free CH on AC and free CH on CD
    flag = 1

    for i in range(0,9):
        for k in dict:
            if dict[k][i] == 0:
                linea_occ = 1

    for temp in possible_lines:
        if len(possible_lines) == 0:
            break
        else:
            ch_vector = lines[temp].state


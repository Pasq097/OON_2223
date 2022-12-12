def check_the_lines(path_to_check, lines):
    flag = 1
    # print("the path to check is " + path_to_check)
    # check if all the lines in the path given in are all free
    possible_lines = [''.join(pair) for pair in zip(path_to_check[:-1], path_to_check[1:])]
    for temp3 in possible_lines:
        if len(possible_lines) == 0:
            break
        else:
            if lines[temp3].state == 0:
                flag = 0
    return flag

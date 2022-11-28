def check_the_lines(path_to_check, lines):
    flag = 1
    # print("the path to check is " + path_to_check)
    # check if all the lines in the path given in are all free
    possible_lines = [''.join(pair) for pair in zip(path_to_check[:-1], path_to_check[1:])]

    for temp3 in possible_lines:
        # print("the line to check is "+temp3)
        # print("the state is")
        # print(lines[temp3].state)
        if len(possible_lines) == 0:
            break
        else:
            if lines[temp3].state == 0:
                flag = 0
    # print("the flag for the path "+ path_to_check + " is")
    # print(flag)
    return flag

def pairing(list_top, list_bottom, list_id):
    old_list = list_top + list_bottom
    new_list = sorted(old_list, key=lambda x: x.ranking, reverse=False)
    new_list = sorted(new_list, key=lambda x: x.points, reverse=True)
    new_list_top = []
    new_list_bottom = []

    while new_list:
        for i in range(1, len(new_list)):
            if int(new_list[0].t_id) < int(new_list[i].t_id):
                j = str(int(new_list[0].t_id)) + str(int(new_list[i].t_id))
            else:
                j = str(int(new_list[i].t_id)) + str(int(new_list[0].t_id))
            if j not in list_id or len(new_list) == 2:
                new_list_bottom = new_list_bottom + [new_list.pop(i)]
                new_list_top = new_list_top + [new_list.pop(0)]
                break
    return new_list_top, new_list_bottom


def pairing_r1(player_list):
    player_list = sorted(player_list, key=lambda x: x.ranking, reverse=False)
    new_list_top = []
    new_list_bottom = []
    new_list_top += [player_list[0]] + [player_list[1]] + \
        [player_list[2]] + [player_list[3]]
    new_list_bottom += [player_list[4]] + [player_list[5]] +\
        [player_list[6]] + [player_list[7]]

    return new_list_top, new_list_bottom

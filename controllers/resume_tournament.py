from datetime import datetime

from .controllers import create_match, create_round_loop
from .pairing import pairing
from .save_load import save_data
from .tinydb_data import add_tournament_data
from view.views import View

view = View()


def convert_to_tuple(tournament, c_round):
    # Converts serialized matches' results back to tuples to respect the
    # requested format.
    for i in range(0, c_round + 1):
        if i == 0:
            r = tournament.r1_result
            t = []
            for j in range(0, len(r)):
                t1 = tuple(r[j])
                t += [t1]
            tournament.r1_result = t
        elif i == 1:
            r = tournament.r2_result
            t = []
            for j in range(0, len(r)):
                t1 = tuple(r[j])
                t += [t1]
            tournament.r2_result = t
        elif i == 2:
            r = tournament.r3_result
            t = []
            for j in range(0, len(r)):
                t1 = tuple(r[j])
                t += [t1]
            tournament.r3_result = t
        elif i == 3:
            r = tournament.r4_result
            t = []
            for j in range(0, len(r)):
                t1 = tuple(r[j])
                t += [t1]
            tournament.r4_result = t

    return tournament


def partial_round(tournament, player_list_top, player_list_bottom, match_id,
                  matchs_played, matchs, matchs_list):
    results = []
    j = 0
    for i in range((4 - matchs), 4):
        match = create_match(player_list_top[i], player_list_bottom[i],
                             matchs_played)
        if match == 0:
            return results, match_id, matchs_played, 0
        else:
            matchs_played = match[3]
            match_id += match[2]
            results.append(([player_list_top[i].name, match[0]],
                           [player_list_bottom[i].name, match[1]]))
            tournament.matchs_list.append(matchs_list[j])
        j += 1

    return results, match_id, matchs_played


def partial_tournament(player_list_top, player_list_bottom, tournament,
                       match_id, matchs_played, round_name_l, round_start_l):
    if matchs_played < 4:
        c_round = 0
    elif matchs_played < 8:
        c_round = 1
    elif matchs_played < 12:
        c_round = 2
    elif matchs_played < 16:
        c_round = 3
    tournament = convert_to_tuple(tournament, c_round)
    matchs = 4 * (c_round + 1) - matchs_played
    if matchs % 4 == 0:
        x = 0
        for i in range(c_round, tournament.turns):
            matchs_list = []
            if x == 0:
                round_name = round_name_l
            else:
                message = "Nom du round : "
                round_name = view.display_in(message)
            x += 1
            pairs = pairing(player_list_top, player_list_bottom, match_id)
            player_list_top = pairs[0]
            player_list_bottom = pairs[1]
            message = f"Round {str(i + 1)}"
            view.display_out(message)
            for j in range(0, 4):
                message = (f"{player_list_top[j].name} "
                           f"{player_list_top[j].surname} "
                           f"vs "
                           f"{player_list_bottom[j].name} "
                           f"{player_list_bottom[j].surname}")
                view.display_out(message)
                matchs_list += [f"{player_list_top[j].name} "
                                f"{player_list_top[j].surname} "
                                f"vs "
                                f"{player_list_bottom[j].name} "
                                f"{player_list_bottom[j].surname}"]
            message = "Appuyez sur Entrée pour commencer le round..."
            view.display_in(message)
            round_start = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            r_result = create_round_loop(tournament, player_list_top,
                                         player_list_bottom, match_id,
                                         matchs_played, matchs_list)
            match_id = r_result[1]
            matchs_played = r_result[2]
            if i == 0:
                tournament.r1_result += r_result[0]
            elif i == 1:
                tournament.r2_result += r_result[0]
            elif i == 2:
                tournament.r3_result += r_result[0]
            elif i == 3:
                tournament.r4_result += r_result[0]
            if len(r_result) == 4:
                message = "Tournoi mis en pause"
                view.display_out(message)
                save_data(player_list_top, player_list_bottom, tournament,
                          match_id, matchs_played, round_name, round_start)
            round_end = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            tournament.rounds_list.append([round_name, round_start, round_end])
    elif 0 < matchs < 4:
        matchs_list = []
        message = f"Round {str(c_round + 1)}"
        view.display_out(message)
        for k in range((4 - matchs), 4):
            message = (f"{player_list_top[k].name} "
                       f"{player_list_top[k].surname} "
                       f"vs "
                       f"{player_list_bottom[k].name} "
                       f"{player_list_bottom[k].surname}")
            view.display_out(message)
            matchs_list += [f"{player_list_top[k].name} "
                            f"{player_list_top[k].surname} "
                            f"vs "
                            f"{player_list_bottom[k].name} "
                            f"{player_list_bottom[k].surname}"]
        message = "Appuyez sur Entrée pour commencer le round..."
        view.display_in(message)
        print(matchs_list[0])
        print(matchs_list[1])
        r_result = partial_round(tournament, player_list_top,
                                 player_list_bottom, match_id,
                                 matchs_played, matchs, matchs_list)
        match_id = r_result[1]
        matchs_played = r_result[2]
        if c_round == 0:
            tournament.r1_result += r_result[0]
        if c_round == 1:
            tournament.r2_result += r_result[0]
        elif c_round == 2:
            tournament.r3_result += r_result[0]
        elif c_round == 3:
            tournament.r4_result += r_result[0]

        if len(r_result) == 4:
            message = "Tournoi mis en pause"
            view.display_out(message)
            save_data(player_list_top, player_list_bottom, tournament,
                      match_id, matchs_played, round_name_l, round_start_l)
        round_end = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        tournament.rounds_list.append([round_name_l, round_start_l, round_end])

        for i in range(c_round + 1, int(tournament.turns)):
            message = (f"Round {str(i + 1)}\n"
                       f"Nom du round : ")
            round_name = view.display_in(message)
            matchs_list = []
            pairs = pairing(player_list_top, player_list_bottom, match_id)
            player_list_top = pairs[0]
            player_list_bottom = pairs[1]
            for j in range(0, 4):
                message = (f"{player_list_top[j].name} "
                           f"{player_list_top[j].surname} "
                           "vs "
                           f"{player_list_bottom[j].name} "
                           f"{player_list_bottom[j].surname}")
                view.display_out(message)
                matchs_list += [f"{player_list_top[j].name} "
                                f"{player_list_top[j].surname} "
                                f"vs "
                                f"{player_list_bottom[j].name} "
                                f"{player_list_bottom[j].surname}"]
            message = "Appuyez sur Entrée pour commencer le round..."
            view.display_in(message)
            round_start = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            r_result = create_round_loop(tournament, player_list_top,
                                         player_list_bottom, match_id,
                                         matchs_played, matchs_list)
            match_id = r_result[1]
            matchs_played = r_result[2]
            if i == 1:
                tournament.r2_result = r_result[0]
            elif i == 2:
                tournament.r3_result = r_result[0]
            elif i == 3:
                tournament.r4_result = r_result[0]

            if len(r_result) == 4:
                message = "Tournoi mis en pause"
                view.display_out(message)
                save_data(player_list_top, player_list_bottom, tournament,
                          match_id, matchs_played, round_name, round_start)
            round_end = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            tournament.rounds_list.append([round_name, round_start, round_end])
    message = "Tournoi terminé"
    view.display_out(message)
    tournament.end_date = datetime.today().strftime('%d/%m/%Y')
    add_tournament_data(tournament)
    player_list = player_list_top + player_list_bottom
    player_list = sorted(player_list, key=lambda x: x.points, reverse=True)
    message = ("Classement final\n"
               "Nom        | Prénom     | Points")
    view.display_out(message)
    for player in player_list:
        message = ("%-12s %-12s %3s" % (player.name, player.surname,
                                        player.points))
        view.display_out(message)
    message = "Appuyez sur Entrée pour continuer..."
    view.display_in(message)

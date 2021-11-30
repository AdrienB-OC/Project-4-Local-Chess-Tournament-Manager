from datetime import datetime

from .pairing import pairing, pairing_r1
from .save_load import save_data
from .tinydb_data import add_player_data, add_tournament_data, fetch_all_data
from models.player_class import Player
from models.tournament_class import Tournament
from view.views import View

view = View()


def create_player():
    data = view.player_input()
    player = Player(data[0], data[1],
                    data[2], data[3], data[4])
    add_player_data(player)
    return player


def create_match(player_1, player_2, matchs_played):
    while True:
        try:
            winner = view.match_input(player_1, player_2)
            if winner in {'1', '2', '3', '9'}:
                match_id = []
                if int(player_1.t_id) < int(player_2.t_id):
                    match_id += [str(int(player_1.t_id)) +
                                 str(int(player_2.t_id))]
                else:
                    match_id += [str(int(player_2.t_id)) +
                                 str(int(player_1.t_id))]
                if winner == '1':
                    player_1.points += 1
                    message = (f" {player_1.surname} {player_1.name} "
                               f"gagne !\n")
                    view.display_out(message)
                    matchs_played += 1
                    return 'win', 'lose', match_id, matchs_played
                elif winner == '2':
                    player_2.points += 1
                    message = (f" {player_2.surname} {player_2.name} "
                               f"gagne !\n")
                    view.display_out(message)
                    matchs_played += 1
                    return 'lose', 'win', match_id, matchs_played
                elif winner == '3':
                    player_1.points += 0.5
                    player_2.points += 0.5
                    message = "Match Nul !\n"
                    view.display_out(message)
                    matchs_played += 1
                    return 'draw', 'draw', match_id, matchs_played
                elif winner == '9':
                    return 0
                break

            else:
                message = "Erreur, entrez un choix valide"
                view.display_out(message)
        except ValueError:
            message = "Erreur, choix invalide"
            view.display_out(message)


def create_round_loop(tournament, player_list_top, player_list_bottom,
                      match_id, matchs_played, matchs_list):
    results = []
    for i in range(0, 4):
        match = create_match(player_list_top[i], player_list_bottom[i],
                             matchs_played)
        if match == 0:
            return results, match_id, matchs_played, 0
        else:
            match_id += match[2]
            matchs_played = match[3]
            results.append(([player_list_top[i].name, match[0]],
                           [player_list_bottom[i].name, match[1]]))
            tournament.matchs_list.append(matchs_list[i])

    return results, match_id, matchs_played


def create_player_list():
    player_list = []
    player_data = fetch_all_data()
    for i in range(0, 8):
        k = 1
        message = "ID | Nom        | Prénom       | Classement"
        view.display_out(message)
        for j in range(len(player_data)):
            message = ("%-4s %-12s %-12s %3s" % (k, player_data[j].name,
                                                 player_data[j].surname,
                                                 player_data[j].ranking))
            view.display_out(message)
            k += 1
        while True:
            try:
                message = ("Entrez l'id correspondant au joueur que "
                           "vous souhaitez ajouter : ")
                option = int(view.display_in(message))
                option -= 1
                if 0 < option < len(player_data):
                    break
                else:
                    message = "Erreur, veuillez entrer un choix valide."
                    view.display_out(message)
            except ValueError:
                message = "Erreur, veuillez entrer un choix valide."
                view.display_out(message)

        for item in enumerate(player_data):
            if item[0] == option:
                player = player_data.pop(option)
                player_list.append(player)
                break

    return player_list


def create_tournament(player_list):
    match_id = []
    matchs_played = 0
    data = view.tournament_input()
    tournament = Tournament(data[0], data[1], data[2], data[3])
    if data[2] == 1:
        tournament.time_control = 'Blitz'
    elif data[2] == 2:
        tournament.time_control = 'Bullet'
    elif data[2] == 3:
        tournament.time_control = 'Coup Rapide'
    tournament.players_list = player_list
    turns = int(tournament.turns)
    for i in range(0, turns):
        message = f"Round {str(i+1)} \n"
        view.display_out(message)
        message = "Nom du round : "
        round_name = view.display_in(message)
        matchs_list = []
        if i == 0:
            pairs = pairing_r1(player_list)
            player_list_top = pairs[0]
            player_list_bottom = pairs[1]
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
            tournament.r1_result += r_result[0]
            if len(r_result) == 4:
                message = "Tournoi mis en pause"
                view.display_out(message)
                save_data(player_list_top, player_list_bottom, tournament,
                          match_id, matchs_played, round_name, round_start)
            round_end = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(tournament.r1_result)
            tournament.rounds_list.append([round_name, round_start, round_end])
        elif i > 0:
            pairs = pairing(player_list_top, player_list_bottom, match_id)
            player_list_top = pairs[0]
            player_list_bottom = pairs[1]
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
    message = "Tournoi terminé !"
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

from tinydb import TinyDB, where

from models.player_class import Tournament_Player
from models.tournament_class import Tournament
from view.views import View


view = View()


def add_player_data(player):
    db = TinyDB("players_db.json")
    players_table = db.table("players")
    serialized_player = {
        'name': player.name,
        'surname': player.surname,
        'birth_date': player.birth_date,
        'gender': player.gender,
        'ranking': player.ranking,
    }
    players_table.insert(serialized_player)
    db.close()


def add_tournament_data(tournament):
    db = TinyDB("tournaments_db.json")
    tournaments_table = db.table("tournaments")
    players_list = []
    points_total = []
    for i in range(0, 8):
        players_list.append(tournament.players_list[i].t_id)
        points_total.append(tournament.players_list[i].points)
    serialized_tournament = {
        'name': tournament.name,
        'location': tournament.location,
        'start_date': tournament.start_date,
        'end_date': tournament.end_date,
        'turns': tournament.turns,
        'rounds_list': tournament.rounds_list,
        'matchs_list': tournament.matchs_list,
        'R1': tournament.r1_result,
        'R2': tournament.r2_result,
        'R3': tournament.r3_result,
        'R4': tournament.r4_result,
        'player_list': players_list,
        'points_total': points_total,
        'time_control': tournament.time_control,
        'description': tournament.description,
    }
    tournaments_table.insert(serialized_tournament)
    db.close()


def update_player_ranking(player_id, new_rank):
    db = TinyDB("players_db.json")
    players_table = db.table("players")
    data = players_table.all()
    data = data[player_id - 1]
    rank = data['ranking']
    name = data['name']
    surname = data['surname']
    players_table.update({'ranking': new_rank}, (where('ranking') == rank) &
                         (where('name') == name) & (where('surname') ==
                         surname))


def update_all_ranking():
    player_list = fetch_all_data()
    for player in player_list:
        view.display_out(f"{player.name} {player.surname}")
        view.display_out(f"Classement : {player.ranking}")
        new_rank = view.display_in('Entrez le nouveau classement de ce '
                                   'joueur : ')
        update_player_ranking(player.t_id, new_rank)
        view.display_out('Classement mis à jour avec succès !')


def display_all_tournaments():
    db = TinyDB("tournaments_db.json")
    tournaments_table = db.table("tournaments")
    tournaments_list = []
    for item in tournaments_table:
        tournament = Tournament(item["name"], item["location"],
                                ' ', ' ')
        tournament.start_date = item["start_date"]
        tournaments_list.append(tournament)
    db.close()

    return tournaments_list


def display_rounds(key):
    db = TinyDB("tournaments_db.json")
    tournaments_table = db.table("tournaments")
    message = ("Liste des tours : \n"
               "Nom            Début                      Fin")
    view.display_out(message)
    for item in tournaments_table:
        if item.doc_id == int(key):
            rounds = item["rounds_list"]
            round_1 = rounds[0]
            round_2 = rounds[1]
            round_3 = rounds[2]
            round_4 = rounds[3]
    message = (f"{round_1[0]}        {round_1[1]}        {round_1[2]}\n"
               f"{round_2[0]}        {round_2[1]}        {round_2[2]}\n"
               f"{round_3[0]}        {round_3[1]}        {round_3[2]}\n"
               f"{round_4[0]}        {round_4[1]}        {round_4[2]}")
    view.display_out(message)
    message = "Appuyez sur Entrée pour continuer..."
    view.display_in(message)


def fetch_matchs_result(key):
    db = TinyDB("tournaments_db.json")
    tournaments_table = db.table("tournaments")
    data = tournaments_table.all()
    data = data[key - 1]
    r1_results = []
    r2_results = []
    r3_results = []
    r4_results = []
    r1 = data["R1"]
    r2 = data["R2"]
    r3 = data["R3"]
    r4 = data["R4"]
    for i in range(0, 4):
        data = r1[i]
        data_r2 = r2[i]
        data_r3 = r3[i]
        data_r4 = r4[i]

        data2 = data[1]
        data = data[0]
        data2_r2 = data_r2[1]
        data_r2 = data_r2[0]
        data2_r3 = data_r3[1]
        data_r3 = data_r3[0]
        data2_r4 = data_r4[1]
        data_r4 = data_r4[0]

        r1_results += data + data2
        r2_results += data_r2 + data2_r2
        r3_results += data_r3 + data2_r3
        r4_results += data_r4 + data2_r4

    return r1_results, r2_results, r3_results, r4_results


def display_matchs_list(key):
    db = TinyDB("tournaments_db.json")
    tournaments_table = db.table("tournaments")
    data = tournaments_table.all()
    data = data[key - 1]
    matchs_list = data["matchs_list"]
    results = fetch_matchs_result(key)
    results_r1 = results[0]
    results_r2 = results[1]
    results_r3 = results[2]
    results_r4 = results[3]
    i = 1
    j = 1
    k = 0
    for match in matchs_list:
        if (i - 1) % 4 == 0:
            k = 0
            message = f"\nRound {j}\n" \
                      f"Match                                    Résultat"
            view.display_out(message)
            j += 1
        if i < 5:
            message = ("%-40s %-5s | %-5s" % (match, results_r1[k + 1],
                                              results_r1[k + 3]))
        elif i < 9:
            message = ("%-40s %-5s | %-5s" % (match, results_r2[k + 1],
                                              results_r2[k + 3]))
        elif i < 13:
            message = ("%-40s %-5s | %-5s" % (match, results_r3[k + 1],
                                              results_r3[k + 3]))
        elif i < 17:
            message = ("%-40s %-5s | %-5s" % (match, results_r4[k + 1],
                                              results_r4[k + 3]))
        view.display_out(message)
        i += 1
        k += 4
    message = "Appuyez sur Entrée pour continuer..."
    view.display_in(message)


def display_tournament_players(key, option):
    db = TinyDB("tournaments_db.json")
    db2 = TinyDB("players_db.json")
    tournaments_table = db.table("tournaments")
    players_table = db2.table("players")

    display_list = []
    data = tournaments_table.all()
    data = data[key - 1]
    players_list = data["player_list"]
    points_total = data["points_total"]

    for player in players_list:
        for item in players_table:
            if item.doc_id == player:
                player_data = Tournament_Player(item.doc_id, item["name"],
                                                item["surname"],
                                                item["birth_date"],
                                                item["gender"],
                                                item["ranking"], 0)
                player_points = points_total[player - (1 + key)]
                player_data.points = player_points
                display_list.append(player_data)
    if option == 1:
        display_list = sorted(display_list, key=lambda x: x.name,
                              reverse=False)
    elif option == 2:
        display_list = sorted(display_list, key=lambda x: x.ranking,
                              reverse=False)
    elif option == 3:
        display_list = sorted(display_list, key=lambda x: x.points,
                              reverse=True)
    message = "Nom            | Prénom         | Classement | Points"
    view.display_out(message)
    for player in display_list:
        message = "%-16s %-16s %-12s %-3s" % (player.name,
                                              player.surname,
                                              player.ranking,
                                              player.points)
        view.display_out(message)
    message = "Appuyez sur Entrée pour continuer..."
    view.display_in(message)


def display_tournament_data(key, choice, choice2):
    if choice == 1:
        display_tournament_players(key, choice2)
    elif choice == 2:
        display_rounds(key)
    elif choice == 3:
        display_matchs_list(key)


def fetch_all_data():
    db = TinyDB("players_db.json")
    players_table = db.table("players")
    player_list = []
    for item in players_table:
        player = Tournament_Player(item.doc_id, item["name"],
                                   item["surname"], item["birth_date"],
                                   item["gender"], item["ranking"], 0)
        player_list.append(player)
    db.close()

    return player_list

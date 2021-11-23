from models.player_class import Tournament_Player
from models.tournament_class import Tournament
from tinydb import TinyDB, where
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
    view.display_out("Liste des tours : ")
    view.display_out("Nom            Début           Fin")
    for item in tournaments_table:
        if item.doc_id == int(key):
            rounds = item["rounds_list"]
            round_1 = rounds[0]
            round_2 = rounds[1]
            round_3 = rounds[2]
            round_4 = rounds[3]
    view.display_out(f"{round_1[0]}        {round_1[1]}        {round_1[2]}\n"
                     f"{round_2[0]}        {round_2[1]}        {round_2[2]}\n"
                     f"{round_3[0]}        {round_3[1]}        {round_3[2]}\n"
                     f"{round_4[0]}        {round_4[1]}        {round_4[2]}")
    view.display_in("Appuyez sur Entrée pour continuer...")


def display_matchs_list(key):
    db = TinyDB("tournaments_db.json")
    tournaments_table = db.table("tournaments")
    data = tournaments_table.all()
    data = data[key - 1]
    matchs_list = data["matchs_list"]
    i = 1
    j = 1
    for match in matchs_list:
        if (i - 1) % 4 == 0:
            view.display_out(f"\nRound {j}")
            j += 1
        view.display_out(match)
        i += 1
    view.display_in("Appuyez sur Entrée pour continuer...")


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
    view.display_out("Nom           Prénom        Classement Points")
    for player in display_list:
        view.display_out("%-13s %-13s %-10s %-5s" % (player.name,
                                                     player.surname,
                                                     player.ranking,
                                                     player.points))
    view.display_in("Appuyez sur Entrée pour continuer...")


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



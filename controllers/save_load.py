from tinydb import TinyDB
from models.player_class import Tournament_Player
from models.tournament_class import Tournament
import os


def serialize_players(player_list_top, player_list_bottom):
    db = TinyDB("db.json")
    players_table = db.table("players")
    players_table.truncate()
    for i in range(0, 4):
        player = player_list_top[i]
        serialized_player = {
            'ID': player.t_id,
            'name': player.name,
            'surname': player.surname,
            'birth_date': player.birth_date,
            'gender': player.gender,
            'ranking': player.ranking,
            'points': player.points
        }
        players_table.insert(serialized_player)
    for i in range(0, 4):
        player = player_list_bottom[i]
        serialized_player = {
            'ID': player.t_id,
            'name': player.name,
            'surname': player.surname,
            'birth_date': player.birth_date,
            'gender': player.gender,
            'ranking': player.ranking,
            'points': player.points
        }
        players_table.insert(serialized_player)
    db.close()


def serialize_tournament(tournament, match_id, matchs_played, round_name,
                         round_start):
    db = TinyDB("db.json")
    tournament_table = db.table("tournament")
    tournament_table.truncate()
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
        'time_control': tournament.time_control,
        'description': tournament.description,
        'match_id': match_id,
        'matchs_played': matchs_played,
        'round_name': round_name,
        'round_start': round_start,
    }
    tournament_table.insert(serialized_tournament)
    db.close()


def load_players():
    db = TinyDB("db.json")
    players_table = db.table("players")
    serialized_players = players_table.all()
    player_list_top = []
    player_list_bottom = []
    for i in range(0, 4):
        s_player = serialized_players[i]
        player = Tournament_Player(s_player["ID"], s_player["name"],
                                   s_player["surname"], s_player["birth_date"],
                                   s_player["gender"], s_player["ranking"],
                                   s_player["points"])
        player_list_top.append(player)
    for i in range(4, 8):
        s_player = serialized_players[i]
        player = Tournament_Player(s_player["ID"], s_player["name"],
                                   s_player["surname"], s_player["birth_date"],
                                   s_player["gender"], s_player["ranking"],
                                   s_player["points"])
        player_list_bottom.append(player)
    db.close()

    return player_list_top, player_list_bottom


def load_tournament():
    db = TinyDB("db.json")
    tournament_table = db.table("tournament")
    s_tournament = tournament_table.all()
    s_tournament = s_tournament[0]
    tournament = Tournament(s_tournament["name"], s_tournament["location"],
                            s_tournament["time_control"],
                            s_tournament["description"])
    tournament.start_date = s_tournament["start_date"]
    tournament.end_date = s_tournament["end_date"]
    tournament.turns = s_tournament["turns"]
    tournament.r1_result = s_tournament["R1"]
    tournament.r2_result = s_tournament["R2"]
    tournament.r3_result = s_tournament["R3"]
    tournament.r4_result = s_tournament["R4"]
    tournament.matchs_list = s_tournament["matchs_list"]
    tournament.time_control = s_tournament["time_control"]
    tournament.description = s_tournament["description"]
    tournament.rounds_list = s_tournament["rounds_list"]
    match_id = s_tournament["match_id"]
    matchs_played = s_tournament["matchs_played"]
    round_name = s_tournament["round_name"]
    round_start = s_tournament["round_start"]

    db.close()

    os.remove("db.json")

    return tournament, match_id, matchs_played, round_name, round_start


def save_data(player_list_top, player_list_bottom, tournament, match_id,
              matchs_played, round_name, round_start):
    serialize_players(player_list_top, player_list_bottom)
    serialize_tournament(tournament, match_id, matchs_played, round_name,
                         round_start)
    exit()


def load_data():
    player_list = load_players()
    tournament_data = load_tournament()

    player_list_top = player_list[0]
    player_list_bottom = player_list[1]
    player_list = player_list[0] + player_list[1]
    player_list = sorted(player_list, key=lambda x: x.ranking, reverse=False)

    tournament = tournament_data[0]
    tournament.players_list = player_list
    match_id = tournament_data[1]
    matchs_played = tournament_data[2]
    round_name = tournament_data[3]
    round_start = tournament_data[4]

    return player_list_top, player_list_bottom, tournament, match_id, \
        matchs_played, round_name, round_start

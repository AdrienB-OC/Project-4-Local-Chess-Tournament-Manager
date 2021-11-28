from datetime import datetime


class Tournament:
    def __init__(self, name, location, time_control,
                 description):
        self.name = name
        self.location = location
        self.start_date = datetime.today().strftime('%d/%m/%Y')
        self.end_date = datetime.today().strftime('%d/%m/%Y')
        self.turns = 4
        self.rounds_list = []
        self.r1_result = []
        self.r2_result = []
        self.r3_result = []
        self.r4_result = []
        self.players_list = []
        self.matchs_list = []
        self.time_control = time_control
        self.description = description

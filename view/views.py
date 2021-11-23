class View:
    def player_input(self):
        name = input("Nom du joueur : ")
        surname = input("Prénom du joueur : ")
        birth_date = input("Date de Naissance (JJ/MM/AAAA) : ")
        gender = input("Sexe (M/F) : ")
        ranking = input("Classement : ")

        return name, surname, birth_date, gender, ranking

    def match_input(self, player1, player2):
        winner = input(f'1 - {player1.name} {player1.surname}\n'
                       f'2 - {player2.name} {player2.surname}\n'
                       f'3 - Match nul \n'
                       f'9 - Mettre le tournoi en pause \n'
                       f'Entrez le chiffre correspondant au gagnant : ')

        return winner

    def tournament_input(self):
        name = input('Nom du tournoi : ')
        location = input('Lieu où se déroule le tournoi : ')
        time_control = int(input(f'Contrôle du temps\n'
                                 f'1 - Blitz\n'
                                 f'2 - Bullet\n'
                                 f'3 - Coup Rapide\n'
                                 f'Entrez votre choix :'))
        description = input('Description : ')

        return name, location, time_control, description

    def display_in(self, display):
        option = input(display)
        return option

    def display_out(self, display):
        print(display)








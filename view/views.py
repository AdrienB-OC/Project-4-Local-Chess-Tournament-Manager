from datetime import datetime


class View:
    def player_input(self):
        name = ""
        while not (name and not name.isspace()):
            name = input("Nom du joueur : ")
            if not (name and not name.isspace()):
                print("Entrez un nom valide")

        surname = ""
        while not (surname and not surname.isspace()):
            surname = input("Prénom du joueur : ")
            if not (surname and not surname.isspace()):
                print("Entrez un prénom valide")

        date_format = "%d/%m/%Y"
        while True:
            birth_date = input("Date de Naissance (JJ/MM/AAAA) : ")
            try:
                datetime.strptime(birth_date, date_format)
                break
            except ValueError:
                print("Format de date incorrect : JJ/MM/AAAA")

        while True:
            gender = input("Sexe (H/F) : ")
            if gender.upper() not in {'H', 'F'}:
                print("Entrez un choix valide : H ou F")
            else:
                break

        while True:
            ranking = input("Classement : ")
            if ranking.isdigit():
                break
            else:
                print("Entrez un nombre valide. (Entier positif)")

        return name, surname, birth_date, gender, ranking

    def match_input(self, player1, player2):
        winner = input(f'1 - {player1.name} {player1.surname}\n'
                       f'2 - {player2.name} {player2.surname}\n'
                       f'3 - Match nul \n'
                       f'9 - Mettre le tournoi en pause \n'
                       f'Entrez le chiffre correspondant au gagnant : ')

        return winner

    def tournament_input(self):
        name = ""
        while not (name and not name.isspace()):
            name = input("Nom du tournoi : ")
            if not (name and not name.isspace()):
                print("Entrez un nom de tournoi valide")

        location = ""
        while not (location and not location.isspace()):
            location = input('Lieu où se déroule le tournoi : ')
            if not (location and not location.isspace()):
                print("Entrez un lieu valide")

        while True:
            time_control = int(input('Contrôle du temps\n'
                                     '1 - Blitz\n'
                                     '2 - Bullet\n'
                                     '3 - Coup Rapide\n'
                                     'Entrez votre choix :'))
            if time_control not in {1, 2, 3}:
                print("Erreur. Entrez un choix valide.")
            else:
                break
        description = input('Description : ')

        return name, location, time_control, description

    def display_in(self, display):
        option = input(display)
        return option

    def display_out(self, display):
        print(display)

    def print_menu(self):
        menu_options = {
            1: "Ajouter un joueur",
            2: "Afficher la liste des joueurs",
            3: "Mettre à jour le classement des joueurs",
            4: "Nouveau Tournoi/Reprendre le tournoi en cours",
            5: "Afficher la liste des tournois",
            6: "Fermer le programme"
        }
        for key in menu_options.keys():
            View.display_out(self, f"{key} -- {menu_options[key]}")

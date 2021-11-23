from .controllers import*
from .resume_tournament import partial_tournament


view = View()
menu_options = {
    1: "Ajouter un joueur",
    2: "Afficher la liste des joueurs",
    3: "Mettre à jour le classement des joueurs",
    4: "Nouveau Tournoi/Reprendre le tournoi en cours",
    5: "Afficher la liste des tournois",
    6: "Fermer le programme"
}


def print_menu():
    for key in menu_options.keys():
        view.display_out(f"{key} -- {menu_options[key]}")


def option1():
    create_player()


def option2():
    player_list = fetch_all_data()
    choice = view.display_in(f"1 - Lister par ordre alphabétique\n"
                             f"2 - Lister par classement\n"
                             f"Entrez votre choix : ")
    if choice == '1':
        player_list = sorted(player_list, key=lambda x: x.surname,
                             reverse=False)
        player_list = sorted(player_list, key=lambda x: x.name,
                             reverse=False)
    if choice == '2':
        player_list = sorted(player_list, key=lambda x: x.ranking,
                             reverse=False)

    view.display_out("ID | Nom            | Prénom           | Classement")
    for player in player_list:
        view.display_out("%-4s %-16s %-16s %3s" % (player.t_id, player.name,
                                                   player.surname,
                                                   player.ranking))
    view.display_in("Appuyez sur Entrée pour continuer...")


def option3():
    update_all_ranking()


def option4():
    if os.path.isfile('./db.json'):
        try:
            choice = view.display_in(f"Reprendre le tournoi en cours ? "
                                     f"Vous ne pouvez pas commencer un "
                                     f"nouveau tournoi en parallèle. \n"
                                     f"1 - Oui\n"
                                     f"2 - Non, plus tard\n"
                                     f"3 - Supprimer les données du "
                                     f"tournoi\n"
                                     f"Votre choix : ")
        except choice not in {'1', '2', '3'}:
            view.display_out(f"Choix invalide. Entrez un chiffre compris "
                             f"entre 1 et 3")
        if choice == '1':
            data = load_data()
            partial_tournament(data[0], data[1], data[2],
                               data[3], data[4], data[5], data[6])
        elif choice == '2':
            pass
        elif choice == '3':
            os.remove("db.json")
    else:
        player_list = create_player_list()
        create_tournament(player_list)


def option5():
    tournaments_list = display_all_tournaments()
    view.display_out(f"ID | Nom du Tournoi | Lieu où s'est déroulé le "
                     f"tournoi | Date de début")
    i = 1
    for tournament in tournaments_list:
        view.display_out("%-4s %-16s %-34s %5s" % (i, tournament.name,
                                                   tournament.location,
                                                   tournament.start_date))
        i += 1
    choice = int(view.display_in("Entrez l'ID d'un tournoi "
                                 "pour plus de détails : "))
    choice2 = int(view.display_in(f"1 - Liste des joueurs du tournoi\n"
                                  f"2 - Liste des tours\n"
                                  f"3 - Liste des matchs\n"
                                  f"0 - Retour au menu\n"
                                  f"Entrez votre choix : "))
    if choice2 == 1:
        choice3 = int(view.display_in(f"1 - Lister par ordre alphabétique\n"
                                      f"2 - Lister par classement\n"
                                      f"Entrez votre choix : "))
        display_tournament_data(choice, choice2, choice3)
    elif choice != 0:
        display_tournament_data(choice, choice2, 0)


def main_menu():
    while True:
        print_menu()
        option = view.display_in('Entrez votre choix : ')
        if option == '1':
            option1()
        elif option == '2':
            option2()
        elif option == '3':
            option3()
        elif option == '4':
            option4()
        elif option == '5':
            option5()
        elif option == '6':
            view.display_out('Fermeture du programme')
            exit()
        else:
            view.display_out(f"Choix invalide. Entrez un chiffre compris "
                             f"entre 1 et 6")


main_menu()
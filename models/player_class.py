class Player:
    def __init__(self, name, surname, birth_date, gender, ranking):
        self.name = name.upper()
        self.surname = surname.capitalize()
        self.birth_date = birth_date
        self.gender = gender
        self.ranking = ranking

    def __str__(self):
        return f"Nom : {self.name} \n" \
               f"Prénom : {self.surname} \n" \
               f"Date de Naissance : {self.birth_date} \n" \
               f"Sexe : {self.gender} \n" \
               f"Classement : {self.ranking} \n"


class Tournament_Player:
    def __init__(self, t_id, name, surname, birth_date, gender, ranking,
                 points):
        self.name = name.upper()
        self.surname = surname.capitalize()
        self.birth_date = birth_date
        self.gender = gender
        self.ranking = ranking
        self.t_id = t_id
        self.points = points

    def __str__(self):
        return f"Nom : {self.name} \n" \
               f"Prénom : {self.surname} \n" \
               f"Date de Naissance : {self.birth_date} \n" \
               f"Sexe : {self.gender} \n" \
               f"Classement : {self.ranking} \n" \
               f"Points : {self.points} \n"

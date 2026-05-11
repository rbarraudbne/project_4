import re

class Player:
    def __init__(self, name: str, surname: str, birthday , chess_id: str):
        self.name = name
        self.surname = surname
        self.birthday = birthday
        self.chess_id = chess_id
        print (f"le joueur {surname} {name} et d'identifiant national d'échec N°{chess_id}a bien été créé.")

    # checking if the chess id have the correct form
    def is_chess_id_correct(self):
        if len(self.chess_id) != 7:
            return False
        pattern = r'^[A-Za-z]{2}[0-9]{5}$'
        if re.match(pattern, self.chess_id):
            return True
        return False

    #adding the new player to the JSON file
    def add_player(self, player_file):
        if not self.is_chess_id_correct():
            print(
                f"Erreur : L'identifiant d'échec '{self.chess_id}' n'est pas valide (format attendu : 2 lettres + 5 chiffres).")
            return

        with open(player_file, "a") as file:
            file.write("self.name, self.surname, self.birthday, self.chess_id\n")


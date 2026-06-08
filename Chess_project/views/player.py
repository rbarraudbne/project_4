
from Chess_project.views.baseview import BaseView


class PlayerView(BaseView):

    def display_create_player(self) -> dict:
        self.display_title("CRÉER UN JOUEUR")

        name = self.get_user_entry(
            msg_display="Nom de famille\n> ",
            msg_error="Le nom ne peut pas être vide.",
            value_type="string",
        )
        first_name = self.get_user_entry(
            msg_display="Prénom\n> ",
            msg_error="Le prénom ne peut pas être vide.",
            value_type="string",
        )
        birthday = self.get_user_entry(
            msg_display="Date de naissance (JJ-MM-AAAA)\n> ",
            msg_error="Format invalide. Exemple : 15-06-1990",
            value_type="date",
        )
        chess_id = self.get_user_entry(
            msg_display="Identifiant national d'échecs (ex: AB12345)\n> ",
            msg_error="Format invalide. Exemple : AB12345",
            value_type="chess_id",
        )
        return {
            "name": name,
            "first_name": first_name,
            "birthday": birthday,
            "chess_id": chess_id,
        }

    def display_all_players(self, players: list):
        self.display_title("LISTE DES JOUEURS")
        if not players:
            print("  Aucun joueur enregistré.")
            return
        sorted_players = sorted(players, key=lambda p: (p["name"], p["first_name"]))
        for p in sorted_players:
            print(f"  {p['name']:20} {p['first_name']:20} {p['birthday']:12} {p['chess_id']}")
        self.display_separator()

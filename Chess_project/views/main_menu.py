from Chess_project.views.baseview import BaseView
from Chess_project.controllers.player_controller import PlayerController
from Chess_project.controllers.tournament_controller import TournamentController
from Chess_project.controllers.report_controller import ReportController
from Chess_project.database import Database


class MainMenu(BaseView):

    def __init__(self):
        self.db = Database()
        self.player_ctrl = PlayerController(self.db)
        self.tournament_ctrl = TournamentController(self.db)
        self.report_ctrl = ReportController(self.db)

    def run(self):
        self.display_title("♟  GESTIONNAIRE DE TOURNOIS D'ÉCHECS  ♟")
        while True:
            user_input = self.get_user_entry(
                msg_display=(
                    "\nQue faire ?\n"
                    "0 - Créer un tournoi\n"
                    "1 - Charger un tournoi\n"
                    "2 - Créer un joueur\n"
                    "3 - Voir les rapports\n"
                    "q - Quitter\n> "
                ),
                msg_error="Veuillez entrer une valeur valide.",
                value_type="selection",
                assertions=["0", "1", "2", "3", "q"],
            )

            if user_input == "0":
                self.tournament_ctrl.create_tournament()
            elif user_input == "1":
                self.tournament_ctrl.load_tournament()
            elif user_input == "2":
                self.player_ctrl.create_player()
            elif user_input == "3":
                self.report_ctrl.run()
            elif user_input == "q":
                print("\n  À bientôt !\n")
                break
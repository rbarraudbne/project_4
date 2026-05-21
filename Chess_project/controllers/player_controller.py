from Chess_project.models.player import Player
from Chess_project.views.player import PlayerView
from Chess_project.controllers.database import Database


class PlayerController:

    def __init__(self, db: Database):
        self.db = db
        self.view = PlayerView()

    def create_player(self):
        data = self.view.display_create_player()
        player = Player(
            name=data["name"],
            first_name=data["first_name"],
            birthday=data["birthday"],
            chess_id=data["chess_id"],
        )
        self.db.save_player(player.to_dict())
        self.view.display_success(
            f"Joueur {player.full_name()} ({player.chess_id}) créé avec succès !"
        )

    def list_players(self):
        players = self.db.load_players()
        self.view.display_all_players(players)
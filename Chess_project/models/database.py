import json
import os

PLAYERS_FILE = os.path.join("data", "players.json")
TOURNAMENTS_FILE = os.path.join("data", "tournaments.json")


class Database:
    """Gère toute la persistance JSON. Sync à chaque modification."""

    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self._init_file(PLAYERS_FILE)
        self._init_file(TOURNAMENTS_FILE)

    @staticmethod
    def _init_file(path: str):
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump([], f)

    @staticmethod
    def _read(path: str) -> list:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _write(path: str, data: list):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # ─── Joueurs ──────────────────────────────────────────────────────────────

    def load_players(self) -> list:
        return self._read(PLAYERS_FILE)

    def save_player(self, player_dict: dict):
        players = self.load_players()
        # Évite les doublons sur chess_id
        for p in players:
            if p["chess_id"] == player_dict["chess_id"]:
                return
        players.append(player_dict)
        self._write(PLAYERS_FILE, players)

    # ─── Tournois ─────────────────────────────────────────────────────────────

    def load_tournaments(self) -> list:
        return self._read(TOURNAMENTS_FILE)

    def save_tournament(self, tournament_dict: dict):
        """Insère ou met à jour un tournoi (clé : name + starting_date)."""
        tournaments = self.load_tournaments()
        key = (tournament_dict["name"], tournament_dict["starting_date"])
        for i, t in enumerate(tournaments):
            if (t["name"], t["starting_date"]) == key:
                tournaments[i] = tournament_dict
                self._write(TOURNAMENTS_FILE, tournaments)
                return
        tournaments.append(tournament_dict)
        self._write(TOURNAMENTS_FILE, tournaments)

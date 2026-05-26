from datetime import datetime
from Chess_project.models.match import ChessMatch


class Round:
    """Un tour de tournoi contenant une liste de matchs."""

    def __init__(self, name: str):
        self.name = name
        self.start_time: str = datetime.now().strftime("%d-%m-%Y %H:%M")
        self.end_time: str = ""
        self.matches: list[ChessMatch] = []

    def add_match(self, match: ChessMatch):
        self.matches.append(match)

    def close(self):
        """Marque le tour comme terminé et enregistre l'heure de fin."""
        self.end_time = datetime.now().strftime("%d-%m-%Y %H:%M")

    def is_finished(self) -> bool:
        return bool(self.end_time)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "matches": [m.to_tuple() for m in self.matches],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Round":
        round_ = cls(name=data["name"])
        round_.start_time = data["start_time"]
        round_.end_time = data.get("end_time", "")
        round_.matches = [ChessMatch.from_tuple(tuple(m)) for m in data["matches"]]
        return round_
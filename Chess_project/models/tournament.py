import random
from Chess_project.models.round import Round
from Chess_project.models.match import ChessMatch


class Tournament:
    """Modèle central d'un tournoi d'échecs."""

    def __init__(
        self,
        name: str,
        location: str,
        starting_date: str,
        finish_date: str,
        list_of_players: list,
        number_of_rounds: int = 4,
        description: str = "",
    ):
        self.name = name
        self.location = location
        self.starting_date = starting_date
        self.finish_date = finish_date
        self.list_of_players = list_of_players   # liste de dicts {chess_id, ...}
        self.number_of_rounds = number_of_rounds
        self.description = description
        self.current_round: int = 0
        self.rounds: list[Round] = []
        self.finished: bool = False
        # Scores cumulés {chess_id: float}
        self.scores: dict = {p["chess_id"]: 0.0 for p in list_of_players}

    # ─── Génération de paires ─────────────────────────────────────────────────

    def _played_pairs(self) -> set:
        """Retourne l'ensemble des paires déjà jouées (frozenset de chess_id)."""
        pairs = set()
        for round_ in self.rounds:
            for match in round_.matches:
                id1 = match.white_player["chess_id"]
                id2 = match.black_player["chess_id"]
                pairs.add(frozenset([id1, id2]))
        return pairs

    def create_players_pairs(self) -> list[tuple]:
        """
        Génère les paires pour le prochain tour selon le système suisse.
        Premier tour : ordre aléatoire.
        Tours suivants : triés par score, en évitant les rematch.
        Retourne une liste de tuples (joueur_blanc, joueur_noir).
        """
        already_played = self._played_pairs()

        if self.current_round == 0:
            players = self.list_of_players[:]
            random.shuffle(players)
        else:
            players = sorted(
                self.list_of_players,
                key=lambda p: self.scores[p["chess_id"]],
                reverse=True,
            )

        pairs = []
        unpaired = players[:]

        while len(unpaired) >= 2:
            player1 = unpaired.pop(0)
            paired = False
            for i, player2 in enumerate(unpaired):
                pair_key = frozenset([player1["chess_id"], player2["chess_id"]])
                if pair_key not in already_played:
                    pairs.append((player1, player2))
                    unpaired.pop(i)
                    paired = True
                    break
            if not paired:
                # Aucun adversaire inédit : on accepte le rematch avec le premier dispo
                player2 = unpaired.pop(0)
                pairs.append((player1, player2))

        return pairs

    def create_round(self) -> Round:
        """Crée le prochain tour avec ses matchs et l'ajoute au tournoi."""
        self.current_round += 1
        round_ = Round(name=f"Round {self.current_round}")
        pairs = self.create_players_pairs()
        for white, black in pairs:
            # Tirage au sort de la couleur
            if random.random() < 0.5:
                white, black = black, white
            round_.add_match(ChessMatch(white, black))
        self.rounds.append(round_)
        return round_

    def update_scores(self, round_: Round):
        """Met à jour les scores après la fin d'un tour."""
        for match in round_.matches:
            self.scores[match.white_player["chess_id"]] += match.white_score
            self.scores[match.black_player["chess_id"]] += match.black_score

    def get_ranking(self) -> list:
        """Retourne la liste des joueurs triés par score décroissant."""
        return sorted(
            self.list_of_players,
            key=lambda p: self.scores[p["chess_id"]],
            reverse=True,
        )

    # ─── Sérialisation ────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "location": self.location,
            "starting_date": self.starting_date,
            "finish_date": self.finish_date,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "description": self.description,
            "list_of_players": self.list_of_players,
            "rounds": [r.to_dict() for r in self.rounds],
            "scores": self.scores,
            "finished": self.finished,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Tournament":
        t = cls(
            name=data["name"],
            location=data["location"],
            starting_date=data["starting_date"],
            finish_date=data["finish_date"],
            list_of_players=data["list_of_players"],
            number_of_rounds=data["number_of_rounds"],
            description=data.get("description", ""),
        )
        t.current_round = data.get("current_round", 0)
        t.finished = data.get("finished", False)
        t.scores = data.get("scores", {p["chess_id"]: 0.0 for p in t.list_of_players})
        t.rounds = [Round.from_dict(r) for r in data.get("rounds", [])]
        return t

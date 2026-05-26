class ChessMatch:
    """
    Un match entre deux joueurs.
    Stocké sous la forme d'un tuple : ([joueur_blanc, score], [joueur_noir, score])
    Scores : 1 = victoire, 0 = défaite, 0.5 = nul
    """

    def __init__(self, white_player: dict, black_player: dict):
        self.white_player = white_player
        self.black_player = black_player
        self.white_score: float = 0.0
        self.black_score: float = 0.0
        self.finished: bool = False

    def set_result(self, result: str):
        """
        result : "blanc" | "noir" | "nul"
        """
        if result == "blanc":
            self.white_score = 1.0
            self.black_score = 0.0
        elif result == "noir":
            self.white_score = 0.0
            self.black_score = 1.0
        elif result == "nul":
            self.white_score = 0.5
            self.black_score = 0.5
        self.finished = True

    def to_tuple(self) -> tuple:
        """Format de stockage JSON demandé par les specs."""
        return (
            [self.white_player, self.white_score],
            [self.black_player, self.black_score],
        )

    @classmethod
    def from_tuple(cls, data: tuple) -> "ChessMatch":
        match = cls(
            white_player=data[0][0],
            black_player=data[1][0],
        )
        match.white_score = data[0][1]
        match.black_score = data[1][1]
        match.finished = True
        return match
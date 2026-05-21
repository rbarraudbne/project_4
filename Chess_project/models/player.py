class Player:
    def __init__(self, name: str, first_name: str, birthday: str, chess_id: str):
        self.name = name
        self.first_name = first_name
        self.birthday = birthday
        self.chess_id = chess_id

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "first_name": self.first_name,
            "birthday": self.birthday,
            "chess_id": self.chess_id,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        return cls(
            name=data["name"],
            first_name=data["first_name"],
            birthday=data["birthday"],
            chess_id=data["chess_id"],
        )

    def full_name(self) -> str:
        return f"{self.first_name} {self.name}"
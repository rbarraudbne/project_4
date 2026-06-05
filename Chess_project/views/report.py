from Chess_project.views.baseview import BaseView


class ReportView(BaseView):

    def display_report_menu(self) -> str:
        return self.get_user_entry(
            msg_display=(
                "\n── RAPPORTS ──\n"
                "0 - Liste de tous les joueurs (ordre alphabétique)\n"
                "1 - Liste de tous les tournois\n"
                "2 - Détail d'un tournoi (nom, dates)\n"
                "3 - Joueurs d'un tournoi (ordre alphabétique)\n"
                "4 - Tours et matchs d'un tournoi\n"
                "q - Retour\n> "
            ),
            msg_error="Choix invalide.",
            value_type="selection",
            assertions=["0", "1", "2", "3", "4", "q"],
        )

    def display_all_players(self, players: list):
        self.display_title("TOUS LES JOUEURS")
        if not players:
            print("  Aucun joueur enregistré.")
            return
        for p in sorted(players, key=lambda x: (x["name"], x["first_name"])):
            print(f"  {p['name']:20} {p['first_name']:20} {p['birthday']:12} {p['chess_id']}")
        self.display_separator()

    def display_all_tournaments(self, tournaments: list):
        self.display_title("TOUS LES TOURNOIS")
        if not tournaments:
            print("  Aucun tournoi enregistré.")
            return
        for t in tournaments:
            status = "✔" if t.get("finished") else "•"
            print(f"  {status} {t['name']:25} {t['location']:20} {t['starting_date']} → {t['finish_date']}")
        self.display_separator()

    def display_tournament_info(self, tournament: dict):
        self.display_title(f"TOURNOI : {tournament['name']}")
        print(f"  Lieu    : {tournament['location']}")
        print(f"  Début   : {tournament['starting_date']}")
        print(f"  Fin     : {tournament['finish_date']}")
        print(f"  Tours   : {tournament['number_of_rounds']}")
        if tournament.get("description"):
            print(f"  Note    : {tournament['description']}")
        self.display_separator()

    def display_tournament_players(self, tournament: dict):
        self.display_title(f"JOUEURS — {tournament['name']}")
        players = sorted(
            tournament["list_of_players"],
            key=lambda p: (p["name"], p["first_name"])
        )
        for p in players:
            print(f"  {p['name']:20} {p['first_name']:20} {p['chess_id']}")
        self.display_separator()

    def display_tournament_rounds(self, tournament: dict):
        self.display_title(f"TOURS & MATCHS — {tournament['name']}")
        rounds = tournament.get("rounds", [])
        if not rounds:
            print("  Aucun tour joué.")
            return
        for round_ in rounds:
            print(f"\n  {round_['name']}"
                  f"  |  Début : {round_['start_time']}"
                  f"  |  Fin : {round_.get('end_time', 'en cours')}")
            self.display_separator(char="·", width=50)
            for i, match in enumerate(round_["matches"], 1):
                white, ws = match[0]
                black, bs = match[1]
                print(
                    f"    Match {i} : "
                    f"{white['name']} {white['first_name']} ({ws} pt)"
                    f"  vs  "
                    f"{black['name']} {black['first_name']} ({bs} pt)"
                )
        self.display_separator()

    def prompt_select_tournament(self, tournaments: list) -> int | None:
        """Permet de choisir un tournoi dans une liste pour les rapports."""
        if not tournaments:
            self.display_error("Aucun tournoi disponible.")
            return None
        print()
        for i, t in enumerate(tournaments):
            print(f"  {i} - {t['name']} ({t['location']})")
        choices = [str(i) for i in range(len(tournaments))] + ["q"]
        user_input = self.get_user_entry(
            msg_display="Choisissez un tournoi | q = annuler\n> ",
            msg_error="Choix invalide.",
            value_type="selection",
            assertions=choices,
        )
        return None if user_input == "q" else int(user_input)
from Chess_project.views.baseview import BaseView


class TournamentView(BaseView):

    # ─── Création ─────────────────────────────────────────────────────────────

    def display_create_tournament(self, available_players: list) -> dict | None:
        self.display_title("CRÉER UN TOURNOI")

        name = self.get_user_entry(
            msg_display="Nom du tournoi\n> ",
            msg_error="Le nom ne peut pas être vide.",
            value_type="string",
        )
        location = self.get_user_entry(
            msg_display="Lieu\n> ",
            msg_error="Le lieu ne peut pas être vide.",
            value_type="string",
        )
        starting_date = self.get_user_entry(
            msg_display="Date de début (JJ-MM-AAAA)\n> ",
            msg_error="Format invalide. Exemple : 01-06-2025",
            value_type="date",
        )
        finish_date = self.get_user_entry(
            msg_display="Date de fin (JJ-MM-AAAA)\n> ",
            msg_error="Format invalide. Exemple : 02-06-2025",
            value_type="date",
        )
        number_of_rounds = self._prompt_number_of_rounds()
        description = input("Description / remarques (optionnel)\n> ").strip()
        selected_players = self._prompt_select_players(available_players)

        if selected_players is None:
            return None

        return {
            "name": name,
            "location": location,
            "starting_date": starting_date,
            "finish_date": finish_date,
            "number_of_rounds": number_of_rounds,
            "description": description,
            "list_of_players": selected_players,
        }

    def _prompt_number_of_rounds(self) -> int:
        while True:
            raw = input("Nombre de tours [4 par défaut]\n> ").strip()
            if raw == "":
                return 4
            if raw.isdigit() and int(raw) > 0:
                return int(raw)
            print("  ✗ Veuillez entrer un entier positif.")

    def _prompt_select_players(self, available_players: list) -> list | None:
        if not available_players:
            self.display_error("Aucun joueur enregistré. Créez d'abord des joueurs.")
            return None

        selected = []
        while True:
            self._display_player_list(available_players, selected)
            choices = [str(i) for i in range(len(available_players))] + ["v", "q"]
            user_input = self.get_user_entry(
                msg_display="\nNuméro pour ajouter/retirer | v = valider | q = annuler\n> ",
                msg_error="Choix invalide.",
                value_type="selection",
                assertions=choices,
            )
            if user_input == "q":
                return None
            if user_input == "v":
                if len(selected) < 2:
                    self.display_error("Un tournoi nécessite au moins 2 joueurs.")
                    continue
                return selected
            player = available_players[int(user_input)]
            if player in selected:
                selected.remove(player)
            else:
                selected.append(player)

    def _display_player_list(self, players: list, selected: list):
        print("\nJoueurs disponibles :")
        for i, p in enumerate(players):
            marker = "✔" if p in selected else " "
            print(f"  [{marker}] {i} - {p['name']} {p['first_name']}  ({p['chess_id']})")
        print(f"\n  {len(selected)} joueur(s) sélectionné(s)")

    # ─── Chargement ───────────────────────────────────────────────────────────

    def display_load_tournament(self, tournaments: list) -> int | None:
        self.display_title("CHARGER UN TOURNOI")
        if not tournaments:
            self.display_error("Aucun tournoi sauvegardé.")
            return None
        for i, t in enumerate(tournaments):
            status = "✔ terminé" if t.get("finished") else "en cours"
            print(f"  {i} - {t['name']} | {t['location']} | {t['starting_date']} [{status}]")
        choices = [str(i) for i in range(len(tournaments))] + ["q"]
        user_input = self.get_user_entry(
            msg_display="\nChoisissez un tournoi | q = annuler\n> ",
            msg_error="Choix invalide.",
            value_type="selection",
            assertions=choices,
        )
        return None if user_input == "q" else int(user_input)

    # ─── Gestion d'un tour ────────────────────────────────────────────────────

    def display_round_start(self, round_name: str, matches: list):
        self.display_title(f"{round_name.upper()}")
        print("  Appariements :\n")
        for i, match in enumerate(matches):
            w = match.white_player
            b = match.black_player
            print(f"  Match {i + 1} : {w['name']} {w['first_name']} (Blancs)"
                  f"  vs  {b['name']} {b['first_name']} (Noirs)")
        self.display_separator()

    def prompt_match_results(self, matches: list) -> list:
        """Demande le résultat de chaque match. Retourne la liste des résultats."""
        self.display_title("SAISIR LES RÉSULTATS")
        results = []
        for i, match in enumerate(matches):
            w = match.white_player
            b = match.black_player
            print(f"\n  Match {i + 1} : {w['name']} {w['first_name']} vs {b['name']} {b['first_name']}")
            result = self.get_user_entry(
                msg_display="  Résultat : b = blancs gagnent | n = noirs gagnent | nul = match nul\n  > ",
                msg_error="  Entrez b, n ou nul.",
                value_type="selection",
                assertions=["b", "n", "nul"],
            )
            mapping = {"b": "blanc", "n": "noir", "nul": "nul"}
            results.append(mapping[result])
        return results

    # ─── Affichage tournoi ────────────────────────────────────────────────────

    def display_tournament_details(self, tournament: dict):
        self.display_title(f"TOURNOI : {tournament.get('name', '')} — {tournament['location']}")
        print(f"  Dates   : {tournament['starting_date']} → {tournament['finish_date']}")
        print(f"  Tours   : {tournament['current_round']}/{tournament['number_of_rounds']}")
        print(f"  Joueurs : {len(tournament['list_of_players'])}")
        if tournament.get("description"):
            print(f"  Note    : {tournament['description']}")
        self.display_separator()

    def display_ranking(self, ranking: list, scores: dict):
        self.display_title("CLASSEMENT")
        for i, p in enumerate(ranking, 1):
            score = scores.get(p["chess_id"], 0.0)
            print(f"  {i}. {p['name']:20} {p['first_name']:20} — {score} pts")
        self.display_separator()

    def display_tournament_menu(self, tournament_name: str) -> str:
        return self.get_user_entry(
            msg_display=(
                f"\n── {tournament_name} ──\n"
                "0 - Lancer le prochain tour\n"
                "1 - Saisir les résultats du tour en cours\n"
                "2 - Voir le classement\n"
                "q - Retour au menu principal\n> "
            ),
            msg_error="Choix invalide.",
            value_type="selection",
            assertions=["0", "1", "2", "q"],
        )
from Chess_project.models.tournament import Tournament
from Chess_project.views.tournament import TournamentView
from Chess_project.models.database import Database


class TournamentController:

    def __init__(self, db: Database):
        self.db = db
        self.view = TournamentView()
        self.active_tournament: Tournament | None = None

    # ─── Création / Chargement ────────────────────────────────────────────────

    def create_tournament(self):
        players = self.db.load_players()
        data = self.view.display_create_tournament(players)
        if data is None:
            self.view.display_error("Création annulée.")
            return

        tournament = Tournament(
            name=data["name"],
            location=data["location"],
            starting_date=data["starting_date"],
            finish_date=data["finish_date"],
            list_of_players=data["list_of_players"],
            number_of_rounds=data["number_of_rounds"],
            description=data["description"],
        )
        self.active_tournament = tournament
        self.db.save_tournament(tournament.to_dict())
        self.view.display_success(f"Tournoi « {tournament.name} » créé !")
        self.view.display_tournament_details(tournament.to_dict())
        self._run_tournament()

    def load_tournament(self):
        tournaments = self.db.load_tournaments()
        index = self.view.display_load_tournament(tournaments)
        if index is None:
            return
        self.active_tournament = Tournament.from_dict(tournaments[index])
        self.view.display_tournament_details(self.active_tournament.to_dict())
        self._run_tournament()

    # ─── Boucle principale du tournoi ─────────────────────────────────────────

    def _run_tournament(self):
        t = self.active_tournament
        while True:
            if t.finished:
                self.view.display_success("Ce tournoi est terminé.")
                self.view.display_ranking(t.get_ranking(), t.scores)
                break

            choice = self.view.display_tournament_menu(t.name)

            if choice == "0":
                self._start_next_round()
            elif choice == "1":
                self._enter_results()
            elif choice == "2":
                self.view.display_ranking(t.get_ranking(), t.scores)
            elif choice == "q":
                break

    def _start_next_round(self):
        t = self.active_tournament
        if t.current_round >= t.number_of_rounds:
            self.view.display_error(
                f"Tous les tours ont été joués ({t.number_of_rounds}/{t.number_of_rounds})."
            )
            return
        # Vérifie que le tour précédent est bien terminé
        if t.rounds and not t.rounds[-1].is_finished():
            self.view.display_error(
                "Saisissez d'abord les résultats du tour en cours (option 1)."
            )
            return

        round_ = t.create_round()
        self.view.display_round_start(round_.name, round_.matches)
        self.db.save_tournament(t.to_dict())

    def _enter_results(self):
        t = self.active_tournament
        if not t.rounds:
            self.view.display_error("Aucun tour en cours. Lancez d'abord un tour (option 0).")
            return
        current_round = t.rounds[-1]
        if current_round.is_finished():
            self.view.display_error("Ce tour est déjà clôturé.")
            return

        results = self.view.prompt_match_results(current_round.matches)
        for match, result in zip(current_round.matches, results):
            match.set_result(result)

        current_round.close()
        t.update_scores(current_round)

        if t.current_round >= t.number_of_rounds:
            t.finished = True

        self.db.save_tournament(t.to_dict())
        self.view.display_success("Résultats enregistrés !")
        self.view.display_ranking(t.get_ranking(), t.scores)
from Chess_project.views.report import ReportView
from Chess_project.models.database import Database


class ReportController:

    def __init__(self, db: Database):
        self.db = db
        self.view = ReportView()

    def run(self):
        while True:
            choice = self.view.display_report_menu()
            if choice == "0":
                self.view.display_all_players(self.db.load_players())
            elif choice == "1":
                self.view.display_all_tournaments(self.db.load_tournaments())
            elif choice in ("2", "3", "4"):
                tournaments = self.db.load_tournaments()
                index = self.view.prompt_select_tournament(tournaments)
                if index is None:
                    continue
                t = tournaments[index]
                if choice == "2":
                    self.view.display_tournament_info(t)
                elif choice == "3":
                    self.view.display_tournament_players(t)
                elif choice == "4":
                    self.view.display_tournament_rounds(t)
            elif choice == "q":
                break

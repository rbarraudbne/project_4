from datetime import datetime
import re


class BaseView:

    def get_user_entry(
        self, msg_display, msg_error, value_type, assertions=None, default_value=None
    ):
        while True:
            value = input(msg_display)
            if value_type == "numeric":
                if value.isnumeric():
                    return int(value)
                print(msg_error)

            elif value_type == "num_superior":
                if value.isnumeric() and int(value) >= default_value:
                    return int(value)
                print(msg_error)

            elif value_type == "string":
                if value.strip():
                    return value.strip()
                print(msg_error)

            elif value_type == "date":
                if self.verify_date(value):
                    return value
                print(msg_error)

            elif value_type == "selection":
                if value in assertions:
                    return value
                print(msg_error)

            elif value_type == "chess_id":
                pattern = r'^[A-Za-z]{2}[0-9]{5}$'
                if re.match(pattern, value):
                    return value
                print(msg_error)

    @staticmethod
    def verify_date(value):
        for fmt in ("%d-%m-%Y", "%d/%m/%Y"):
            try:
                datetime.strptime(value, fmt)
                return True
            except ValueError:
                pass
        return False

    @staticmethod
    def get_timestamp():
        return datetime.now().strftime("%d-%m-%Y %H:%M")

    @staticmethod
    def display_separator(char="─", width=50):
        print(char * width)

    def display_title(self, title: str):
        self.display_separator()
        print(f"  {title}")
        self.display_separator()

    def display_success(self, message: str):
        print(f"\n  ✔ {message}\n")

    def display_error(self, message: str):
        print(f"\n  ✗ {message}\n")


import sys
import requests
import html
import random
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QRadioButton, QPushButton, QMessageBox
from PySide6 import QtCore



class QuizGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multiple Choice Quiz Game")
        self.layout = QVBoxLayout()
        self.setStyleSheet("background: #f9EBEA;")
        self.setFixedWidth(700)

        self.current_question = 0
        self.correct_answers = 0
        self.questions = []
        self.create_widgets()
        self.load_questions()

    def create_widgets(self):
        self.question_label = QLabel()
        self.layout.addWidget(self.question_label)

        self.option1 = QRadioButton()
        self.layout.addWidget(self.option1)

        self.option2 = QRadioButton()
        self.layout.addWidget(self.option2)

        self.option3 = QRadioButton()
        self.layout.addWidget(self.option3)

        self.option4 = QRadioButton()
        self.layout.addWidget(self.option4)

        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedWidth(100)
        self.submit_button.setFixedHeight(40)
        self.submit_button.setStyleSheet("""
                                        QPushButton {
                                            color:  white;
                                            background-color: #900C3F;
                                            border: 5px solid white;
                                            border-radius: 10px;
                                            margin-left: 15px;
                                        }
                                        QPushButton:hover {
                                            color: #68c62a;
                                        }
                                        """)

        self.submit_button.clicked.connect(self.check_answer)
        self.layout.addWidget(self.submit_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)

    def load_questions(self):
        url = "https://opentdb.com/api.php"
        parameters = {"amount": 20, "type": "multiple"}
        response = requests.get(url, params=parameters)
        if response.status_code == 200:
            data = response.json()
            if data["response_code"] == 0:
                self.questions = data["results"]
                self.show_question()
            else:
                self.show_error_message(f"Failed to load questions.")
        else:
            self.show_error_message(f"Failed to connect to the server. {response.status_code}")

    def show_question(self):
        self.clear_radio_buttons()  # Clear checked radio buttons
        question_data = self.questions[self.current_question]
        self.question_label.setText(html.unescape(question_data["question"]))  # Unescape html quotes
        options = question_data["incorrect_answers"] + [question_data["correct_answer"]]
        options = [option.encode("latin1").decode("utf-8") for option in options]  # Handle special characters

        # Check if number of options is at least 4 (some in opentdb multiple choice have less)
        if len(options) == 4:
            random.shuffle(options)  # Shuffle options
            self.option1.setText(options[0])
            self.option2.setText(options[1])
            self.option3.setText(options[2])
            self.option4.setText(options[3])
        else:    # Skip to the next question if number of options is not 4, otherwise will get IndexError
            self.show_error_message("Invalid question format. Skipping to the next question.")
            self.current_question += 1
            if self.current_question < len(self.questions):
                self.show_question()
            else:
                self.show_result()

    def clear_radio_buttons(self):
        self.option1.setAutoExclusive(False)
        self.option1.setChecked(False)
        self.option1.setAutoExclusive(True)
        self.option2.setAutoExclusive(False)
        self.option2.setChecked(False)
        self.option2.setAutoExclusive(True)
        self.option3.setAutoExclusive(False)
        self.option3.setChecked(False)
        self.option3.setAutoExclusive(True)
        self.option4.setAutoExclusive(False)
        self.option4.setChecked(False)
        self.option4.setAutoExclusive(True)

    def check_answer(self):
        selected_option = None
        if self.option1.isChecked():
            selected_option = self.option1.text()
        elif self.option2.isChecked():
            selected_option = self.option2.text()
        elif self.option3.isChecked():
            selected_option = self.option3.text()
        elif self.option4.isChecked():
            selected_option = self.option4.text()

        if selected_option:
            question_data = self.questions[self.current_question]
            correct_answer = question_data["correct_answer"].encode("latin1").decode("utf-8")
            if selected_option == correct_answer:
                self.correct_answers += 1

            self.current_question += 1
            if self.current_question < len(self.questions):
                self.show_question()
            else:
                self.show_result()
        else:
            self.show_error_message("Please select an option.")

    def show_result(self):
        message = f"You answered {self.correct_answers} out of {len(self.questions)} questions correctly."
        QMessageBox.information(self, "Quiz Result", message)
        self.close()

    def show_error_message(self, message: str) -> None:
        QMessageBox.critical(self, "Error", message)
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = QuizGame()
    game.show()
    sys.exit(app.exec())

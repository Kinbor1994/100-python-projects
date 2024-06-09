import sys
import random
from pathlib import Path
from PySide6 import QtWidgets, QtCore


class App(QtWidgets.QWidget):

    BASE_DIR = Path(__file__).resolve().parent
    words_file = BASE_DIR / "terms_informatic.txt"

    LE_STYLE = """
        background-color: white;
        font:bold;
        font-size:15px;
        """
        
    BTN_STYLE = """
        background-color: white;
        color:black;
        font:bold;
        """

    TE_STYLE = """
        background-color: #73d5ee;
        color: #190468;
        font:bold;
        font-size:28px;
        """
    
    TE_END_STYLE = """
        background-color: #eaf869;
        color: #190468;
        font:bold;
        font-size:28px;
        """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("words finding")
        self.setGeometry(100, 100, 400, 400)
        
        self.words = self.load_words(self.words_file) # Lire les mots depuis le fichier
        self.current_word = ""
        self.current_scrambled_word = ""
        self.score = 0

        self.setup_css()
        self.setup_ui()
        self.setup_initial_value()
        self.setup_connection()

    def setup_ui(self):
        """Méthode pour ajouter les widget sur le formulaire"""
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_gb = QtWidgets.QGroupBox(title="BOREL Words Game")
        self.group_layout = QtWidgets.QVBoxLayout(self.main_gb)
        self.btn_layout = QtWidgets.QHBoxLayout()
        self.te_infos = QtWidgets.QTextEdit()
        self.te_infos.setStyleSheet(self.TE_STYLE)
        self.te_infos.setReadOnly(True)
        self.le_user_entry = QtWidgets.QLineEdit()
        self.le_user_entry.setReadOnly(True)
        self.le_user_entry.setStyleSheet(self.LE_STYLE)
        self.le_current_word = QtWidgets.QLineEdit()
        self.le_current_word.setReadOnly(True)
        self.le_current_word.setStyleSheet(self.LE_STYLE)
        self.btn_start = QtWidgets.QPushButton("Start")
        self.btn_start.setStyleSheet(self.BTN_STYLE)
        self.btn_quit = QtWidgets.QPushButton("Quit")
        self.btn_quit.setStyleSheet(self.BTN_STYLE)
        self.btn_valid = QtWidgets.QPushButton("Valid")
        self.btn_valid.setStyleSheet(self.BTN_STYLE)
        self.btn_valid.setVisible(False)
        self.btn_stop = QtWidgets.QPushButton("Stop")
        self.btn_stop.setStyleSheet(self.BTN_STYLE)
        self.btn_stop.setVisible(False)

        self.main_layout.addWidget(self.main_gb)
        self.group_layout.addWidget(self.te_infos)
        self.group_layout.addWidget(self.le_user_entry)
        self.group_layout.addWidget(self.le_current_word)
        self.group_layout.addLayout(self.btn_layout)
        self.btn_layout.addWidget(self.btn_start)
        self.btn_layout.addWidget(self.btn_quit)
        self.btn_layout.addWidget(self.btn_valid)
        self.btn_layout.addWidget(self.btn_stop)

    def setup_initial_value(self):
        self.te_infos.setText(
            "<div style='text-align: center;'>Bienvenue dans le jeu, trouvez le mot en informatique. </div>"
        )

    def setup_connection(self):
        """Etablie les connections pour les bouttons
        """
        self.btn_start.clicked.connect(self.start_game)
        self.btn_stop.clicked.connect(self.end_game)
        self.btn_quit.clicked.connect(self.quit)
        self.btn_valid.clicked.connect(self.check_word)
    
    def setup_css(self):
        self.setStyleSheet("background-color: #1eda37;")
        
    def load_words(self, file_path):
        """Récupère les mots dans une liste."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                words = file.read().strip().split(", ")
            return words
        except FileNotFoundError:
            QtWidgets.QMessageBox.critical(
                self, "Erreur", f"Le fichier {file_path} est introuvable."
            )
            exit(1)

    def scramble_word(self, word):
        """Mélange les lettres du mot

        Args:
            word (str): mot à deviner
        """
        scrambled = list(word)  # Transforme les caractères du mot en un liste
        random.shuffle(scrambled)  # Permute la position des caractères dans la liste
        return "".join(
            scrambled
        )  # Transforme les caractère dans la liste en une chaine de caractère

    def next_word(self):
        """Sélectionner un nouveau mot à deviner."""
        self.current_word = random.choice(self.words)
        self.current_scrambled_word = self.scramble_word(self.current_word)
        self.le_current_word.setText(self.current_scrambled_word)
        self.te_infos.setHtml(
            f"<div style='text-align: center;'>Indices:<br>Le mot commence par: <span style='color:green;'>{self.current_word[0]}</span><br> Et se termine par: <span style='color:green;'>{self.current_word[-1]}</span> </div>"
        )

    def start_game(self):
        """Lance le jeux
        """
        self.le_user_entry.setReadOnly(False)
        self.btn_start.setVisible(False)
        self.btn_quit.setVisible(False)
        self.btn_valid.setVisible(True)
        self.btn_stop.setVisible(True)
        self.te_infos.setStyleSheet(self.TE_STYLE)
        self.next_word()
    
    def end_game(self):
        """Mets fin au jeu
        """
        self.le_user_entry.setReadOnly(True)
        self.btn_start.setVisible(True)
        self.btn_quit.setVisible(True)
        self.btn_valid.setVisible(False)
        self.btn_stop.setVisible(False)
        self.le_current_word.clear()
        self.le_user_entry.clear()
        self.te_infos.setStyleSheet(self.TE_END_STYLE)
        self.te_infos.setText(f"<div style='text-align: center;'>Merci pour votre participation.<br>Score: {str(self.score)} </div>")
        self.score = 0
    
    def quit(self):
        """Ferme le jeu
        """
        self.close()
        
    def check_word(self):
        """Vérifier le mot deviné par l'utilisateur."""
        guessed_word = self.le_user_entry.text().strip()
        if guessed_word == self.current_word:
            self.score += 5
            QtWidgets.QMessageBox.information(self, "Correct", f"Bonne réponse! Votre score est maintenant de {self.score}.")
        else:
            QtWidgets.QMessageBox.warning(self, "Incorrect", f"Faux! Le mot correct était: {self.current_word}")

        self.le_user_entry.clear()
        self.next_word()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    game = App()
    game.show()

    sys.exit(app.exec())

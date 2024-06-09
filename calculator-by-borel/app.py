from math import sqrt, pow
import sys

from PySide6 import QtWidgets


class Calculator(QtWidgets.QWidget):

    BUTTONS = [
        ("C", "Del", "(", ")"),
        ("%", "√", "x²", "1/x"),
        ("7", "8", "9", "/"),
        ("4", "5", "6", "*"),
        ("1", "2", "3", "-"),
        (".", "0", "+", "="),
    ]

    OPERATORS = ["+", "-", "*", "/", "=", "."]

    ERROR_STYLE = """
        bold=True;
        color: red;
        """

    NORMAL_STYLE = """
        bold=True;
        color: green;
        """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculatrice par Borel")
        self.setup_ui()

    def setup_ui(self):

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.le_result = QtWidgets.QLineEdit()
        self.le_operation = QtWidgets.QLineEdit()

        self.main_layout.addWidget(self.le_operation)
        self.main_layout.addWidget(self.le_result)

        for row in self.BUTTONS:
            h_layout = QtWidgets.QHBoxLayout()
            for button_text in row:
                button = QtWidgets.QPushButton(button_text)
                button.clicked.connect(self.compute)
                h_layout.addWidget(button)
            self.main_layout.addLayout(h_layout)

    def compute(self):
        sender = self.sender().text()
        current_text = self.le_operation.text()
        last_char = current_text[-1:]

        if sender in self.OPERATORS and (last_char == sender):
            return
        elif sender == "C":
            self.le_operation.clear()
            self.le_result.clear()
        elif sender == "Del":
            self.le_operation.setText(current_text[:-1])
        elif sender == "x²":
            self.le_operation.setText(f"{current_text}**2")
        elif sender == "√":
            self.le_operation.setText(f"{current_text[:-1]}sqrt({last_char})")
        elif sender == "1/x":
            self.le_operation.setText(f"1/({current_text})")
        elif sender == "%":
            self.le_operation.setText(f"{float(eval(current_text))/100}")
        elif sender == "=":
            try:
                result = eval(self.le_operation.text())
                self.le_result.setText(str(result))
                self.set_style()
            except Exception as err:
                self.le_result.setText("Il y a une erreur dans votre opération.")
                self.set_style("error")
        else:
            self.le_operation.setText(self.le_operation.text() + sender)

    def set_style(self,type:str="normal"):
        if type == "normal":
            self.le_result.setStyleSheet(self.NORMAL_STYLE)
        else:
            self.le_operation.setStyleSheet(self.ERROR_STYLE)
            self.le_result.setStyleSheet(self.ERROR_STYLE)
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win = Calculator()
    win.show()
    sys.exit(app.exec())

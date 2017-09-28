"""

    app.py

    This module starts the PyQt application.

"""


import sys
from PyQt5.QtWidgets import QApplication, QTextEdit, QWidget, QPushButton, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QLabel


class App(QWidget):

    def __init__(self):
        super(App, self).__init__()
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()

        titleLayout = QHBoxLayout()
        mainTitle = QLabel('Auto Word Suggestion')
        titleLayout.addWidget(mainTitle)
        titleLayout.setContentsMargins(0, 0, 0, 20)

        suggestionLayout = QGridLayout()
        for i in range(5):
            suggestionLayout.addWidget(QLabel('Test ' + str(i)), 0, i)
            suggestionLayout.addWidget(QLabel('Test %'), 1, i)
        suggestionLayout.setContentsMargins(0, 0, 0, 20)

        self.textArea = QTextEdit()
        self.btnClear = QPushButton('Clear Text Area')

        # Add event handlers
        self.btnClear.clicked.connect(self.clearTextArea)
        self.textArea.textChanged.connect(self.onTextChange)

        # Add all widgets and layouts to mainLayout:
        mainLayout.addLayout(titleLayout)
        mainLayout.addLayout(suggestionLayout)
        mainLayout.addWidget(self.textArea)
        mainLayout.addWidget(self.btnClear)

        self.setLayout(mainLayout)
        self.setWindowTitle('Kneser-Ney Word Prediction')

    def clearTextArea(self):
        self.textArea.clear()

    def onTextChange(self):
        text = self.textArea.toPlainText()
        lastToken = self.getLastToken(text)

        if not lastToken:
            return

        print(lastToken)


    def getLastToken(self, text):
        if not text:
            return None
        return text.strip().split()[-1]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.resize(800, 600)
    a.show()
    sys.exit(app.exec_())

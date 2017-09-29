"""

    app.py

    This module starts the PyQt application.

"""

import pickle
import os
import sys
from PyQt5.QtWidgets import QApplication, QTextEdit, QWidget, QPushButton, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from src.kneserNey import KneserNey


class App(QWidget):

    def __init__(self):
        super(App, self).__init__()
        with open(os.path.abspath('data/bigram-prob-dist/bigramProbDist.pkl'),
                  'rb') as file:
            self.bigramProbDist = pickle.load(file)
        self.initUI()

    def initUI(self):
        self.mainLayout = QVBoxLayout()

        self.titleFont = QFont('Helvetica Neue', 20)
        self.bodyFont = QFont('Helvetica Neue', 12)

        titleLayout = QHBoxLayout()
        mainTitle = QLabel('Auto Word Suggestion')
        mainTitle.setFont(self.titleFont)
        mainTitle.setAlignment(Qt.AlignCenter)
        titleLayout.addWidget(mainTitle)
        titleLayout.setContentsMargins(0, 0, 0, 20)

        self.suggestionLayout = QGridLayout()
        self.suggestionLayout.setContentsMargins(0, 0, 0, 20)

        self.textArea = QTextEdit()
        self.btnClear = QPushButton('Clear Text Area')

        # Add event handlers
        self.btnClear.clicked.connect(self.clearTextArea)
        self.textArea.textChanged.connect(self.onTextChange)

        # Add all widgets and layouts to mainLayout:
        self.mainLayout.addLayout(titleLayout)
        self.mainLayout.addLayout(self.suggestionLayout)
        self.mainLayout.addWidget(self.textArea)
        self.mainLayout.addWidget(self.btnClear)

        self.setLayout(self.mainLayout)
        self.setWindowTitle('Kneser-Ney Word Prediction')

    def onTextChange(self):
        text = self.textArea.toPlainText()
        lastToken = self.getLastToken(text)

        if not lastToken:
            return

        probabilityDist = self.bigramProbDist.get(lastToken, [])

        if not probabilityDist:
            return

        # Remove original suggestions:
        for i in reversed(range(self.suggestionLayout.count())):
            self.suggestionLayout.itemAt(i).widget().setParent(None)

        # Add new suggestions:
        for i in range(len(probabilityDist)):
            suggestionLabel = QLabel(probabilityDist[i][0])
            suggestionPercent = QLabel('{0:.2f}'
                .format(probabilityDist[i][1] * 100) + '%')
            suggestionLabel.setFont(self.bodyFont)
            suggestionPercent.setFont(self.bodyFont)
            self.suggestionLayout.addWidget(suggestionLabel, 0, i)
            self.suggestionLayout.addWidget(suggestionPercent, 1, i)

    def getLastToken(self, text):
        if not text:
            return None
        return text.rsplit(None, 1)[-1]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.resize(800, 600)
    a.show()
    sys.exit(app.exec_())

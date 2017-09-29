"""

    app.py

    This module starts the PyQt application.

"""

import pickle
import os
import sys
from PyQt5.QtWidgets import QApplication, QTextEdit, QWidget, QPushButton, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QLabel
from kneserNey import KneserNey


class App(QWidget):

    def __init__(self):
        super(App, self).__init__()
        with open(os.path.abspath('data/bigram-freq-dist/bigramFreqDist.pkl'), 'rb') as file:
            bigramFreqDist = pickle.load(file)
            self.kneserNey = KneserNey(bigramFreqDist, 0.75)
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()

        titleLayout = QHBoxLayout()
        mainTitle = QLabel('Auto Word Suggestion')
        titleLayout.addWidget(mainTitle)
        titleLayout.setContentsMargins(0, 0, 0, 20)

        self.suggestionLayout = QGridLayout()
        self.suggestionsLabel = []
        self.suggestionsPercentage = []
        self.suggestionLayout.setContentsMargins(0, 0, 0, 20)

        self.textArea = QTextEdit()
        self.btnClear = QPushButton('Clear Text Area')

        # Add event handlers
        self.btnClear.clicked.connect(self.clearTextArea)
        self.textArea.textChanged.connect(self.onTextChange)

        # Add all widgets and layouts to mainLayout:
        mainLayout.addLayout(titleLayout)
        mainLayout.addLayout(self.suggestionLayout)
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

        probabilityDist = self.kneserNey.predictNextWord(lastToken)

        if not probabilityDist:
            return

        # Remove original suggestions:
        for i in reversed(range(self.suggestionLayout.count())):
            self.suggestionLayout.itemAt(i).widget().setParent(None)

        # Add new suggestions:
        for i in range(len(probabilityDist)):
            self.suggestionLayout.addWidget(QLabel(probabilityDist[i][0]), 0, i)
            self.suggestionLayout.addWidget(QLabel('{0:.2f}'.format(probabilityDist[i][1] * 100)), 1, i)


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

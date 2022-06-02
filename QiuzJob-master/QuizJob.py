import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QPixmap

import sqlite3

questionCount = 0
maxPoints = 0

class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("First.ui", self)
        self.next.clicked.connect(self.gotoprofile)

    def gotoprofile(self):
        profile = ProfileScreen()
        widget.addWidget(profile)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class ProfileScreen(QDialog):
    def __init__(self):
        super(ProfileScreen, self).__init__()
        loadUi("Profile.ui", self)
        self.ButtonReady.clicked.connect(self.gotoquestions)

    def gotoquestions(self):
        questionSc = QuestionsScreen()
        widget.addWidget(questionSc)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class QuestionsScreen(QDialog):
    def __init__(self):
        global questionCount, maxPoints
        super(QuestionsScreen, self).__init__()
        loadUi("Questions.ui", self)
        self.done_btn.hide()
        self.questions_label.setText(QuestionsFarmer[questionCount])

        self.nextquestion.clicked.connect(self.question_changer_forward)
        self.prevquestion.clicked.connect(self.question_changer_backward)


    def question_changer_forward(self):
        global questionCount, maxPoints

        self.prevquestion.show()

        maxPoints += int(self.points.value())
        print(maxPoints)
        questionCount += 1
        self.questions_label.setText(QuestionsFarmer[questionCount])
        self.points.setValue(0)
        self.points_show.setText(str(maxPoints))


    def question_changer_backward(self):
        global questionCount, maxPoints

        self.nextquestion.show()

        questionCount -= 1
        maxPoints -= int(self.points.value())
        self.questions_label.setText(QuestionsFarmer[questionCount])
        self.points.setValue(0)
        self.points_show.setText(str(maxPoints))






QuestionsFarmer = ['croissant 1', 'croissant 2', 'croissant 3', 'croissant 4', 'croissant 5', 'lol']

# main

app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
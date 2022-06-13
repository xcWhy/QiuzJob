import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QPixmap

import sqlite3


class ProfileScreen(QDialog):
    global maxPoints

    def __init__(self, username):
        super(ProfileScreen, self).__init__()
        loadUi("Profile.ui", self)
        global job_index
        self.user = username
        self.greeting_label.setText(f'Greetings, {self.user}!')
        self.warning_label.hide()
        self.ButtonReady.clicked.connect(self.gotoquestions)
        self.prevLabels = [self.prevlabel1, self.prevlabel2, self.prevlabel3]
        self.bestLabels = [self.bestlabel1, self.bestlabel2, self.bestlabel3]
        self.refresh_btn.clicked.connect(self.refresh_page)
        if job_index == -1:
            self.theme_chooser()
        self.labels_text()

    def gotoquestions(self):
        global maxPoints
        if self.theme_box.currentText() == '---':
            self.job_cheker()
        else:
            self.theme_chooser()
            maxPoints = 0
            questionSc = QuestionsScreen()
            widget.addWidget(questionSc)
            widget.setCurrentIndex(widget.currentIndex() + 1)
            self.warning_label.hide()

    def labels_text(self):
        global maxPoints, prevText, bestText, job_text, prevJob, bestJob

        connection = sqlite3.connect("results.db")
        cur = connection.cursor()
        print("Successfully Connected to SQLite")

        cur.execute('SELECT theme, score FROM res_questions WHERE user = ?', (self.user,))

        rows = cur.fetchmany(3)

        print(rows)

        for i in range(len(rows)):
            self.prevLabels[i].setText(str(f'{rows[i][0]} : {rows[i][1]}'))
            self.bestLabels[i].setText(str(f'{rows[i][0]} : {rows[i][1]}'))


    def theme_chooser(self):
        global job_index, job_text
        if self.theme_box.currentText() == 'Farmer':
            job_index = 0
            job_text = self.theme_box.currentText()
            print(job_index)
        elif self.theme_box.currentText() == 'Waitress':
            job_index = 1
            job_text = self.theme_box.currentText()
            print(job_index)
        elif self.theme_box.currentText() == 'Chef':
            job_index = 2
            job_text = self.theme_box.currentText()
            print(job_index)
        elif self.theme_box.currentText() == 'Doctor':
            job_index = 3
            job_text = self.theme_box.currentText()
            print(job_index)
        elif self.theme_box.currentText() == 'Programmer':
            job_index = 4
            job_text = self.theme_box.currentText()
            print(job_index)

    def job_cheker(self):
        self.warning_label.show()

    def refresh_page(self):
        global prevJob, bestJob, job_text, maxPoints

        connection = sqlite3.connect("results.db")
        cur = connection.cursor()
        print("Successfully Connected to SQLite")

        if job_text != '' and maxPoints != 0:

            cur.execute("INSERT INTO res_questions (theme, score, user) VALUES (?, ?, ?);",
                        (job_text, maxPoints, self.user))
            connection.commit()

        #self.theme_chooser()
        self.labels_text()

        job_text = ''
        maxPoints = 0



class QuestionsScreen(QDialog): #oshte edna funkciq kaoqto da refreshva i da ne precakva vyprosite
    def __init__(self):
        global questionCount, maxPoints, job_index, questionCount
        super(QuestionsScreen, self).__init__()
        loadUi("Questions.ui", self)
        self.refresh()
        #self.done_btn.hide()
        self.prevquestion.hide()
        self.points.setMaximum(100)
        self.isVis = self.done_btn.isVisible

        self.questions_label.setText(Questions[job_index][questionCount])

        self.nextquestion.clicked.connect(self.question_changer_forward)
        self.prevquestion.clicked.connect(self.question_changer_backward)
        self.done_btn.clicked.connect(self.ready)


    def question_changer_forward(self):
        global questionCount, maxPoints, job_index

        self.prevquestion.show()

        maxPoints += int(self.points.value())
        print(maxPoints)
        questionCount += 1

        if questionCount == 4:
            self.btn_shower(self.nextquestion)
            self.done_btn.show()

        self.questions_label.setText(Questions[job_index][questionCount])  # opravi tukkkk <<<< trqbva da e s dboivna skoba
        self.points.setValue(0)
        self.points_show.setText(str(maxPoints))


    def question_changer_backward(self):
        global questionCount, maxPoints, job_index

        self.nextquestion.show()

        questionCount -= 1

        if questionCount == 0:
            self.btn_shower(self.prevquestion)

        maxPoints -= int(self.points.value())
        self.questions_label.setText(Questions[job_index][questionCount]) # opravi tukkkk <<<<
        self.points.setValue(0)
        self.points_show.setText(str(maxPoints))


    def btn_shower(self, btn):
        self.btn = btn
        self.btn.hide()

    def refresh(self):
        global questionCount, job_index
        questionCount = 0
        job_index = job_index
        self.questions_label.setText(Questions[job_index][questionCount])

    def ready(self):
        global maxPoints
        maxPoints += int(self.points.value())
        profile = ProfileScreen()
        widget.addWidget(profile)
        widget.setCurrentIndex(widget.currentIndex() - 1)
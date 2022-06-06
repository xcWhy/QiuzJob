import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QPixmap

import sqlite3

questionCount = 0
maxPoints = 0


prevText = ['0', '0', '0']
bestText = ['0', '0', '0']
prevJob = ['0', '0', '0']
bestJob = ['0', '0', '0']
job_index = -1
job_text = str()


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
    global maxPoints
    def __init__(self):
        super(ProfileScreen, self).__init__()
        loadUi("Profile.ui", self)
        global job_index
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
        print(prevText)
        bestText.sort(reverse=True)
        print(bestText)
        print('-----')
        for i in range(0, len(self.prevLabels)):
            self.prevLabels[i].setText(str(f'{prevJob[i]} : {prevText[i]}'))
        for j in range(0, len(self.bestLabels)):
            self.bestLabels[j].setText(str(f'{bestJob[j]} : {bestText[j]}'))

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

        if job_text != '' and maxPoints != 0:
            prevText.insert(0, str(maxPoints))
            bestText.insert(0, str(maxPoints))

            prevJob.insert(0, str(job_text))
            bestJob.insert(0, str(job_text))

        if len(prevJob) > 3 or len(bestJob) > 3 or len(prevText) > 3 or len(bestText) > 3:
            prevJob.pop(len(prevJob) - 1)
            bestJob.pop(len(bestJob) - 1)
            prevText.pop(len(prevText) - 1)
            bestText.pop(len(bestText) - 1)

        self.theme_chooser()
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






Questions = [['croissant 1', 'croissant 2', 'croissant 3', 'croissant 4', 'croissant 5', 'lol'],
             ['2croissant 1', '2croissant 2', '2croissant 3', '2croissant 4', '2croissant 5', 'lol'],
             ['3croissant 1', '3croissant 2', '3croissant 3', '3croissant 4', '3croissant 5', 'lol'],
             ['4croissant 1', '4croissant 2', '4croissant 3', '4croissant 4', '4croissant 5', 'lol'],
             ['5croissant 1', '5croissant 2', '5croissant 3', '5croissant 4', '5croissant 5', 'lol'],
             ]

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

import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QPixmap
import requests
import random

import sqlite3

#da se sloji da se smenq teksta ri profesiite - da ti dava koq si izbral // chrez ogromen buton

#da se napravi mqsto otkydeto potrebitelq shte moje da si vijda rezultatite (vischkite)
#forgot password

questionCount = 0
maxPoints = 0

job_index = -1
job_text = str()
questionsTest = []

class WelcomeScreen(QDialog):
    def __init__(self): #we call the main functions from here
        super(WelcomeScreen, self).__init__()
        loadUi("First.ui", self)
        self.Login_btn.clicked.connect(self.gotologin)
        self.Signin_btn.clicked.connect(self.gotosignin)

    def gotologin(self): #the function which allows to switch to the "log in screen"
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotosignin(self): #the function which allows to switch to the "sign up screen"
        signin = SigninScreen()
        widget.addWidget(signin)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class SigninScreen(QDialog): #sign up object
    def __init__(self): #main function which calls everything else in the class
        super(SigninScreen, self).__init__()
        loadUi("CreateAccScreen.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.gologin_btn.hide() #we hide some buttons and labels here
        self.warning_label.hide()
        self.confirm_label.hide()
        self.create_btn.clicked.connect(self.createAcc)


    def createAcc(self): #we create the account of the person here
        username = self.usernamefield.text()
        password = self.passwordfield.text()# we get the strings of both text boxes

        if len(username) == 0 or len(password) == 0:
            self.warning_label.show()

        else:
            connection = sqlite3.connect("test2.db")
            cur = connection.cursor()
            print("Successfully Connected to SQLite")

            cur.execute("INSERT INTO login_info (username, password) VALUES (?, ?);",
                        (username, password))
            connection.commit() # we insert user's username and password into the database

            cur.close()

            self.gologin_btn.show()
            self.gologin_btn.clicked.connect(self.gotologin)

    def gotologin(self): #we go to login
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class LoginScreen(QDialog): #log in class
    def __init__(self): # main
        super(LoginScreen, self).__init__()
        loadUi("LoginScreen.ui", self)
        #self.wrong_label.hide()
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_btn.clicked.connect(self.loginfunc)

    def loginfunc(self): #here we check if the information is in the database
        username = self.usernamefield.text()
        password = self.passwordfield.text()# we get the strings from the text boxes

        if len(username) == 0 or len(password) == 0:
            self.wrong_label.show()

        else:
            print('hah')
            connection = sqlite3.connect("test2.db")
            cur = connection.cursor()
            #query = 'SELECT password FROM login_info WHERE username =\''+username+"\'"
            cur.execute("SELECT password FROM login_info WHERE username = ?", (username,)) #we search for a password with this given username
            result_pass = cur.fetchone()[0]
            if result_pass == password: #if correct we go to the profile screen
                print('weeeeeeeeeeeee')
                self.gotoprofile(username)
            else:
                print('liosho >:(')
                self.wrong_label.show() #if not correct we show a warning label

    def gotoprofile(self, username): #we create a profile object
        profile = ProfileScreen(username)
        widget.addWidget(profile)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ProfileScreen(QDialog):
    global maxPoints

    def __init__(self, username): #
        super(ProfileScreen, self).__init__()
        loadUi("Profile.ui", self)
        global job_index
        self.user = username
        self.greeting_label.setText(f'Greetings, {self.user}!')
        self.warning_label.hide()
        self.ButtonReady.clicked.connect(self.gotoquestions)

        self.prevLabels = [self.prevlabel1, self.prevlabel2, self.prevlabel3] #those lists are for showing the results of the user
        self.bestLabels = [self.bestlabel1, self.bestlabel2, self.bestlabel3]

        self.refresh_btn.clicked.connect(self.refresh_page)
        if job_index == -1: #if the person hasn't chosen a profession we give him a warning to do so
            self.theme_chooser()
        self.labels_text()

        self.us_btn.clicked.connect(self.openaboutus)
        self.ourWindow = OurScreen(self.user)

    def openaboutus(self): # it's the little window which opens when we click "about us"
        self.ourWindow.show()

    def labels_text(self): #here we show all the user's results

        connection = sqlite3.connect("results.db")
        cur = connection.cursor()
        print("Successfully Connected to SQLite")

        cur.execute('SELECT theme, score FROM res_questions WHERE user = ?', (self.user,))
        rows = cur.fetchall()
        rows1 = cur.fetchall()
        rows1.sort()

        max_results = []
        latest = []

        for i in range(len(rows)-1, -1, -1): #we choose the latest 3 results from the database
            latest.append(rows[i])
            if len(latest) == 3:
                break

        #print("results:" + str(latest))

        for j in range(0, len(rows)):
            max_results.append(rows[j])
        #print("unsorted:" + str(max))

        for j in range(0, len(max_results)): # here we choose the best 3 results from the database
            for k in range(j + 1, len(max_results)):
                if max_results[j][1] < max_results[k][1]:
                    a = max_results[j]
                    max_results[j] = max_results[k]
                    max_results[k] = a
        #print("rows:" + str(max))


        for i in range(len(latest)):
            self.prevLabels[i].setText(str(f'{latest[i][0]} : {latest[i][1]}%'))
            self.bestLabels[i].setText(str(f'{max_results[i][0]} : {max_results[i][1]}%')) #here we show the user his results in the 3 * 2 labels

    def theme_chooser(self): # here we get the information - which profession has the user chosen
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


    def refresh_page(self): # we refresh the page the button is clicked
        global prevJob, bestJob, job_text, maxPoints

        percents = (maxPoints * 100) / 500 #we make the results into percents

        connection = sqlite3.connect("results.db")
        cur = connection.cursor()
        print("Successfully Connected to SQLite")

        if job_text != '' and maxPoints != 0:
            cur.execute("INSERT INTO res_questions (theme, score, user) VALUES (?, ?, ?);", #we insert the user's results into the database
                        (job_text, percents, self.user))
            connection.commit()

        # self.theme_chooser()
        self.labels_text() # we show the new results

        job_text = '' #we reset these
        maxPoints = 0

    def gotoquestions(self): # we create another object "question screen"
        global maxPoints
        if self.theme_box.currentText() == '---':
            self.warning_label.show()
        else:
            self.theme_chooser()
            maxPoints = 0
            questionSc = QuestionsScreen(self.user)
            widget.addWidget(questionSc)
            widget.setCurrentIndex(widget.currentIndex() + 1)
            self.warning_label.hide()


class OurScreen(QDialog): #the little screen

    def __init__(self, user):
        super(OurScreen, self).__init__()
        loadUi("info_screen.ui", self)
        self.warn_label.hide()
        self.user = user

        self.send_btn.clicked.connect(self.MessageSender)

    def MessageSender(self):
        #print(1)
        message = f'~~From username: "{self.user}"~~\n' + self.box.toPlainText()
        print(message)
        token = "ODIyODI0MzkyNTc1OTQyNjU2.Gv-2aQ.sKFJWsCT1sCSbLsiogiwlaQzvDTu8C1vLGy0MU" #a special token which should be changed almost every hour
        channel_id = 986276615849926668 #the id of the server / channel which we want to send the message to

        url = 'https://discord.com/api/v9/channels/{}/messages'.format(channel_id) # the api link which we give - it sends the msgs to the given link
        data = {'content': message}
        header = {'authorization': token}

        r = requests.post(url, data=data, headers=header)
        print(r.status_code)

        #self.send_btn.hide()

        # print(len(token))


class QuestionsScreen(QDialog):  # question screen class
    def __init__(self, user):
        global questionCount, maxPoints, job_index, questionCount, job_text, questionNum, questionsTest
        super(QuestionsScreen, self).__init__()
        loadUi("Questions.ui", self)

        self.hehe_btn.show() #the big button which shows when we go to the question screen

        print(job_text)

        questionsTest = []

        while len(questionsTest) != 5: # here we choose 5 random questions for the profession
            index = random.randint(0, 9)
            if Questions[job_index][index] not in questionsTest:
                questionsTest.append(Questions[job_index][index])

        self.hehe_btn.clicked.connect(self.hehe_func)

        self.user = user
        self.refresh()
        # self.done_btn.hide()
        self.prevquestion.hide()
        self.warn_label.hide()
        self.points.setMaximum(100) # we lock the max to be 100
        self.isVis = self.done_btn.isVisible

        #self.questions_label.setText(f'{questionCount + 1}. {questionsTest[questionCount]}')

        self.nextquestion.clicked.connect(self.question_changer_forward)
        self.prevquestion.clicked.connect(self.question_changer_backward)
        self.done_btn.clicked.connect(self.ready)

    def hehe_func(self): # the main reason for the 'hehe_btn' is to refresh the whole screen
        global job_text, questionCount, maxPoints, job_index

        maxPoints = 0
        questionCount = 0

        self.proff_label.setText(f'How suitable are you for a {job_text}?')
        self.questions_label.setText(f'{questionCount + 1}. {questionsTest[questionCount]}')
        self.points_show.setText(str(maxPoints))
        self.points.setValue(0)
        self.prevquestion.hide()
        self.nextquestion.show()

        self.hehe_btn.hide()


    def question_changer_forward(self): #it shows us the next question
        global questionCount, maxPoints, job_index, questionNum, questionsTest

        #questionNum = random.randint(0, 9)

        if self.points.value() == 0:
            self.warn_label.show()

        else:
            self.prevquestion.show()

            maxPoints += int(self.points.value())
            print(maxPoints)
            questionCount += 1

            if questionCount == 4:
                self.btn_shower(self.nextquestion)
                self.done_btn.show()

            self.questions_label.setText(f'{questionCount + 1}. {questionsTest[questionCount]}')
            self.points.setValue(0)
            self.points_show.setText(str(maxPoints))
            self.warn_label.hide()

    def question_changer_backward(self): #it shows us the previous question
        global questionCount, maxPoints, job_index, questionNum, questionsTest

        #questionNum = random.randint(0, 9)

        if self.points.value() == 0:
            self.warn_label.show()

        else:
            self.nextquestion.show()

            questionCount -= 1

            if questionCount == 0:
                self.btn_shower(self.prevquestion)

            maxPoints -= int(self.points.value())
            self.questions_label.setText(f'{questionCount + 1}. {questionsTest[questionCount]}')  # opravi tukkkk <<<<
            self.points.setValue(0)
            self.points_show.setText(str(maxPoints))
            self.warn_label.hide()

    def btn_shower(self, btn):
        self.btn = btn
        self.btn.hide()


    def refresh(self): # we dont know if that does anything
        global questionCount, job_index, questionsTest
        questionCount = 0
        job_index = job_index
        self.questions_label.setText(f'{questionCount + 1}. {questionsTest[questionCount]}')

    def ready(self): #the ready button which send us back to the profile screen
        global maxPoints
        self.hehe_btn.show()
        maxPoints += int(self.points.value())
        profile = ProfileScreen(self.user)
        widget.addWidget(profile)
        widget.setCurrentIndex(widget.currentIndex() - 1)



Questions = [['Do you have problem-solving skills? / Are you creative\n / can think outside the box?', 'Do you have mechanical skills / you can repair things easy?', 'Do you have interpersonal/communication skills?', 'Do you maintain great physical stamina?', 'Are you in good health?', 'Are you good at organizing and managing tasks?','Can you remain flexible and adapt easily when faced to unexpected changes in weather?','Are you up-to-date with technology?','Can you work in teams? /\n Are you good at teamworks?','Could you describe yourself as trustworthy?'],
             ['Do you have decent communication and listening skills?', 'Could you describe yourself as being great at multitasking?', 'Do you happen to have good memory?', 'Are you good at following instructions?', 'Do you know more than one language?', 'Do you have high stamina?','Would you be able to maintain proffesionalism in bad scenarios?','Do you have critical thinking?',' Would you describe yourself as patient?','Do you happen to have social perceptiveness skills?'],
             ['Do you like cooking?', 'Do you use spices well?', 'Can you estimate what kind of flavours supplement each other?', 'Do you think the food is not only for the body but also for the soul?', 'Do you like eating?', 'Do you like tasting new kind of food?','Are people impressed by your dishes?','Can you prepare something delicious?','Do you know which the five basic sauces are?','Do you know some unknown products?'],
             ['Are you responsible?', 'Do you put the human life on first position?', 'Do you love studying?', 'Are you interested in Biology and Chemistry?', 'Are you resistant to mental pressure?', 'You are not afraid of blood?', 'You are not afraid of needles?', 'Do you have the necessary education?', 'Are you precise?', 'Do you like helping other people?'],
             ['Do you know some programming languages?', 'Are you interested in technologies?', 'Do like Maths?', 'Can you think logically?', 'Do you like learning new things?', 'Are you good at project management?','Do you know basic data structures and algorithms?','Do you happen to have great problem solving skills?','Would you describe yourself as patient?','Would be able to work in teamwork?'],
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

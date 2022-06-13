import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QPixmap

import sqlite3


connection = sqlite3.connect("results.db")
cur = connection.cursor()
print("Successfully Connected to SQLite")

user = 'eli'

cur.execute('SELECT theme, score FROM res_questions WHERE user = ?', (user,))

rows = cur.fetchmany(3)

print(rows)

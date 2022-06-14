import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QPixmap

import sqlite3

connection = sqlite3.connect("results.db")
cur = connection.cursor()
print("Successfully Connected to SQLite")

cur.execute('SELECT theme, score FROM res_questions WHERE user = ?', ('eli',))

rows = cur.fetchall()

rezultati = []

for i in range(len(rows) - 1, 0, -1):
    rezultati.append(rows[i])
    if len(rezultati) == 3:
        break


print(rezultati)

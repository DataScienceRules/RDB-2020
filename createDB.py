import sqlite3
import random
import time
import datetime
import os
import csv
import tkinter
from tkinter import filedialog, messagebox
from venv.data_generator import generate_data
from venv.gui import gui

def create_db():
    try:
        connection = sqlite3.connect('zemedelske_stroje.db')
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Jednotka(seriove_cislo VARCHAR PRIMARY KEY )")
        cursor.execute("CREATE TABLE IF NOT EXISTS Stroj(vin VARCHAR PRIMARY KEY )")
        cursor.execute("CREATE TABLE IF NOT EXISTS Konfigurace(konfig_id VARCHAR PRIMARY KEY )")
        cursor.execute("CREATE TABLE IF NOT EXISTS Kombinace(seriove_cislo VARCHAR, vin VARCHAR, konfig_id VARCHAR, od TIMESTAMP, do TIMESTAMP, PRIMARY KEY(seriove_cislo, vin, konfig_id, od, do), FOREIGN KEY(seriove_cislo) REFERENCES Jednotka(seriove_cislo), FOREIGN KEY(vin) REFERENCES Stroj(vin),  FOREIGN KEY(konfig_id) REFERENCES Konfigurace(konfig_id))")
        cursor.execute("CREATE TABLE IF NOT EXISTS Zaznamy(zaznam_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, cas timestamp, seriove_cislo VARCHAR, FOREIGN KEY(seriove_cislo) REFERENCES Jednotka(seriove_cislo))")
        cursor.execute("CREATE TABLE IF NOT EXISTS Data_(data_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, zaznam_id INT, atribut VARCHAR, bit_val BIT, float_val FLOAT, FOREIGN KEY(zaznam_id) references Zaznamy(zaznam_id))")

        connection.commit()
        connection.close()
    except sqlite3.Error as err:
        print(err)


def insert_into_db(cursor):
    with open("jednotky.csv", "r", buffering=1, encoding="utf-8") as jednotky:
        jednotky = jednotky.readlines()
        for one in jednotky:
            cursor.execute("INSERT INTO Jednotka VALUES(?)", [one[:-2]])
    with open("stroje.csv", "r", buffering=1, encoding="utf-8") as stroje:
        stroje = stroje.readlines()
        for one in stroje:
            cursor.execute("INSERT INTO Stroj VALUES(?)", [one[:-2]])
    with open("konfigurace.csv", "r", buffering=1, encoding="utf-8") as konfigy:
        konfigy = konfigy.readlines()
        for one in konfigy:
            cursor.execute("INSERT INTO Konfigurace VALUES(?)", [one[:-2]])
    with open("kombinace.csv", "r", buffering=1, encoding="utf-8") as kombinace:
        kombinace = kombinace.readlines()
        for one in kombinace:
            one = one.split(",")
            cursor.execute("INSERT INTO Kombinace VALUES(?,?,?,?,?)", (one[2], one[0], one[1], one[3], one[4]))
    with open("zaznamy.csv", "r", buffering=1, encoding="utf-8") as zaznamy:
        zaznamy = zaznamy.readlines()
        for one in zaznamy:
            one = one.split(",")
            cursor.execute("INSERT INTO Zaznamy(cas, seriove_cislo) VALUES(?, ?)", (one[1], one[0]))
    with open("data.csv", "r", buffering=1, encoding="utf-8") as data:
        data = data.readlines()
        for one in data:
            one = one.split(",")
            if one[2] == '':
                one[2] = None
            if one[3] == '\n':
                one[3] = None
            cursor.execute("INSERT INTO Data_(zaznam_id, atribut, bit_val, float_val) VALUES(?,?,?,?)", (one[0], one[1], one[2], one[3]))



connection = sqlite3.connect('zemedelske_stroje.db')
cursor = connection.cursor()
'''

cursor.execute("DELETE FROM Jednotka")
cursor.execute("DELETE FROM Stroj")
cursor.execute("DELETE FROM Konfigurace")
cursor.execute("DELETE FROM Zaznamy")
cursor.execute("DELETE FROM Kombinace")
cursor.execute("DELETE FROM Data_")



generate_data()

create_db()
insert_into_db(cursor)
'''



pocet_stroju = cursor.execute("select seriove_cislo from Jednotka limit 10")
print(pocet_stroju.fetchall())

training_query = cursor.execute("select * from Zaznamy where seriove_cislo like '88855662024772572239' ").fetchall()
print(training_query)

pocet_stroju = cursor.execute("select * from Zaznamy limit 10")
print(pocet_stroju.fetchall())
connection.commit()
connection.close()

gui()

print("done")
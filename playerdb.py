import sqlite3
from cards import Card


class Player:

    players = {}

    @staticmethod
    def create_database(): # Δημιουργία βάσης στην περίπτωση που δεν υπάρχει
        try:
            connnection = sqlite3.connect("CardGame_database.db")
            with connnection:
                cursor = connnection.cursor()
                sql = 'CREATE TABLE players (person_id INTEGER PRIMARY KEY AUTOINCREMENT, name text ,points integer);'
                cursor.execute(sql)
                return True
        except sqlite3.Error: return False

    @staticmethod
    def players_number(): # μέθοδος με την οποία μετράμε το πλήθος των παικτών
        try:
            connection = sqlite3.connect("CardGame_database.db")
            with connection:
                cursor = connection.cursor()
                sql = "SELECT count (*) from players;" # Συνάρτηση count της sql η οποία μετράει το πλήθος των παιχτών στον πίνακα players
                cursor.execute(sql)
                return cursor.fetchone()[0]
        except sqlite3.Error:
            return 0

    @staticmethod
    def show_records():  # Συνάρτηση προβολής των εγγραφών του πίνακα table
        try:
            connection = sqlite3.connect("CardGame_database.db") # Σύνδεση με τη βάση δεδομένων με τη μέθοδο connect της sqlite3
            with connection:
                cursor = connection.cursor() # ορίζουμε έναν δρομέα ο οποίος εισάγει εντολές στη βάση δεδομένων
                sql = "SELECT * from players;"
                cursor.execute(sql) # ο κέρσορας εκτελεί την εντολή sql
                records = cursor.fetchall()  # Με τη μέθοδο fetchall επιστρέφουμε όλα τα αποτελέσματα σε μία μεταβλητή
                for rec in records: # Με τη δομή επανάληψης εμφανίζουμε όλα τα δεδομένα
                    print(rec)
        except sqlite3.Error as er:
            print(er)

    def __init__(self,name ,person_id=None, points=0, new=False):# Ειδική μέθοδος που αρχικοποιεί τα χαρακτηριστικά του κάθε παίχτη
        self.person_id = person_id
        self.name = name
        self.points = points

        Player.players[self.name] = self.points
        if new:
            self.insert_records()

    def insert_records(self):  # Μέθοδος εισαγωγής παίχτη
        try:
            connection = sqlite3.connect("CardGame_database.db")
            with connection:
                cursor = connection.cursor()
                sql = "INSERT INTO players (name,points) VALUES (?,?);"
                cursor.execute(sql, (self.name,self.points))
        except sqlite3.Error as er:
            print(er)

    def set_points(self, points,name):
        self.points = points
        try:
            connection = sqlite3.connect("CardGame_database.db")
            with connection:
                cursor = connection.cursor()
                sql = "UPDATE players set points ='{}' WHERE name = '{}';".format(points, name)
                cursor.execute(sql)
        except sqlite3.Error as er:
            print(er)

    def calculate_value(self, card):
        if card.isdigit():
            return int(card)
        elif card == 'A':
            return 1
        else:
            return 10

    def delete_records(self,person_id):  # Συνάρτηση διαγραφής παίχτη
        try:
            connection = sqlite3.connect("CardGame_database.db")
            with connection:
                cursor = connection.cursor()
                sql = "DELETE  FROM players where person_id =='{}';".format(person_id)  # Ερώτημα (query) για τη διαγραφή του μαθητή βάση του κωδικού του από τον πίνακα students
                cursor.execute(sql) # O κέρσορας εκτελεί την εντολή που καταχωρείται στη μεταβλητή sql
        except sqlite3.Error as er:
            print(er)

    def __repr__(self):
        return self.name, self.points

    def __str__(self):
        for key, value in Player.players.items():
            return key , value


import random
import tkinter as tk
import time
from tkinter import filedialog, messagebox, simpledialog
from game import Game , Player
import sqlite3

global card_1, card_2

class Card: # κλάση τραπουλόχαρτο

    def __init__(self, value, symbol): # H __init__ κατασκευάζει τα αντικείμενα τραπουλόχαρτα
        self._value = value  # Δήλωση παραμέτρων που αφορούν την τιμή και το σύμβολο του κάθε τραπουλόχαρτου
        self._symbol = symbol

    @property
    def value(self): # Επιστρέφει τις κάρτες self._face value.
        return self._value

    @property
    def symbol (self):  # Επιστρέφει τις κάρτες self._face value.
        return self._symbol

    def __str__(self):
        return self.value + self.symbol

    def __format__(self, format_spec):
        return f'{str(self):{format}}'


class Cards:
    ''' Δημιουργία κλάσης Τράπουλα την οποία θα την χρησιμοποιήσουμε στο παιχνίδι μας'''
    values = ['A', '2', '3', '4', '5', '6', '7', '8','9', '10', 'J', 'Q', 'K']
    symbols = ['♣', '♦','♥','♠' ]

    def __init__(self):
        self.full_cards = [] # λίστα που η οποία περιέχει τα χαρτιά από την αρχική τράπουλα
        self.collected_cards = [] # Λίστα η οποία μαζεύει τα χαρτιά που έχουν βρεθεί ίδια και τα ανοίγει
        self.saw_cards = {} # Λεξικό το οποίο περιέχει για κλειδιά την θέση του
                            # χαρτιού που άνοιξε και τιμή τα χαρακτηριστικά του
        self.number = 13
        self.char = ""

    def pie(self): # Μέθοδος ανακατέματος τράπουλας
        random.shuffle(self.full_cards) # καλούμε τη μέθοδο shuffle της κλάσης random με όρισμα self.full_deck

    def collect(self): # μέθοδος με την οποία μαζεύουμε όλα τα τραπουλόχαρτα και δημιουργούμε ξανά την τράπουλα
        self.full_cards = self.full_cards + self.collected_cards
        self.collected_cards = []

    def saw(self,card1,card2,card3 = None): # Μέθοδος με την οποία παίρνουμε τα φύλλα που έχει
        # επιλέξει ο παίχτης και ελέγχει εάν τα
        for saw_card in card1,card2,card3:
            if saw_card is None:
                continue
            if self.full_cards[saw_card] in self.collected_cards:
                continue
            else:
                self.saw_cards[saw_card+1] = self.full_cards[saw_card]
        for i in self.collected_cards:
            if i in self.saw_cards:
                self.saw_cards.pop(i)

        for key , value in self.saw_cards.items():
            print(key,value )

    def __str__(self): # Ειδική μέθοδος η οποία μας επιστρέφει την τράπουλα σε πίνακα 4x13
        c = ''
        counter = 0
        for i in self.full_cards:
            c = c + str(i) + ' '
            counter += 1
            if counter % self.number == 0:
                c = c + '\n'
        return c

    def __format__(self, format_spec):
        return  f'{str(self)}:{format}'

    def d_level(self,level): # Μέθοδος που ανάλογα με το επίπεδο δυσκολίας εμφανίζει διαφορετικό αριθμό φύλλων
        if level == 1:
            self.closed_cards(level, 4)
        elif level == 2:
            self.closed_cards(level, 10)
        elif level == 3:
            self.closed_cards(level, 13)

    def closed_cards(self, level,number):
        for i in self.symbols:  # Κατασκευάστρια μέθοδο τράπουλας
            if level == 1:
                for j in Cards.values[9:]:
                    self.full_cards.append(Card(j, i))
            if level == 2:
                for j in Cards.values[:10]:
                    self.full_cards.append(Card(j, i))
            if level == 3:
                for j in Cards.values:
                    self.full_cards.append(Card(j, i))
        self.number = number
        self.pie()
        counter = 0
        for i,j in enumerate(self.full_cards):
            self.char = self.char + str(i+1) + ' '
            counter += 1
            if counter % number == 0:
                self.char = self.char + '\n'

    def open_cards(self):
        for value, card in enumerate(self.full_cards):
            if card in self.collected_cards:
                print(value+1,card)


class CardImages():
    images = {}

    def __init__(self):
        self.spritesheet = tk.PhotoImage(
            file="../CardMatchingGame/cards2.gif")  # Εκχώρηση ενός αντικειμένου photoImage μέσα σε κάποια τοπική μεταβλητή
        self.card_width = 79  # 79px πλάτος                              #Η PhotoImage παίρνει σαν παράμετρο την εικόνα
        self.card_height = 123  # 123 px ύψος
        self.num_sprintes = 13  # Διαδοχικός αριθμός εικόνων
        self.last_img = None
        line = 0
        for x in ['♣', '♦','♥','♠' ]:
            CardImages.images[x] = [self.subimage(self.card_width * i, line, self.card_width * (i + 1),self.card_height + line) for i in range(self.num_sprintes)]
            line += self.card_height
        CardImages.images["b"] = self.subimage(0, line, self.card_width, self.card_height + line)

    def subimage(self, l, t, r, b):  # Μέθοδος με την οποία μπορούμε να πάρουμε να πάρουμε ένα τμήμα από μία εικόνα
        print(l, t, r,b)  # l,t,r,b  τα όρια της εικόνας που θέλουμε να περικόψουμε από την κύρια εικόνα "spritesheet"
        dst = tk.PhotoImage()  # ορίζουμε ένα αντικείμενο PhotoImage χωρίς αναφορά
        dst.tk.call(dst, 'copy', self.spritesheet, '-from', l, t, r, b, '-to', 0, 0)
        return dst

    def showimage(self, canvas, x, y, symbol, value):
        self.last_img = canvas.create_image(x, y, image=self.images[symbol][value], anchor="nw")
            #Το anchor το ορίζουμε με nw ώστε οι συντεταγμένες των φύλλων να καθορίζονται από εμάς


class GUICard():

    tableCards = {}

    def __init__(self, card, canvas):
        self.canvas = canvas
        self.value = card.value
        self.symbol = card.symbol
        self.position = None
        self.image = None
        GUICard.tableCards[card] = self

    def _open_image(self):
        if self.face:
            return CardImages.images[self.symbol][Cards.values.index(self.value)]
        else:
            return CardImages.images['b']

    def set_face(self,face):
        if self.position and face != self.face:
            self.face = face
            self.canvas.itemconfig(self.image,image = self._open_image())
        else:
            self.face = face

    def set_position(self, new_position):
        if not self.position: self.position = new_position
        if not self.image:
            self.image = self.canvas.create_image(*self.position, image =  self._open_image())
        self.canvas.itemconfig(self.image, anchor='nw')

    def __str__(self):
        out = self.value + self.symbol
        if self.position:
            out += '['+str(self.position[0])+','+str(self.position[1])+']'
        return out


class Human_Player():
    players = {}

    @staticmethod
    def create_database():  # Δημιουργία βάσης στην περίπτωση που δεν υπάρχει
        try:
            connnection = sqlite3.connect("CardGame_database.db")
            with connnection:
                cursor = connnection.cursor()
                sql = 'CREATE TABLE players (person_id INTEGER PRIMARY KEY AUTOINCREMENT, name text ,points integer);'
                cursor.execute(sql)
                return True
        except sqlite3.Error:
            return False

    @staticmethod
    def players_number():  # μέθοδος με την οποία μετράμε το πλήθος των παικτών
        try:
            connection = sqlite3.connect("CardGame_database.db")
            with connection:
                cursor = connection.cursor()
                sql = "SELECT count (*) from players;"  # Συνάρτηση count της sql η οποία μετράει το πλήθος των παιχτών στον πίνακα players
                cursor.execute(sql)
                return cursor.fetchone()[0]
        except sqlite3.Error:
            return 0

    @staticmethod
    def show_records():  # Συνάρτηση προβολής των εγγραφών του πίνακα table
        try:
            connection = sqlite3.connect(
                "CardGame_database.db")  # Σύνδεση με τη βάση δεδομένων με τη μέθοδο connect της sqlite3
            with connection:
                cursor = connection.cursor()  # ορίζουμε έναν δρομέα ο οποίος εισάγει εντολές στη βάση δεδομένων
                sql = "SELECT * from players;"
                cursor.execute(sql)  # ο κέρσορας εκτελεί την εντολή sql
                records = cursor.fetchall()  # Με τη μέθοδο fetchall επιστρέφουμε όλα τα αποτελέσματα σε μία μεταβλητή
                for rec in records:  # Με τη δομή επανάληψης εμφανίζουμε όλα τα δεδομένα
                    print(rec)
        except sqlite3.Error as er:
            print(er)

    def __init__(self,canvas,cards, name="", points=0, parametros = False,person_id=None,*kartes):
        Player.count += 1
        self.create_database()
        if parametros:
            self.name = simpledialog.askstring("Title", "Το όνομά του παίχτη {}:".format(Player.count))
        self.person_id = person_id
        self.canvas = canvas
        self.player_count = Player.count
        self.points = points
        self.kartes = kartes
        if parametros:
            self.insert_records()
        self.c = cards
        self.active = False
        self.play = False



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

    def delete_records(self,person_id):  # Συνάρτηση διαγραφής παίχτη
        try:
            connection = sqlite3.connect("CardGame_database.db")
            with connection:
                cursor = connection.cursor()
                sql = "DELETE  FROM players where person_id =='{}';".format(person_id)  # Ερώτημα (query) για τη διαγραφή του μαθητή βάση του κωδικού του από τον πίνακα students
                cursor.execute(sql) # O κέρσορας εκτελεί την εντολή που καταχωρείται στη μεταβλητή sql
        except sqlite3.Error as er:
            print(er)

    def __str__(self):
        return self.name,self.points

    def playing(self,card1,card2):
        if self.c.full_cards[card1].value == "J" and self.c.full_cards[card2].value == "J":
            self.points += self.calculate_value(self.c.full_cards[card1].value)
            self.matched_card(card1, card2)
            print(f"Συνολική βαθμολογία: {self.points}")
            print("Παίζεται ξανά")
            if len(self.c.collected_cards) < len(self.c.full_cards):
                self.plays()
        elif self.c.full_cards[card1].value == "Q" and self.c.full_cards[card2].value == "K" or \
                self.c.full_cards[card2].value == "Q" and self.c.full_cards[card1].value == "K":
            card3 = int(int(input("Παρακαλώ τραβήχτε ένα επιπλέον τυχαίο φύλλο: ")) - 1)
            if self.c.full_cards[card3] in self.c.collected_cards:
                print("Είναι ήδη ανοιχτό")
            elif self.c.full_cards[card1].value == self.c.full_cards[card3].value:
                self.points += self.calculate_value(self.c.full_cards[card1].value)
                self.matched_card(card1, card3)
                print(f"Συνολική βαθμολογία: {self.points}")
            elif self.c.full_cards[card2].value == self.c.full_cards[card3].value:
                self.points += self.calculate_value(self.c.full_cards[card3].value)
                self.matched_card(card2, card3)
                print(f"Συνολική βαθμολογία: {self.points}")
            else:
                print("Δυστυχώς Χάσατε την σειρά σας")
                print("Τα φύλλα που έχουν ανοιχτεί χωρίς να έχει γίνει matched είναι :   ")
                self.c.saw(card1, card2, card3)
                self.c.open_cards()

        elif self.c.full_cards[card1].value == "K" and self.c.full_cards[card2].value == "K":
            self.points += self.calculate_value(self.c.full_cards[card1].value)
            self.matched_card(card1, card2)
            print(f"Συνολική βαθμολογία: {self.points}")
        elif self.c.full_cards[card1].value == self.c.full_cards[card2].value:
            self.points += self.calculate_value(self.c.full_cards[card1].value)
            self.matched_card(card1, card2)
            print(f"Συνολική βαθμολογία: {self.points}")
        else:
            self.canvas.itemconfig("current", self.kartes[0].set_face(False))
            self.canvas.itemconfig("current", self.kartes[1].set_face(False))
            print("Δυστυχώς Χάσατε την σειρά σας")
            print("Τα φύλλα που έχουν ανοιχτεί χωρίς να έχει γίνει matched είναι :   ")
            self.c.saw(card1, card2)
        print("Τα ανοιχτά φύλλα είναι:")
        self.c.open_cards()

    def calculate_value(self, card):
        if card.isdigit():
            return int(card)
        elif card == 'A':
            return 1
        else:
            return 10

    def matched_card(self, card1,card2):  # Μέθοδος με την οποία τραβάμε ένα φύλλο και το αποθηκεύουμε στη collected_deck
        if len(self.c.full_cards) != 0:
            c1 = self.c.full_cards[card1]
            self.c.collected_cards.append(c1)
            c2 = self.c.full_cards[card2]
            self.c.collected_cards.append(c2)
            for card in card1,card2:
                if card in self.c.saw_cards:
                    del self.c.saw_cards[card]
            print(c1,c2)
        else:
            print("Cards Empty")


class CardGameApp():

    def __init__(self, root):
        self.root = root
        self.root.title("Παιχνίδι μνήμης vol.1")  # τίτλος Κεντρικού παράθυρου
        self.board_width, self.board_height = 1400, 800  # διαστάσεις καμβά
        self.root.resizable(False, False)  # Μέθοδος με την οποία ορίζουμε τα αυστηρά πλαίσια
        self.c = Cards()# Αντικείμενο Τράπελα
        # Πρώτο πλαίσιο Frame
        self.f = tk.Frame(root)
        self.f.pack(expand=True, fill="both")  # μηχανή γεωμετρίας pack()
        self.top_font = 'Courier 20'
        self._elapsedtime = 0.0
        self.n_players = None
        self.players = []
        self.cards = CardImages()
        self.create_widgets()
        self.kartes = []

    def create_widgets(self):
        # TODO να γίνει ένα widgets που να εμφανίζει σκοπ,ονόματα παιχτών

        # Δεύτερο πλαίσιο Frame το οποίο τοποθετείται στο Πρώτο Frame
        self.f1 = tk.Frame(self.f)  # Δημιουργία ενός αντικειμένου τύπου Frame μέσα στο οποίο θα τοποθετήσουμε τα\
        # γραφικά αντικείμενα όπως είναι τα button
        self.f1.pack(fill="x")  # βασικές παραμέτρους της pack (expand , fill, side)
        self.timestr = tk.StringVar()
        time_display = tk.Label(self.f1, fg="red", bg="black", font="Courier 14", textvariable=self.timestr, width=10)
        self._set_time(self._elapsedtime)# Αντικείμενο που περιέχει κειμενο
        time_display.pack(side="left", fill='x', expand=False, pady=2, padx=2)
        self.button_info = tk.Button(self.f1, text='  [ Πληροφορίες ]  ', font="Courier 10", command=self.info, width=10)
        self.button_info.pack(side='right', fill='x')
        self.mb = tk.Menubutton(self.f1, text="Menu")  # Δημιουργία ενός menu button
        self.mb.pack(side="left", fill="x")
        self.menu = tk.Menu(self.mb)
        self.submenu = tk.Menu(self.menu, tearoff=True)
        self.menu.add_cascade(label="Νέο Παιχνίδι", menu=self.submenu, underline=0)
        self.submenu.add_command(label="Επίπεδο 1", command=self.eazy_level)
        self.submenu.add_command(label="Επίπεδο 2", command=self.medium_level)
        self.submenu.add_command(label="Επίπεδο 3", command=self.hard_level)
        self.menu.add_command(label="Άνοιγμα Παιχνιδιού", command=self.file)
        self.menu.add_command(label="Παύση Παιχνιδιού", command=self.stop_game)
        self.menu.add_command(label="Αποθήκευση Παιχνιδιού")
        self.menu.add_command(label="Τέλος παιχνιδιού", command=self.buttonPushed)
        self.mb.config(menu=self.menu)
        self.f2 = tk.Frame(self.f) # Δημιουργία αντικειμένου Frame πάνω στο οποίο θα τοποθετηθούν τα χαρτιά της\
        # της τράπουλας καθώς επίσης και κάποια άλλα Frame όπου στα οποία θα τοποθετήσουμε τα widgets\
        # Το πρώτο όρισμα μας δείχνει που ανήκει ιεραρχικά ένα αντικείμενο
        self.f2.pack(expand=True, fill="both")
        self.canvas = tk.Canvas(self.f2, width=1400, height=800, bg="darkgreen")# Γραφική κλάση που μας προσφέρει η tkinter
        self.canvas.pack(side="left", fill="both")
        self.canvas.bind('<Button-1>', self.click)
# TODO η κλάση Computer_play  η οποία θα μαθαίνει στον υπολογιστή πως θα παίζει
# TODO τρόπο με τον οποίο θα εμφανίζεται ,σε περίπτωση αποθήκευσης, τρόπο με το οποίο θα ξεκινάει από εκεί που το αποθηκεύσαμε

    def click_face(self, event):#Μέθοδος με την οποία το π
        if self.canvas.find_withtag('current'):
            num = (self.canvas.find_withtag('current'))
            print(num)
            card = GUICard.tableCards[self.c.full_cards[num[0]-1]]
            self.canvas.itemconfig("current",card.set_face(False))

    def stop_game(self):
        self.stop_timer()
        self.run = False

    def _set_time(self, elap):
        minutes = int(elap / 60)
        seconds = int(elap - minutes * 60.0)
        self.timestr.set('%02d:%02d' % (minutes, seconds))
        return '%02d:%02d' % (minutes, seconds)

    def _update_timer(self):
        self._elapsedtime = time.time() - self._start
        self._set_time(self._elapsedtime)
        self._timer = self.root.after(200, self._update_timer)

    def start_timer(self):
        self._elapsedtime = 0.0
        self._start = time.time() - self._elapsedtime
        self._update_timer()

    def stop_timer(self):
        self.root.after_cancel(self._timer)
        self._elapsedtime = time.time() - self._start

    def eazy_level(self):
        self.c.d_level(1)
        self.c.pie()
        self.canvas.delete("all")
        self.ask_numbers()
        self.start_timer()
        k = 0
        count2 = 123 # θέση σε px πάνω στον καμβά όπου αρχίζει να γίνεται ο σχεδιασμός των φύλλων
        for i in range(4):
            count1 = 550
            for j in range(4):
                gui = GUICard(self.c.full_cards[k], self.canvas)
                gui.set_face(False)
                deck = (count1, count2)
                gui.set_position(deck)
                count1 += self.cards.card_width
                k+=1
            count2 += self.cards.card_height
        self.play_game()

    def medium_level(self):
        self.c.d_level(2)
        self.c.pie()
        self.canvas.delete("all")
        self.ask_numbers()
        self.start_timer()
        k = 0
        count2 = 123 # θέση σε px πάνω στον καμβά όπου αρχίζει να γίνεται ο σχεδιασμός των φύλλων
        for i in range(4):
            count1 = 316
            for j in range(10):
                gui = GUICard(self.c.full_cards[k], self.canvas)
                gui.set_face(False)
                deck = (count1, count2)
                gui.set_position(deck)
                count1 += self.cards.card_width
                k+=1
            count2 += self.cards.card_height

    def hard_level(self):
        self.c.d_level(3)
        self.c.pie()
        self.canvas.delete("all")
        self.ask_numbers()
        self.start_timer()
        k = 0
        count2 = 123 # θέση σε px πάνω στον καμβά όπου αρχίζει να γίνεται ο σχεδιασμός των φύλλων
        for i in range(4):
            count1 = 158
            for j in range(13):
                gui = GUICard(self.c.full_cards[k], self.canvas)
                gui.set_face(False)
                deck = (count1, count2)
                gui.set_position(deck)
                count1 += self.cards.card_width
                k+=1
            count2 += self.cards.card_height

    def ask_numbers(self):
        self.n_players = simpledialog.askinteger("Τίτλος", "Παρακαλώ επιλέξτε τον αριθμό των παιχτών")
        if self.n_players == 1:
            for number in range(self.n_players):
                self.players.append(Player(self.c,
                                           parametros=True))  # Δημιουργία λίστας στην οποία προσθέτουμε για στοιχεία αντικείμενα της κλάσης Players
                self.players.append(ComputerPlay(self.c))
        else:
            for number in range(self.n_players):
                self.players.append(Human_Player(self.canvas,self.c,parametros=True,*self.kartes))  # Δημιουργία λίστας στην οποία προσθέτουμε για στοιχεία αντικείμενα της κλάσης Players
        self.show_players()

    def show_players(self): # μας τυπώνει ταξινομημένα τα ονόματα των παιχτών που καταχωρήσαμε
        print('Παίκτες: [', end ='')
        for player in sorted(self.players, key=lambda x: x.name): # Κάνουμε χρήση lambda ώστε η ταξινόμηση να γίνει στο όνομα
            print(player.name, end = ',')
        print(']')

    def click(self, event):
        global card_1,card_2
        if self.canvas.find_withtag('current'):
            num1 = (self.canvas.find_withtag('current'))
            print(num1[0])
            card1 = GUICard.tableCards[self.c.full_cards[num1[0] - 1]]
            self.kartes.append(card1)
            print(card1.value)
            self.canvas.itemconfig("current", card1.set_face(True))
            if num1[0] not in self.c.collected_cards:
                self.c.collected_cards.append(num1[0] - 1)
                if len(self.c.collected_cards) == 2:
                    card_1 = self.c.collected_cards[0]
                    card_2 = self.c.collected_cards[1]
            print(self.kartes,self.c.collected_cards)

    def play_game(self):  # καλεί διαδοχικά τους παίκτες να παίξουν και αποφασίζει ποιος νίκησε
        for p in range(len(self.players)):
            print(50 * '*', '\nΠαίζει ο παίκτης...', self.players[p].name,"\n")
            if self.players[p].name == "PcMaster":
                self.players[p].computer_plays()
            else:
                root.update_idletasks()
                box = messagebox.showinfo("Σειρά του παίχτη", f"Παίζει ο παίχτης:{self.players[p].name}")
                self.players[p].playing(card_1,card_2)
            if p == self.n_players - 1:
                del p
            else:
                print("Game Over")
                self.show_winner()
                self.run = False

    def show_winner(self):# αποφασίζει ποιος είναι ο νικητής
        for player in sorted(self.players, key=lambda x: x.points):
            print(player.name , player.points)

    def info(self):
        message = '''
Το παιχνίδι παίζεται με έναν ή περισσότερους παίκτες και 1 τράπουλα, η οποία αποτελείται από 4 “σειρές” φύλλων 
(κούπα ♥, σπαθί ♣, καρό ♦, μπαστούνι ♠), με το καθένα να περιλαμβάνει τους αριθμούς από το 1 έως το 10 και τις 
φιγούρες: Βαλές (J), Ντάμα(Q), Ρήγας (K). Οι κάρτες απλώνονται στο τραπέζι,  κατά την έναρξη του παιχνιδιού, 
και τοποθετούνται σε διάταξη πίνακα m x n (m γραμμές και n στήλες).  Αρχικά, όλες οι  κάρτες είναι κλειστές, 
δηλαδή έχουν κρυμμένη την όψη που περιέχει τον αριθμό του τραπουλόχαρτου ή τη φιγούρα. Όταν έρθει η σειρά του, 
κάθε παίκτης καλείται να ανοίξει ένα ζεύγος κλειστών καρτών. Αν οι κάρτες που ανοίχθηκαν έχουν το ίδιο σύμβολο 
(Α, 2, ..., 10, J, Q, K), τότε ο παίκτης κερδίζει τους πόντους που αντιστοιχούν στην αξία της κάρτας, οι κάρτες 
μένουν ανοικτές στο τραπέζι, και παίζει ο επόμενος παίκτης. Αν οι επιλεγμένες κάρτες δεν έχουν το ίδιο σύμβολο, 
τότε τοποθετούνται πάλι κλειστές στην ίδια θέση και το παιχνίδι συνεχίζεται με τον επόμενο παίκτη. Το παιχνίδι 
ολοκληρώνεται όταν ανοιχτούν όλες οι κάρτες, οπότε ανακηρύσσεται νικητής ο παίκτης που έχει συγκεντρώσει τους 
περισσότερους πόντους. Οι αξίες των τραπουλόχαρτων έχουν ως εξής: (i) ο Άσσος (Α) έχει αξία 1, (ii) τα φύλλα 2..10 
έχουν αξία ίση με τον αριθμό του φύλλου, (iii) οι φιγούρες J, K, Q έχουν αξία 10.
        '''
        simpledialog.messagebox.showinfo("MATCH CARDS GAME v.1 Οδηγίες ", message)

    def buttonPushed(self):
        answer = messagebox.askyesno('Μύνημα', "Είστε σίγουρος/η ότι θέλετε να φύγετε")
        if answer: self.root.destroy()  # Σβήνει το περιβάλλον διεπαφής

    def file(self):
        name = filedialog.askopenfilename()
        print(name)


root = tk.Tk()  # Δημιουργία αντικειμένου που είναι το βασικό παράθυρο
CardGameApp(root)  # Καλούμε την κλάση CardGameApp με όρισμα την root
root.mainloop()  # με τη μέθοδο mainloop ξεκινάμε έναν βρόχο επεξεργασίας γεγονότων για το αντικείμενο root
# άμα θέλουμε να εισάλουμε ένα αντικείμενο με την κλάση Label(που θα μπει το παράθυρο, κειμενο γραμματοσειρά)
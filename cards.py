import random


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

    def d_level(self): # Μέθοδος που ανάλογα με το επίπεδο δυσκολίας εμφανίζει διαφορετικό αριθμό φύλλων
        while True:
            try:
                level = int(input('Παρακαλώ επιλέξτε επίπεδο:\n1)Εύκολο\n2)Μέτριας Δυσκολίας\n3)Δύσκολο\n---> '))
                if level == 1:
                    self.closed_cards(level,4)
                    break
                elif level == 2:
                    self.closed_cards(level,10)
                    break
                elif level ==3:
                    self.closed_cards(level,13)
                    break
            except ValueError:print()

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

from cards import Cards,Card
import random


class Player():

    count = 0

    def __init__(self,cards,name="",points=0,parametros = False):
        Player.count+=1
        if parametros:
            self.name = input(f"Δώστε το όνομα του παίχτη {Player.count}:")
        self.c = cards
        self.points = points

    def __str__(self):
        return self.name,self.points

    def plays(self):
        print(self.c.char)
        card1 = int(int(input("Παρακαλώ τραβήχτε ένα φύλλο: ")) - 1)
        if self.c.full_cards[card1] in self.c.collected_cards:
            print("Είναι ήδη ανοιχτό")
            self.plays()
        card2 = int(int(input("Παρακαλώ τραβήχτε ένα επιπλέον φύλλο: ")) - 1)
        if self.c.full_cards[card2] in self.c.collected_cards:
            print("Είναι ήδη ανοιχτό")
            self.plays()
        self.playing(card1, card2)

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


class ComputerPlay(Player):

    def __init__(self,cards,name="",points=0,parametros = False):
        super().__init__(cards,name,points,parametros )
        self.name = "PcMaster"

    def computer_plays(self):
        while True:
            a = len(self.c.full_cards)
            l=list(range(a))
            if len(self.c.saw_cards) == 5:
                card1 = random.choice(l)
                card2 = random.choice(l)
                if card1 != card2:
                    card1_value = self.c.saw_cards[card1]
                    card2_value = self.c.saw_cards[card2]
                    if card1_value.value == card2_value.value:
                        self.playing(card1,card2)

            else:
                card1 = random.choice(l)
                card2 = random.choice(l)
                if card1 != card2:
                    card1_value = self.c.full_cards[card1]
                    card2_value = self.c.full_cards[card2]
                    if card1_value and card2_value in self.c.collected_cards:
                        self.computer_plays()
                    else:
                        self.playing(card1,card2)

            print(f"Συνολική βαθμολογία: {self.points}")


class Game:

    def __init__(self):
        print("Παίζουμε Matched Game")
        self.c = Cards()
        self.run = False
        self.n_players = self.number_of_players()
        self.players = []
        if self.n_players == 1:
            for number in range(self.n_players):
                self.players.append(Player(self.c,parametros=True))  # Δημιουργία λίστας στην οποία προσθέτουμε για στοιχεία αντικείμενα της κλάσης Players
                self.players.append(ComputerPlay(self.c))
        else:
            for number in range(self.n_players):
                self.players.append(Player(self.c,parametros=True))  # Δημιουργία λίστας στην οποία προσθέτουμε για στοιχεία αντικείμενα της κλάσης Players
        self.show_players()
        self.c.d_level()
        self.play_game()

    def number_of_players(self):# ζητάει από τον χρήστη τον αριθμό παικτών
        number = ''
        while True: # Ελέγχουμε έαν γίνεται σωστή εισαγωγή δεδομένων από τον χρήστη
            number = input('Παρακαλώ εισάγεται τον αριθμό των παιχτών:')
            if number.isdigit():
                return int(number)

    def show_players(self): # μας τυπώνει ταξινομημένα τα ονόματα των παιχτών που καταχωρήσαμε
        print('Παίκτες: [', end ='')
        for player in sorted(self.players, key=lambda x: x.name): # Κάνουμε χρήση lambda ώστε η ταξινόμηση να γίνει στο όνομα
            print(player.name, end = ',')
        print(']')

    def play_game(self):  # καλεί διαδοχικά τους παίκτες να παίξουν και αποφασίζει ποιος νίκησε
        self.run = True
        while self.run:
            if len(self.c.collected_cards) != len(self.c.full_cards):
                for p in range(len(self.players)):
                        print(50 * '*', '\nΠαίζει ο παίκτης...', self.players[p].name,"\n")
                        if self.players[p].name =="PcMaster":
                            self.players[p].computer_plays()
                        else:
                            self.players[p].plays()
                        if p == self.n_players - 1:
                            del p
            else:
                print("Game Over")
                self.show_winner()
                self.run = False

    def show_winner(self):# αποφασίζει ποιος είναι ο νικητής
        for player in sorted(self.players, key=lambda x: x.points):
            print(player.name , player.points)


if __name__ == "__main__":
    game = Game()

from cards import Cards,Card
import random


class Player():

    count = 0

    def __init__(self,cards,name="",points=0,parametros = False):
        Player.count+=1
        if parametros:
            self.name = input(f"Δώστε το όνομα του παίχτη {Player.count}:")
        self.cards = cards
        self.points = points

    def __str__(self):
        return self.name,self.points

    def plays(self):
        print(self.cards)
        card1 = int(int(input("Παρακαλώ τραβήχτε ένα φύλλο: ")) - 1)
        if self.cards.full_cards[card1] in self.cards.collected_cards:
            print("Είναι ήδη ανοιχτό")
            self.plays()
        card2 = int(int(input("Παρακαλώ τραβήχτε ένα επιπλέον φύλλο: ")) - 1)
        if self.cards.full_cards[card2] in self.cards.collected_cards:
            print("Είναι ήδη ανοιχτό")
            self.plays()
        self.playing(card1, card2)

    def playing(self,card1,card2):
        if self.cards.full_cards[card1].value == "J" and self.cards.full_cards[card2].value == "J":
            self.points += self.calculate_value(self.cards.full_cards[card1].value)
            self.matched_card(card1, card2)
            print(f"Συνολική βαθμολογία: {self.points}")
            print("Παίζεται ξανά")
            if len(self.cards.collected_cards) < len(self.cards.full_cards):
                self.plays()
            else:
                return
        if self.cards.full_cards[card1].value == "Q" and self.cards.full_cards[card2].value == "K" or \
                self.cards.full_cards[card2].value == "Q" and self.cards.full_cards[card1].value == "K":
            card3 = int(int(input("Παρακαλώ τραβήχτε ένα επιπλέον τυχαίο φύλλο: ")) - 1)
            if self.cards.full_cards[card3] in self.cards.collected_cards:
                print("Είναι ήδη ανοιχτό")
            if self.cards.full_cards[card1].value == self.cards.full_cards[card3].value:
                self.points += self.calculate_value(self.cards.full_cards[card1].value)
                self.matched_card(card1, card3)
                print(f"Συνολική βαθμολογία: {self.points}")
                return
            if self.cards.full_cards[card2].value == self.cards.full_cards[card3].value:
                self.points += self.calculate_value(self.cards.full_cards[card3].value)
                self.matched_card(card2, card3)
                print(f"Συνολική βαθμολογία: {self.points}")
                return
        elif self.cards.full_cards[card1].value == "K" and self.cards.full_cards[card2].value == "K":
            self.points += self.calculate_value(self.cards.full_cards[card1].value)
            self.matched_card(card1, card2)
            print(f"Συνολική βαθμολογία: {self.points}")
            return
        elif self.cards.full_cards[card1].value == self.cards.full_cards[card2].value:
            self.points += self.calculate_value(self.cards.full_cards[card1].value)
            self.matched_card(card1, card2)
            print(f"Συνολική βαθμολογία: {self.points}")
            return
        else:
            self.cards.saw(card1, card2)
        print("Δυστυχώς Χάσατε την σειρά σας")
        return

    def calculate_value(self, card):
        if card.isdigit():
            return int(card)
        elif card == 'A':
            return 1
        else:
            return 10

    def matched_card(self, card1,card2):  # Μέθοδος με την οποία τραβάμε ένα φύλλο και το αποθηκεύουμε στη collected_deck
        if len(self.cards.full_cards) != 0:
            c1 = self.cards.full_cards[card1]
            self.cards.collected_cards.append(c1)
            c2 = self.cards.full_cards[card2]
            self.cards.collected_cards.append(c2)
            print(c1,c2)
        else:
            print("Cards Empty")


class ComputerPlay(Player):

    def __init__(self,cards,name="",points=0,parametros = False):
        super().__init__(cards,name,points,parametros )
        self.name = "PcMaster"

    def computer_plays(self):
        while True:
            a = len(self.cards.full_cards)
            l=list(range(a))
            if len(self.cards.saw_cards) == 5:
                card1 = random.choice(l)
                card2 = random.choice(l)
                if card1 != card2:
                    card1_value = self.cards.saw_cards[card1]
                    card2_value = self.cards.saw_cards[card2]
                    if card1_value.value == card2_value.value:
                        self.playing(card1,card2)

            else:
                card1 = random.choice(l)
                card2 = random.choice(l)
                if card1 != card2:
                    card1_value = self.cards.full_cards[card1]
                    card2_value = self.cards.full_cards[card2]
                    if card1_value and card2_value in self.cards.collected_cards:
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

    def show_players(self): # μας τυπώνει τους παίκτες
        print('Παίκτες: [', end ='')
        for player in sorted(self.players, key=lambda x: x.name):
            print(player.name, end = ',')
        print(']')

    def play_game(self):  # καλεί διαδοχικά τους παίκτες να παίξουν και αποφασίζει ποιος νίκησε
        self.run = True
        while self.run:
            if len(self.c.collected_cards)<len(self.c.full_cards):
                for p in range(len(self.players)):
                    print(50 * '*', '\nΠαίζει ο παίκτης...', self.players[p].name)
                    print(p)
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

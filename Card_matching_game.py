import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import cards
import time


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

class CardGameApp():
    ''' Κλάση η οποία κατασκευάζει το βασικό περιβάλλον'''

    def __init__(self, root):
        self.root = root
        self.root.title("Παιχνίδι μνήμης")  # τίτλος Κεντρικού παράθυρου
        self.root.resizable(False, False)  # Μέθοδος με την οποία ορίζουμε τα αυστηρά πλαίσια
        self.board_width, self.board_height = 1400, 800
        # Πρώτο πλαίσιο Frame
        self.c = cards.Cards()
        self.run = False
        self.table = []
        self.top_font = 'Courier 20'
        self._elapsedtime = 0.0
        self.f = tk.Frame(self.root)  # Δημιουργία αντικειμένου Frame πάνω στο οποίο θα τοποθετηθούν τα χαρτιά της\
        # της τράπουλας καθώς επίσης και κάποια άλλα Frame όπου στα οποία θα τοποθετήσουμε τα widgets\
        # Το πρώτο όρισμα μας δείχνει που ανήκει ιεραρχικά ένα αντικείμενο
        self.f.pack(expand=True, fill="both")  # μηχανή γεωμετρίας pack()
        self.cards = CardImages()
        self.create_widgets()

    def create_widgets(self):
        # Δεύτερο πλαίσιο Frame το οποίο τοποθετείται στο Πρώτο Frame
        self.f1 = tk.Frame(self.f)  # Δημιουργία ενός αντικειμένου τύπου Frame μέσα στο οποίο θα τοποθετήσουμε τα\
        # γραφικά αντικείμενα όπως είναι τα button
        self.f1.pack(fill="x")  # βασικές παραμέτρους της pack (expand , fill, side)
        self.timestr = tk.StringVar()
        time_display = tk.Label(self.f1, fg="green", bg="black", font="Courier 14", textvariable=self.timestr, width=10)
        self._set_time(self._elapsedtime)
        time_display.pack(side="left", fill='x', expand=False, pady=2, padx=2)
        self.button_info = tk.Button(self.f1, text='  [ Πληροφορίες ]  ', font="Courier 15", command=self.info, width=10)
        self.button_info.pack(side='right', fill='x')
        self.mb = tk.Menubutton(self.f1, text="Menu")  # Δημιουργία ενός menu button
        self.mb.pack(side="left", fill="x")
        self.menu = tk.Menu(self.mb)
        self.menu.add_command(label="Νέο Παιχνίδι", command=self.start_game)
        self.menu.add_command(label="Άνοιγμα Παιχνιδιού", command=self.file)
        self.menu.add_command(label="Παύση Παιχνιδιού", command=self.stop_game)
        self.menu.add_command(label="Αποθήκευση Παιχνιδιού")
        self.submenu = tk.Menu(self.menu, tearoff=True)
        self.menu.add_cascade(label="Επίπεδο Δυσκολίας", menu=self.submenu, underline=0)
        self.submenu.add_command(label="Επίπεδο 1", command=self.eazy_level)
        self.submenu.add_command(label="Επίπεδο 2", command=self.medium_level)
        self.submenu.add_command(label="Επίπεδο 3", command=self.hard_level)
        self.menu.add_command(label="Τέλος παιχνιδιού", command=self.buttonPushed)
        self.mb.config(menu=self.menu)
        self.f2 = tk.Frame(self.f)
        self.f2.pack(expand=True, fill="both")
        self.canvas = tk.Canvas(self.f2, width=1400, height=800, bg="darkgreen")
        self.canvas.pack(side="left", fill="both")


    def start_game(self):
        self.run = True
        self.canvas.delete("all")
        self.start_timer()

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
        self.canvas.delete("all")
        count2 = 123 # θέση σε px πάνω στον καμβά όπου αρχίζει να γίνεται ο σχεδιασμός των φύλλων
        for symbol in ['♣', '♦','♥','♠' ]:
            count1 = 158
            for i in range(9, 13):
                x, y = (count1, count2)
                self.cards.showimage(self.canvas, x, y, symbol, i)
                count1 += self.cards.card_width
            count2 += self.cards.card_height

    def medium_level(self):
        self.canvas.delete("all")
        count2 = 123
        for symbol in ['♣', '♦','♥','♠' ]:
            count1 = 158
            for i in range(10):
                x, y = (count1, count2)
                self.cards.showimage(self.canvas, x, y, symbol, i)
                count1 += self.cards.card_width
            count2 += self.cards.card_height

    def hard_level(self):
        self.canvas.delete("all")
        count2 = 123
        for symbol in ['♣', '♦','♥','♠' ]:
            count1 = 158
            for i in range(13):
                x, y = (count1, count2)
                self.cards.showimage(self.canvas, x, y, symbol, i)
                count1 += self.cards.card_width
            count2 += self.cards.card_height

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
CardGameApp(root)
root.mainloop()  # με τη μέθοδο mainloop ξεκινάμε έναν βρόχο επεξεργασίας γεγονότων για το αντικείμενο root

# άμα θέλουμε να εισάλουμε ένα αντικείμενο με την κλάση Label(που θα μπει το παράθυρο, κειμενο γραμματοσειρά)
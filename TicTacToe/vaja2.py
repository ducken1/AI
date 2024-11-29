import time         #link v pomoc - https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python/

class Game:
    def __init__(self):
        self.initialize_game()

    def initialize_game(self):
        self.current_state = [['.','.','.'],    #konstruktor za izris tic-tac-toe polja
                              ['.','.','.'],
                              ['.','.','.']]

        self.player_turn = 'X' #igralec X bo vedno zacel prvi

    def draw_board(self):
        for i in range(0, 3):       #izris polja
            for j in range(0, 3):
                print('|{}|'.format(self.current_state[i][j]), end=" ")
            print()
        print()

    def is_valid(self, px, py):                 #funkcija za preveritev legalnosti poteze
        if px < 0 or px > 2 or py < 0 or py > 2:    #ce je poteza izven polja
            return False
        elif self.current_state[px][py] != '.':     #ce je pozicija ze zasedena.. torej ni enaka praznemu polju
            return False    
        else:
            return True

    def is_end(self):           #funkcija da preverimo ali se je igra zakljucila
                                    #VERTIKALNA ZMAGA
        for i in range(0, 3):
            if (self.current_state[0][i] != '.' and         #preverimo kateri simbol je na mestu 0,0 ali 0,1 ali 0,2
                self.current_state[0][i] == self.current_state[1][i] and #nato preverimo ce je isti simbol eno navzdol ter nato ce je isti simbol dve navzdol
                self.current_state[1][i] == self.current_state[2][i]):
                return self.current_state[0][i] #ce je potem vrnemo zacetni simbol - zmagovalca

        for i in range(0, 3):       #HORIZONTALNA ZMAGA
            if (self.current_state[i] == ['X', 'X', 'X']):  #preverimo ce so v kateri vrsti 3 isti simboli
                return 'X'
            elif (self.current_state[i] == ['O', 'O', 'O']):
                return 'O'

                    #LEVA DIAGONALA
        if (self.current_state[0][0] != '.' and         #isti princip kot pri vertikalni.. sprva preverimo ce je kateri simbol na 0,0
            self.current_state[0][0] == self.current_state[1][1] and    #nato ce je isti simbol na 1,1
            self.current_state[0][0] == self.current_state[2][2]):  #in znova ce je isti na 2,2
            return self.current_state[0][0]     #ce je vrnemo zmagovalca

                    #DESNA DIAGONALA
        if (self.current_state[0][2] != '.' and             #isto kot zgoraj le da zacnemo na 0,2 in preverjamo 1,1 ter 2,0
            self.current_state[0][2] == self.current_state[1][1] and
            self.current_state[0][2] == self.current_state[2][0]):
            return self.current_state[0][2]     #vrnemo zmagovalca


        for i in range(0, 3):       #preverimo ce je celotno polje zapolnjeno
            for j in range(0, 3):
                if (self.current_state[i][j] == '.'):   #ce obstaja prazno mesto na polju ne vrnemo nicesar.. igra se nadaljuje
                    return None
                 
        return '.'  #ce pa je celotno polje zapolnjeno pa ni izpolnjen noben od zgornjih pogojev.. je izenaceno

    def max(self, globina): #max nam predstavlja racunalniskega igralca - O
                # -1 pomeni izgubo
                # 0 pomeni izenaceno
                # 1 pomeni zmago

            #sprva nastavimo na -2 ker je izven -1 do 1
        maxv = -2

        px = None
        py = None

        result = self.is_end()

        if result == 'X':   #ce zmaga X (mi) returnamo -1
            return (-1, 0, 0)
        elif result == 'O':     #cce zmaga O (racunalnik) rerturnamo 1
            return (1, 0, 0)
        elif result == '.':     #ce je izenaceno returnamo 0
            return (0, 0, 0)

        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.': #na prvem praznem polju bo racunalnik naredil potezo - O
                # To nam predstavlja eno globino minimax drevesa
                    self.current_state[i][j] = 'O'
                    (m, min_i, min_j) = self.min(globina)
                # Ce je m karkoli izmed -1, 0, 1 oziroma vecje kot -2 nastavimo maxv na m ter mu dodamo koordinate te poteze
                    if m > maxv:
                        maxv = m - globina
                        px = i
                        py = j
                # To polje znova nastavimo na prazno
                    self.current_state[i][j] = '.'

        return (maxv, px, py)   #vrnemo stanje koncane igre ter koordinate poteze

    def max_alpha_beta(self, alpha, beta, globina):
        maxv = -2
        px = None
        py = None

        result = self.is_end()

        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'O'
                    (m, min_i, in_j) = self.min_alpha_beta(alpha, beta, globina)
                    if m > maxv:
                        maxv = m-globina
                        px = i
                        py = j
                    self.current_state[i][j] = '.'  #do sem je vse isto kakor pri max funkciji

                    if maxv >= beta:        #alpha je najboljsa ze poiskana moznost za racunalnik - O
                        return (maxv, px, py)

                    if maxv > alpha:        #beta je najboljsa ze poiskana moznost za nas - X
                        alpha = maxv    

        return (maxv, px, py)

    def min(self, globina): #min nam predstavlja nas - X
                # -1 pomeni zmago
                # 0 pomeni izenaceno
                # 1 pomeni izgubo

        minv = 2

        qx = None
        qy = None

        result = self.is_end()

        if result == 'X':       #isti princip kot pri max
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':     #deluje isto kot max.. le da max isce najoptimalnejse poteze za racunalnika ter min deluje kot pomoc nam da zmanjsa stevilo zmag racunalnika
                    self.current_state[i][j] = 'X'
                    (m, max_i, max_j) = self.max(globina)
                    if m < minv:        #ce je m manjsi kakor minv nastavimo minv na m ter koordinate poteze
                        minv = m + globina
                        qx = i
                        qy = j
                    self.current_state[i][j] = '.'  #to polje znova nastavimo na prazno

        return (minv, qx, qy)   #ter vrnemo najboljse stanje koncane igre ter koordinate poteze 

    def min_alpha_beta(self, alpha, beta, globina):

        minv = 2

        qx = None
        qy = None

        result = self.is_end()

        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'X'
                    (m, max_i, max_j) = self.max_alpha_beta(alpha, beta, globina)
                    if m < minv:
                        minv = m + globina
                        qx = i
                        qy = j
                    self.current_state[i][j] = '.'

                    if minv <= alpha:       #alpha je najboljsa ze poiskana moznost za racunalnik - O
                        return (minv, qx, qy)

                    if minv < beta:         #beta je najboljsa ze poiskana moznost za nas - X
                        beta = minv

        return (minv, qx, qy)

    def play(self, globina):         #funkcija loopa ki omogoca igranje igre proti racunalnika
        while True:             #dokler je true rise tic-tac-toe polje ter preverja ali je konec igre
            self.draw_board()
            self.result = self.is_end()

            if self.result != None:     
                if self.result == 'X':  #zmagamo mi
                    print('Zmagovalec ste vi - X')
                elif self.result == 'O':    #zmaga racunalnik
                    print('Zmagovalec je racunalnik - O')
                elif self.result == '.':
                    print("Izenaceno")

                self.initialize_game()
                return

            #Če ni konec igre in smo na vrsti mi 
            if self.player_turn == 'X':

                while True:

                    (m, qx, qy) = self.min(globina)
                    #print('Recommended move: X = {}, Y = {}'.format(qx, qy))

                    px = int(input('Izberite X koordinato: '))
                    py = int(input('Izberite Y koordinato: '))

                    (qx, qy) = (px, py)

                    if self.is_valid(px, py):   #preverimo validnost nase poteze
                        self.current_state[px][py] = 'X' #ce je nastavimo tam X
                        self.player_turn = 'O' #ter je na vrsti racunalnik
                        break
                    else:
                        print('Zal ta poteza ni dovoljena. Poskusite znova!')

        # drugače je na vrsti racunalnik
            else:
                (m, px, py) = self.max(globina)
                self.current_state[px][py] = 'O'    #na px in py nastavimo O
                self.player_turn = 'X'  #ter smo na vrsti mi
                
    def play_alpha_beta(self, globina):
     while True:
        self.draw_board()
        self.result = self.is_end()

        if self.result != None:
            if self.result == 'X':
                print('Zmagovalec ste vi - X')
            elif self.result == 'O':
                print('Zmagovalec je racunalnik - O')
            elif self.result == '.':
                print("Izenaceno")


            self.initialize_game()
            return

        if self.player_turn == 'X':

            while True:
                (m, qx, qy) = self.min_alpha_beta(-2, 2, globina)
               # print('Recommended move: X = {}, Y = {}'.format(qx, qy))

                px = int(input('Izberite X koordinato: '))
                py = int(input('Izberite Y koordinato: '))

                qx = px
                qy = py

                if self.is_valid(px, py):
                    self.current_state[px][py] = 'X'
                    self.player_turn = 'O'
                    break
                else:
                    print('Zal ta poteza ni dovoljena. Poskusite znova!')

        else:
            (m, px, py) = self.max_alpha_beta(-2, 2, globina)
            self.current_state[px][py] = 'O'
            self.player_turn = 'X'

def main():
        g = Game()
        if (argument == 1): {
            g.play(globina)
        }
        elif (argument == 2): {
            g.play_alpha_beta(globina)
        }
        else:
            print("Izbrali ste napačno vrednost. Poskusite znova 1 ali 2")

if __name__ == "__main__":
        print("1: Algoritem minimax\n")
        print("2: Algoritem minimax z alpha-beta odrezovanjem\n")
        argument = int(input("Izberite zeljen algoritem: "))
        globina = int(input("Izberite zeljeno globino/tezavnost: "))
        main()
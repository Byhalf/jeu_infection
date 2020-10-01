from copy import deepcopy
from random import randint
from abc import ABC, abstractmethod
from math import inf as infinity
import sys
global total_noeud_explorer
total_noeud_explorer = 0

class Moves:
    #type/player/source/destination
    """Une class définissant les coups. Elle s'initialise avec un string,un Player,des coordonnée,des coordonnées.
     Les coordonnées sont une listes de 2 int"""

     #slots pour augmenter la vitesse du code
    __slots__ = ['type_of','player','source','destination']

    def __eq__(self, other): 
        if(not isinstance(other,Moves)):
            return False
        return self.type_of == other.type_of and self.source == other.source and self.destination == other.destination
            

    def __str__(self):
        return "player "+ self.player.type_of_player() +" depart"+str(self.source)+ "destination: "+ str(self.destination) + " "+ (self.type_of)
    def __init__(self,type_of,player,source,destination):
        #string/Player/tuple/tuple
        self.type_of = type_of
        self.player = player
        self.source = source
        self.destination = destination
        


class State: 
    #board[i][j]== 0 |player1| player2
    """La instances de la classe State contiennent les état du jeux.Elle s'initialise avec un player,un player,un int, un int 
    (qui sont 2 int pour la dimension) et un int pour le nombre de coup d'avance pour le joueur1(le joueur blanc)"""

    def __init__(self,player1,player2,width,heigth,coup_avance):
        #player1 = white_player
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.player1_score = 1
        self.player2_score = 1
        self.p1_last_move = None
        self.p2_last_move = None
        self.same_move_counter = 0
        self.coup_avance = coup_avance
        
        #On initialise la grille, avec une valeur de 0 pour les cases vides
        M = width
        N = heigth
        self.board = [[0]*M]
        for _ in range(N-1):
            self.board.append([0]*M) 
        self.board[0][0]= self.player2
        self.board[N-1][M-1]= self.player1


    
    def next_player(self,player):
        """Une méthode permettant de renvoyé l'autre joueur que celui donné en paramètre"""
        if (player == self.player1):
            return self.player2
        else:
            return self.player1

    def show_board(self):
        """Une méthode qui affiche la grille de jeu"""
        #O pour le joueur blanc et X pour le joueur noire
        for i in range(len(self.board)):
            print("")
            for j in range((len(self.board[0]))):
                print("|",end="")
                if(self.board[i][j]==0):
                    print(" ",end="")
                elif(self.board[i][j])==self.player2:
                    print("X",end="")
                elif(self.board[i][j])==self.player1:
                    print("O",end="")

                print("|",end="")
        print("\n")

    def get_score(self, player):
        """Une méthode qui renvoie le score relatif d'un joueur c'est à dire son score - le score du joueur adverse"""
        if player == self.player1:
            player_score = self.player1_score
            next_player_score =self.player2_score
        else:
            player_score = self.player2_score
            next_player_score = self.player1_score
        return player_score - next_player_score
    
#append prend trop de temps, add = list.append
    def get_moves(self,player):
        """Une méthode qui renvoie la liste des coups possible pour un joueur donné"""
        #return list of moves
        board = self.board
        res = []
        add = res.append
        #Pour que les coups d'avances soit prédit par le MinMax
        if(self.coup_avance>0):
         #que player2 car les coups d'avance ne sont jamais pour le joueur2
            if(player == state.player2):
                #comme le string est ce qui est utilisé pour savoir quelle type de coup est efféctué, temps que c'est différent de move_player
                #et de dupplicate, il ne se passera rien avec ce coup.
                add(Moves("rien",None,None,None))
                return res
        for i in range(len(board)):
            for j in range((len(board[0]))): 

                if(board[i][j]==player): 
                    #move_player
                    if(i>1 and board[i-2][j]== 0):
                        add(Moves("move_player",player,(j,i),(j,i-2)))
                    if(i<len(board)-2 and board[i+2][j]== 0):
                        add(Moves("move_player",player,(j,i),(j,i+2)))
                    if(j>1 and board[i][j-2]== 0):
                        add(Moves("move_player",player,(j,i),(j-2,i)))
                    if(j<len(board[0])-2 and board[i][j+2]== 0):
                        add(Moves("move_player",player,(j,i),(j+2,i)))
                    #duplicate
                    if(i>0 and board[i-1][j]== 0):
                        add(Moves("dupplicate",player,(j,i),(j,i-1)))
                    if(i<len(board)-1 and board[i+1][j]== 0):
                        add(Moves("dupplicate",player,(j,i),(j,i+1)))
                    if(j>1 and board[i][j-1]== 0):
                        add(Moves("dupplicate",player,(j,i),(j-1,i)))
                    if(j<len(board[0])-1 and board[i][j+1]== 0):
                        add(Moves("dupplicate",player,(j,i),(j+1,i)))
        return res

 
    def play(self,move):
        """Une méthode qui renvoie un état (instance de State) avec le coup passé en paramètre effectué"""
        player = move.player
        new_state = deepcopy(self)
        board = new_state.board
        next_player = self.next_player(player)
        destination = move.destination
        source = move.source
        #variable permettant de connaitre les nombre de pion de chaque joueur sans avoir à le recalculé
        toAdd = 0
        toSub = 0

        #on applique le coup
        if(move.type_of == "dupplicate"):
            board[destination[1]][destination[0]]=player
            toAdd += 1
            if(destination[1]>0):
                if (board[destination[1]-1][destination[0]]==next_player):
                    board[destination[1]-1][destination[0]] = player
                    toSub -= 1
                    toAdd += 1
            if (destination[0]>0):
                if (board[destination[1]][destination[0]-1]==next_player):
                    board[destination[1]][destination[0]-1]=player
                    toSub -= 1
                    toAdd += 1
            if(destination[1]<len(board)-1):
                if (board[destination[1]+1][destination[0]]==next_player):
                    board[destination[1]+1][destination[0]] = player
                    toSub -= 1
                    toAdd += 1
            if (destination[0]<len(board[0])-1):
                if (board[destination[1]][destination[0]+1]==next_player):
                    board[destination[1]][destination[0]+1]=player
                    toSub -= 1
                    toAdd += 1
        elif(move.type_of == "move_player"):
            board[source[1]][source[0]]= 0
            board[destination[1]][destination[0]] = player
        
        if player == self.player1:
            if move == self.p1_last_move:
                self.same_move_counter += 1
            else:
                self.p1_last_move = move
                self.same_move_counter = 0
            
            new_state.player1_score += toAdd
            new_state.player2_score += toSub
        else:
            if move == self.p2_last_move:
                self.same_move_counter += 1
            else:
                self.p2_last_move = move
                self.same_move_counter = 0
            new_state.player2_score += toAdd
            new_state.player1_score += toSub

        if (new_state.coup_avance>0):
            new_state.coup_avance -= 1
            return new_state
        new_state.current_player = next_player
        return new_state



        
    def is_terminal(self):
        if(self.same_move_counter>7):
            return True
        if (self.player1_score ==0 or self.player2_score == 0):
            return True
        if(len(self.get_moves(self.player1))==0 or len(self.get_moves(self.player2))==0):
            return True
        return False

    def get_winner(self):
        score1 = self.get_score(self.player1)
        score2 = self.get_score(self.player2)
        if(score1>score2):
            return self.player1
        elif(score1<score2):
            return self.player2
        else:
            return "draw"

class Player(ABC):
    noeud_explore1 = 0
    noeud_explore2 = 0

    _counter = 0
    @staticmethod
    def counter_of_noeud(player):
        if player.number == 1:
            Player.noeud_explore1 +=1
        else:
            Player.noeud_explore2 +=1
    @staticmethod
    def get_noeud_explore1():
        return Player.noeud_explore1
    @staticmethod    
    def get_noeud_explore2():
        return Player.noeud_explore2
    @staticmethod
    def reset_noeud():
        Player.noeud_explore1 = 0
        Player.noeud_explore2 = 0
    def __init__(self):
        Player._counter += 1
        self.number = Player._counter
    def __str__(self):
        return "Player"+str(self.number)

    def __eq__(self, other): 
        if(not isinstance(other,Player)):
            return False
        return self.__str__() == other.__str__()



    @abstractmethod
    def choose_move(self):
        pass
    @abstractmethod
    def type_of_player(self):
        pass

class Random_player(Player):
    def __str__(self):
        return super().__str__() +"  "+"random"
    def choose_move(self,state,p):
        moves = state.get_moves(p)
        return moves[randint(0,len(moves)-1)]
    def type_of_player(self):
        return "random"

class MinMax(Player):
    def __str__(self):
        return super().__str__() + "  MinMax"
    def __init__(self, profondeur):
        super().__init__()
        self.profondeur = profondeur
    def type_of_player(self):
        return "MinMax"
    def evaluate(self,state,player):
        if(state.is_terminal()):
            winner = state.get_winner()
            if player == winner:
                return 100
            elif player == None:
                return 0
            else:
                return -100
        else:
            return state.get_score(player)

    def minMax(self,state,player,depth):
        if depth == 0 or state.is_terminal():
            return [self.evaluate(state,player) ,None]
        
        else:
            Player.counter_of_noeud(self)
            global total_noeud_explorer
            total_noeud_explorer += 1
            if state.current_player == player:
                b = -infinity
                for move in state.get_moves(player):
                    new_state = state.play(move)
                    m = self.minMax(new_state,player,depth-1)
                    if b<(m[0]):
                        b = m[0] 
                        best_move = move
            else:
                b = +infinity
                player2 = state.current_player
                for move in state.get_moves(player2):
                    new_state = state.play(move)
                    m = self.minMax(new_state,player,depth-1)
                    if b>m[0]:
                        b = m[0]
                        best_move = move
        return [b,best_move]

    def choose_move(self,state,player):
        move = self.minMax(state,player,self.profondeur)[1]
        return move
            
#a faire
class AlphaBeta(Player):

    def __str__(self):
        return super().__str__()
    def __init__(self,profondeur):
        super().__init__()
        self.profondeur = profondeur

    def type_of_player(self):
        return "alphaBeta"
    def evaluate(self,state,player):
        if(state.is_terminal()):
            winner = state.get_winner()
            if player == winner:
                return 100
            elif player == None:
                return 0
            else:
                return -100
        else:
            return state.get_score(player)

    def alphaBeta(self,state,player,depth,alpha = [-infinity,None],
    beta= [infinity,None]):
        global total_noeud_explorer
        total_noeud_explorer += 1
        Player.counter_of_noeud(self)
        if depth == 0 or state.is_terminal():
            return [self.evaluate(state,player) ,None]
        
        else:
            if state.current_player == player:
                for move in state.get_moves(player):
                    new_state = state.play(move)
                    m = self.alphaBeta(new_state,player,depth-1,alpha,beta)
                    #max
                    if alpha[0] < m[0]:
                        alpha = m
                        alpha[1] = move

                    if alpha[0]>=beta[0]:
                        return alpha
                return alpha
                        
            else:
                player2 = state.current_player
                for move in state.get_moves(player2):
                    new_state = state.play(move)
                    m = self.alphaBeta(new_state,player,depth-1,alpha,beta)
                    #min
                    if beta[0]>m[0]:
                        beta = m
                        beta[1] = alpha[1]

                    if alpha[0]>=beta[0]:
                        return beta
                return beta

    def choose_move(self,state,player):
        move = self.alphaBeta(state,player,self.profondeur)[1]
        return move


#6 paramètre au programme Longueur/Largeur/Coup d'avance Blanc/prof blanc/idem Noire/élagage ou non.

w = int(sys.argv[1])
h = int(sys.argv[2])
coup_avance = int(sys.argv[3])
profondeur_blanc = int(sys.argv[4])
profondeur_noire = int(sys.argv[5])
elagage = int(sys.argv[6])

if elagage == 1:
    elagage = True
else:
    elagage = False

if elagage:
    player1 = AlphaBeta(profondeur_blanc)
    player2 = AlphaBeta(profondeur_noire)
else:
    player1 = MinMax(profondeur_blanc)
    player2 = MinMax(profondeur_noire)

state = State(player1, player2, w, h, coup_avance)
state.show_board()

while(state.is_terminal() != True):
    p = state.current_player
    move = p.choose_move(state, p)
    state = state.play(move)
    state.show_board()

print("winner = ",state.get_winner())
print("score joueur1= ",state.player1_score)
print("score joueur2= ", +state.player2_score)
# print("noeud exploré joueur1 = "+str(player1.noeud_explore))
# print("noeud exploré joueur2 = "+str(player2.noeud_explore))
print(AlphaBeta.get_noeud_explore1())
print(AlphaBeta.get_noeud_explore2())
Player.reset_noeud()


#### pour les graphique #######
import matplotlib.pyplot as plt
x1,y1,x2,y2 = [],[],[],[]
dimX = 3
dimY = 3
for i in range(1,5):
    print(i)
    total_noeud_explorer = 0
    x1.append(i)
    x2.append(i)
    player1 = MinMax(i)
    player2 = MinMax(i)
    Player.reset_noeud()

    state = State(player1,player2,dimX,dimY,0)
    while(state.is_terminal() != True):
        p = state.current_player
        move = p.choose_move(state,p)
        state = state.play(move)
        #state.show_board()
    #y1.append(Player.get_noeud_explore1()+Player.get_noeud_explore2())
    y1.append(total_noeud_explorer)
    total_noeud_explorer = 0
    Player.reset_noeud()
    player1 = AlphaBeta(i)
    player2 = AlphaBeta(i)
    state = State(player1,player2,dimX,dimY,0)
    while(state.is_terminal() != True):
        p = state.current_player
        move = p.choose_move(state,p)
        state = state.play(move)
        #state.show_board()
    #print(Player.get_noeud_explore2())
    #y2.append(Player.get_noeud_explore1()+Player.get_noeud_explore2())
    y2.append(total_noeud_explorer)
    total_noeud_explorer = 0
    Player.reset_noeud()




###########beau graph###############
print(x1,y1)
print(x2,y2)
plt.subplot(3,1,1)
plt.plot(x1,y1)
plt.xlabel("profondeur")
plt.ylabel("Noeuds explorés")
plt.title("MinMax")

plt.subplot(3,1,2)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=1)

plt.plot(x2,y2)
plt.xlabel("profondeur")
plt.ylabel("Noeuds explorés")
plt.title("AlphaBeta")

plt.subplot(3,1,3)
plt.plot(x1,y1,label="MinMax")
plt.plot(x2,y2,label="AlphaBeta")
plt.xlabel("profondeur")
plt.ylabel("Noeuds explorés")
plt.title("AlphaBeta et MinMax")
plt.legend()
plt.suptitle("Jeu de dimension 5*5")
plt.show()


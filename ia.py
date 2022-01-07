NB_PION = 4

class IA:
    count_tour = 0
    def __init__(self):
        self.ia_first = False
        self.mode = "set"
        
    def new_game(self, ia_first: bool):
        self.ia_first = ia_first
    
    def player_sets(self, x, y, u=None,v=None):
        #check cell befor set player in cell 
        self.mode = "set"
        
        print(f'#In player_sets func with mode: {self.mode}')

    def player_moves(self, x1, y1, x2, y2, u=None,v=None):
        #check cell befor move player in cell
        self.mode = "move"
        
        print(f'#In player_moves func with mode: {self.mode}')

    def play(self):
        IA.count_tour +=1
        print(f'#In play func with mode: {self.mode}', ' | #NB_TOUR: ', IA.count_tour)
        
        u, v  = 0, 0
        x, y  = 0, 0
        x1,y1 = 0, 0
        x2,y2 = 0, 0
        
        if self.mode == "set":    # set mode
            ret = "set", (x,y), (u,v)
        elif self.mode == "move": #move mode
            ret = "move", (x1,y1), (x2,y2), (u,v)
        else: raise ValueError(f"{self.mode} unknow mode")
        
        print("mode:", self.mode)
        if IA.count_tour == NB_PION: self.mode = "move"
        
        return ret

#------------------------------------------#
if __name__ == '__main__':
    ia1 = IA()
    ia2 = IA()
    
    ia1.new_game(True)
    ia2.new_game(False)
    
    #ia1.player_sets(ret[0], ret[1])
    #ia1.player_moves(ret[0], ret[1], ret[2], ret[3])
        
    NB_ROUND = 10
    c = 0
    while c < NB_ROUND:
        
        if c%2 == 0:
            ia1.ia_first = True
            ia2.ia_first = False
            print('\n', c, '-'*5, ' ia1 ', '-'*5,)
            ret = ia1.play()
        else:
            ia2.ia_first = True
            ia1.ia_first = False
            print('\n', c, '-'*5, ' ia2 ', '-'*5)
            ret = ia2.play()
        c +=1
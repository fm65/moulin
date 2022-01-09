import random
import damier

NB_PION = 18
field = damier.Damier()

empty_game = ["╔═══════╗",
              "║       ║",
              "║       ║",
              "║       ║",
              "║       ║",
              "║       ║",
              "║       ║",
              "║       ║",
              "╚═══════╝"]




def get_player_symbol(player):
    if player is None:
        return "◯"
    if player.get_color() == "blue":
        return "B"#"①"
    if player.get_color() == "red":
        return "R"#"②"

def print_field(field):
    to_print = empty_game
    for position in damier.Damier.position_list:
        player = field.get_cell(position).get_player()
        tmp_list = list(to_print[position[0]])
        tmp_list[position[1]] = get_player_symbol(player)
        to_print[position[0]] = "".join(tmp_list)
    for line in to_print:
        print(line)
        

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
        
        print("mode:", self.mode)
        if IA.count_tour == NB_PION//2+1: self.mode = "move"

        u, v  = None, None
        
        self.ia_player  = field.get_current_player()
        self.ia_color   = field.get_current_player().get_color()
        
        self.opposed_player  = field.get_not_current_player()
        self.opposed_color   = field.get_not_current_player().get_color()
        
        self.ia_player_empty_positions  = field.get_empty_position_list()
        self.ia_player_filled_positions = field.list_of_position_for_player(self.ia_player)
        
        self.opposed_player_empty_positions  = field.get_empty_position_list()
        self.opposed_player_filled_positions = field.list_of_position_for_player(self.opposed_player)
        
        self.ia_selected_coords = random.choices(self.ia_player_empty_positions)[0]
        self.ia_selected_cell = field.get_cell(self.ia_selected_coords)
        
        if IA.count_tour > 1 and len(field.list_of_empty_linked_cell_for_player(self.ia_player)) > 0:
            self.ia_selected_coords = random.choices(field.list_of_empty_linked_cell_for_player(self.ia_player))[0]
            self.ia_selected_cell = field.get_cell(self.ia_selected_coords)
        
        
        if self.mode == "set": #-----------PHASE 1-------------#
            print("#-----------PHASE 1-------------#")
            
            self.ia_selected_cell.set_player(self.ia_player)

            x, y  = self.ia_selected_coords[0], self.ia_selected_coords[1]

            if field.can_kill(self.ia_selected_cell): #IF MOULIN

                while True:
                    self.opposed_selected_coords = random.choices(self.opposed_player_filled_positions)[0]
                    self.opposed_selected_cell = field.get_cell(self.opposed_selected_coords)
                    
                    if field.can_get_killed(self.opposed_selected_cell):
                        field.kill_cell(self.opposed_selected_cell)
                        break

                u, v  = self.opposed_selected_coords[0], self.opposed_selected_coords[1]
            
            ret = "set", (x,y), (u,v)
            
        elif self.mode == "move": #-----------PHASE 2-------------#
            print("#-----------PHASE 2-------------#")
            count_move_try = 0
            while True:
                self.ia_dest_coords = random.choices(self.ia_player_filled_positions)[0]
                self.ia_dest_coords_cell = field.get_cell(self.ia_dest_coords)
                self.ia_selected_cell = field.get_cell(self.ia_selected_coords)
                
                if field.can_move(self.ia_selected_cell, self.ia_dest_coords_cell):
                    field.move(self.ia_selected_cell, self.ia_dest_coords)
                    break
                
                if count_move_try == 24: break
                count_move_try +=1

            if field.can_kill(self.ia_dest_coords_cell): #IF MOULIN

                while True:
                    if field.can_get_killed(self.opposed_selected_cell):
                        field.kill_cell(self.opposed_selected_cell)
                        break
                    self.opposed_selected_cell = field.get_cell(self.opposed_selected_coords)
                    self.opposed_selected_coords = random.choices(self.opposed_player_filled_positions)[0]

                u, v  = self.opposed_selected_coords[0], self.opposed_selected_coords[1]
                
            x1, y1 = self.ia_selected_coords[0], self.ia_selected_coords[1]
            x2, y2 = self.ia_dest_coords[0], self.ia_dest_coords[1]
            
            ret = "move", (x1,y1), (x2,y2), (u,v)

        else: raise ValueError(f"{self.mode} unknow mode")
        
        field.switch_player()
        
        return ret

#------------------------------------------#
if __name__ == '__main__':
    ia1 = IA()
    ia2 = IA()
    
    ia1.new_game(True)
    ia2.new_game(False)
    
    #ia1.player_sets(ret[0], ret[1])
    #ia1.player_moves(ret[0], ret[1], ret[2], ret[3])
        
    NB_ROUND = 18
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
        print(ret)
        print_field(field)
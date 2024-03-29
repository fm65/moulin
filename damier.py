from player import *
from cell import *
import pickle


class Damier:

    list_of_moulin = [[(1, 1), (1, 4), (1, 7)], [(2, 2), (2, 4), (2, 6)], [(3, 3), (3, 4), (3, 5)],
                      [(4, 1), (4, 2), (4, 3)], [(4, 5), (4, 6), (4, 7)], [(5, 3), (5, 4), (5, 5)],
                      [(6, 2), (6, 4), (6, 6)], [(7, 1), (7, 4), (7, 7)], [(1, 1), (4, 1), (7, 1)],
                      [(2, 2), (4, 2), (6, 2)], [(3, 3), (4, 3), (5, 3)], [(1, 4), (2, 4), (3, 4)],
                      [(5, 4), (6, 4), (7, 4)], [(3, 5), (4, 5), (5, 5)], [(2, 6), (4, 6), (6, 6)],
                      [(1, 7), (4, 7), (7, 7)]]
    
    position_list = [(1, 1), (1, 4), (1, 7),
                        (2, 2), (2, 4), (2, 6),
                        (3, 3), (3, 4), (3, 5),
                        (4, 1), (4, 2), (4, 3),
                        (4, 5), (4, 6), (4, 7),
                        (5, 3), (5, 4), (5, 5),
                        (6, 2), (6, 4), (6, 6),
                        (7, 1), (7, 4), (7, 7)]

    def __init__(self):
        self.cell_list = {}
        for position in Damier.position_list:
            self.cell_list[position] = Cell(position, self)
        self.player1 = Player("blue", self)
        self.player2 = Player("red", self)
        self.player1.set_current(True)
        self.phase1 = True
        self.phase2 = False

    def get_phase(self):
        if self.phase1 is True:
            return self.phase1
        return self.phase2

    def switch_phase(self):
        if self.phase1 is True:
            self.phase1 = False
            self.phase2 = True
        else:
            self.phase1 = True
            self.phase2 = False

    def get_current_player(self):
        return self.player1 if self.player1.is_current else self.player2

    def get_not_current_player(self):
        return self.player1 if self.player2.is_current else self.player2

    def switch_player(self):
        self.player1.toggle_current()
        self.player2.toggle_current()

    def get_empty_position_list(self):
        return list(filter(lambda position: self.get_cell(position).is_empty(), Damier.position_list))

    def list_of_position_for_player(self, player):
        position_list = []
        tab_cell = self.get_cell_list_for_player(player)
        for cell in tab_cell:
            position_list.append(cell.get_position())
        return position_list

    def list_of_empty_linked_cell_for_player(self, player):
        list_of_empty_linked_cell = []
        list_of_linked_cell = []
        for cell in self.get_cell_list_for_player(player):
            list_of_linked_cell.append(cell.get_linked_cells())
        for linked_cells in list_of_linked_cell:
            for linked_cell in linked_cells:
                if self.get_cell(linked_cell).is_empty():
                    list_of_empty_linked_cell.append(linked_cell)
        return list_of_empty_linked_cell

    def set_player_for_cell(self, position):
        cell = self.get_cell(position)
        player = self.get_current_player()
        if not cell.is_empty():
            raise Exception("Cell is not empty")
        cell.set_player(player)

    def get_cell(self, position) -> Cell:
        return self.cell_list[position]

    def set_cell(self, position):
        self.cell_list[position].player = self.get_current_player()

    def get_cell_list_for_player(self, player):
        return list(filter(lambda cell: cell.get_player() == player, self.cell_list.values()))

    def is_in_moulins(self, cell) -> bool:
        for list_of_position_moulin in self.list_of_moulin:
            if not cell.get_position() in list_of_position_moulin:
                continue
            if (self.cell_list[list_of_position_moulin[0]].get_player() == self.cell_list[list_of_position_moulin[1]].get_player()) \
                    and (self.cell_list[list_of_position_moulin[1]].get_player() == self.cell_list[list_of_position_moulin[2]].get_player()):
                return True
        return False

    def has_all_pion_in_moulins(self, player):
        for position in self.position_list:
            if not self.cell_list[position].get_player() == player:
                continue
            if not self.is_in_moulins(self.cell_list[position]):
                return False
        return True

    def move(self, cell: Cell, new_cell: Cell):
        new_cell.set_player(cell.get_player())
        cell.set_player(None)

    def cell_can_move(self, cell):
        if cell.is_movable():
            return True
        else:
            return False

    def can_move(self, cell, new_cell):
        if not new_cell.is_empty():
            return False
        if cell.get_player().count_pion() == 3:
            return True
        if self.are_cells_linked(cell, new_cell):
            return True
        return False

    def are_cells_linked(self, cell, new_cell):
        if new_cell.get_position() in cell.get_linked_cells():
            return True
        return False

    def get_number_of_pion_in_field(self):
        count = 0
        for position in Damier.position_list:
            cell = self.cell_list[position]
            if cell.is_empty():
                continue
            else:
                count += 1
        return count

    def is_finished(self):
        if self.player1.count_pion() == 2 or \
           self.player2.count_pion() == 2 or \
           self.player1.count_movable_pion() == 0 or \
           self.player2.count_movable_pion() == 0:
            return True
        return False

    def can_kill(self, cell):
        if self.is_in_moulins(cell):
            return True
        return False

    def can_get_killed(self, cell):
        if self.has_all_pion_in_moulins(cell.get_player()):
            return True
        if self.is_in_moulins(cell):
            return False
        return True

    def kill_cell(self, cell):
        if self.can_get_killed(cell):
            cell.die()
            return True
        return False

    def save_state(self):
        with open("Sauvegarde_du_moulin", "wb") as f:
            pickle.dump(self, f)

    def reload_state(self):
        with open("Sauvegarde_du_moulin", "rb") as r:
            game = pickle.load(r)
        return game

    def want_to_save(self):
        choice = input("Si vous voulez sauvegarder votre partie entrer o :")
        if choice == "o":
            self.save_state()

    def is_your_turn_to_play(self, color):
        if color == self.get_current_player().color:
            #print("C'est à toi de jouer")
            return True
        #print("Ce n'est pas à toi de jouer")
        return False
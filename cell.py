class Cell:

    list_of_linked_cells = {(1, 1): [(1, 4), (4, 1)], (1, 4): [(1, 1), (1, 7), (2, 4)], (1, 7): [(1, 4), (4, 7)],
                            (2, 2): [(4, 2), (2, 4)], (2, 4): [(1, 4), (2, 2), (2, 6), (3, 4)],
                            (2, 6): [(2, 4), (4, 6)], (3, 3): [(3, 4), (4, 3)], (3, 4): [(3, 3), (2, 4), (3, 5)],
                            (3, 5): [(3, 4), (4, 5)], (4, 1): [(1, 1), (4, 2), (7, 1)],
                            (4, 2): [(4, 1), (2, 2), (4, 3), (6, 2)], (4, 3): [(3, 3), (5, 3)],
                            (4, 5): [(3, 5), (4, 6), (5, 5)], (4, 6): [(4, 5), (2, 6), (4, 7), (6, 6)],
                            (4, 7): [(1, 7), (4, 6), (7, 7)], (5, 3): [(4, 3), (5, 4)],
                            (5, 4): [(5, 3), (5, 5), (6, 4)], (5, 5): [(5, 4), (4, 5)], (6, 2): [(4, 2), (6, 4)],
                            (6, 4): [(6, 2), (5, 4), (6, 6), (7, 4)], (6, 6): [(4, 6), (6, 4)],
                            (7, 1): [(4, 1), (7, 4)], (7, 4): [(7, 1), (6, 4), (7, 7)], (7, 7): [(7, 4), (4, 7)]}

    def __init__(self, position, field):
        self.position = position
        self.field = field
        self.player = None

    def get_position(self):
        return self.position

    def set_player(self, player):
        self.player = player

    def get_player(self):
        return self.player

    def is_empty(self):
        if self.player is None:
            return True
        return False

    def get_linked_cells(self):
        return self.list_of_linked_cells[self.position]

    def is_movable(self):
        if self.is_empty():
            return False
        if self.get_player().count_pion() == 3:
            return True
        linked_cell_list = self.get_linked_cells()
        for linked_cell in linked_cell_list:
            if self.field.get_cell(linked_cell).is_empty():
                return True
        return False

    def die(self):
        self.player = None

    def is_my_player(self, player):
        if player == self.player:
            return True
        else:
            return False


class Player:

    def __init__(self, color, field):
        self.color = color
        self.is_current = False
        self.field = field

    def toggle_current(self):
        self.is_current = not self.is_current

    def get_current(self):
        return self.is_current

    def set_current(self, is_current):
        self.is_current = is_current

    def get_color(self):
        return self.color

    def count_pion(self):
        return len(self.field.get_cell_list_for_player(self))

    def count_movable_pion(self):
        return len(list(filter(lambda cell: cell.is_movable(), self.field.get_cell_list_for_player(self))))

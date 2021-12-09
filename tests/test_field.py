import unittest
from damier import Damier

field = Damier()


class FieldTests(unittest.TestCase):
    def test_field_phase_init(self):
        #  Test si à l'initialisation, ma classe field possède un attribut phase1 égale à True
        self.assertTrue(field.phase1)

    def test_field_switch_phase_when_init(self):
        field.switch_phase()
        #  Test si ma fonction switch_phase() me change la valeur de field phase1 à Faux et phase2 à True à l'initialisation du Field
        self.assertTrue(field.phase2)
        self.assertFalse(field.phase1)

    def test_is_in_moulins_for_every_moulin(self):
        for position in field.cell_list:
            field.cell_list[position].player = field.get_current_player()
        for position in field.cell_list:
            #  Test si avec un terrain rempli avec un seul joueur, la réponse est toujours vrai
            self.assertTrue(field.is_in_moulins(field.cell_list[position]))





if __name__ == '__main__':
    unittest.main()

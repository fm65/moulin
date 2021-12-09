import unittest
from damier import Damier

field = Damier()


class FieldTests(unittest.TestCase):
    def test_field_phase_init(self):
        #  Test si à l'initialisation, ma classe field possède un attribut phase1 égale à True
        self.assertTrue(field.phase1)

    def test_field_switch_phase(self):
        field.switch_phase()
        #  Test si ma fonction switch_phase() met change la valeur de field phase1 à Faux et phase2 à True
        self.assertTrue(field.phase2)
        self.assertFalse(field.phase1)


if __name__ == '__main__':
    unittest.main()

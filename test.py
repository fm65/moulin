import unittest
from damier import Damier


class FieldTests(unittest.TestCase):
    def test_field_phase_init(self):
        field = Damier()
        #  Test si à l'initialisation, ma classe field possède un attribut phase1 égale à True
        self.assertTrue(field.phase1)

    def test_field_switch_phase_when_init(self):
        field = Damier()
        field.switch_phase()
        #  Test si ma fonction switch_phase() me change la valeur de field phase1 à Faux et phase2 à True à l'initialisation du Field
        self.assertTrue(field.phase2)
        self.assertFalse(field.phase1)

    def test_is_in_moulins_for_every_moulin(self):
        field = Damier()
        for position in field.cell_list:
            field.cell_list[position].player = field.get_current_player()
        for position in field.cell_list:
            #  Test si avec un terrain rempli avec un seul joueur, la réponse est toujours vrai  pour vérifier si tout les moulins fonctionnent
            self.assertTrue(field.is_in_moulins(field.cell_list[position]))

    def test_has_all_pion_in_moulins(self):
        field = Damier()
        field.cell_list[(1, 1)].player = field.get_current_player()
        field.cell_list[(1, 4)].player = field.get_current_player()
        field.cell_list[(1, 7)].player = field.get_current_player()
        field.cell_list[(4, 5)].player = field.get_not_current_player()
        field.cell_list[(4, 6)].player = field.get_not_current_player()
        field.cell_list[(7, 7)].player = field.get_not_current_player()
        # Test si la fonctions has_all_pions_in_moulins fonctionne
        self.assertTrue(field.has_all_pion_in_moulins(field.get_current_player()))
        self.assertFalse(field.has_all_pion_in_moulins(field.get_not_current_player()))

    def test_can_kill_normally(self):
        field = Damier()
        field.cell_list[(1, 1)].player = field.get_current_player()
        field.cell_list[(1, 4)].player = field.get_current_player()
        field.cell_list[(1, 7)].player = field.get_current_player()
        field.cell_list[(2, 6)].player = field.get_not_current_player()
        field.cell_list[(4, 5)].player = field.get_not_current_player()
        field.cell_list[(4, 6)].player = field.get_not_current_player()
        field.cell_list[(4, 7)].player = field.get_not_current_player()
        # Test si un kill "classique" fonctionne
        self.assertTrue(field.can_kill(field.cell_list[(1, 1)]))
        # Test si les 2 joueurs ont tout leurs pions dans des moulins
        self.assertTrue(field.has_all_pion_in_moulins(field.get_current_player()))
        self.assertFalse(field.has_all_pion_in_moulins(field.get_not_current_player()))
        # Test si la case 2,6 peut mourir mais par les autres car ils sont dans un moulins
        self.assertTrue(field.can_get_killed(field.cell_list[(2, 6)]))
        self.assertTrue(field.is_in_moulins(field.cell_list[(4, 5)]))
        self.assertFalse(field.can_get_killed(field.cell_list[(4, 5)]))
        self.assertFalse(field.can_get_killed(field.cell_list[(4, 6)]))
        self.assertFalse(field.can_get_killed(field.cell_list[(4, 7)]))

    def test_can_kill_while_enemy_in_moulin(self):
        field = Damier()
        field.cell_list[(1, 1)].player = field.get_current_player()
        field.cell_list[(1, 4)].player = field.get_current_player()
        field.cell_list[(1, 7)].player = field.get_current_player()
        field.cell_list[(4, 5)].player = field.get_not_current_player()
        field.cell_list[(4, 6)].player = field.get_not_current_player()
        field.cell_list[(4, 7)].player = field.get_not_current_player()
        # Test si un kill lorque tout les pions ennemies sont tous dans des moulins fonctionne
        self.assertTrue(field.can_kill(field.cell_list[(1, 1)]))
        # Test si les 2 joueurs ont tout leurs pions dans des moulins
        self.assertTrue(field.has_all_pion_in_moulins(field.get_current_player()))
        self.assertTrue(field.has_all_pion_in_moulins(field.get_not_current_player()))

    def test_winning_because_enemy_cant_move(self):
        field = Damier()
        field.cell_list[(1, 7)].player = field.get_current_player()
        field.cell_list[(4, 7)].player = field.get_current_player()
        field.cell_list[(7, 7)].player = field.get_current_player()
        field.cell_list[(7, 4)].player = field.get_current_player()
        field.cell_list[(1, 4)].player = field.get_not_current_player()
        field.cell_list[(4, 6)].player = field.get_not_current_player()
        field.cell_list[(6, 4)].player = field.get_not_current_player()
        field.cell_list[(7, 1)].player = field.get_not_current_player()
        # Test si la fonction is_finished détecte bien que le joueur ne peut plus bouger
        self.assertTrue(field.is_finished())

    def test_winning_normally(self):
        field = Damier()
        field.cell_list[(1, 7)].player = field.get_current_player()
        field.cell_list[(4, 7)].player = field.get_current_player()
        field.cell_list[(7, 7)].player = field.get_current_player()
        field.cell_list[(7, 4)].player = field.get_current_player()
        field.cell_list[(1, 4)].player = field.get_not_current_player()
        field.cell_list[(4, 6)].player = field.get_not_current_player()
        # Test si la fonction number_of_pion_in_field retourne bien 6 dans ce cas
        self.assertEqual(field.get_number_of_pion_in_field(), 6)
        # Test si la fonction is_finished détecte bien la fin de partie
        self.assertTrue(field.is_finished())

    def test_cant_move_a_pion(self):
        field = Damier()
        field.cell_list[(1, 4)].player = field.get_current_player()
        field.cell_list[(4, 7)].player = field.get_current_player()
        field.cell_list[(1, 1)].player = field.get_current_player()
        field.cell_list[(6, 2)].player = field.get_current_player()
        field.cell_list[(1, 7)].player = field.get_not_current_player()
        field.cell_list[(7, 7)].player = field.get_not_current_player()
        field.cell_list[(7, 1)].player = field.get_not_current_player()
        field.cell_list[(4, 5)].player = field.get_not_current_player()
        # Test si le pion en 1,7 est bien détecte comme étant bloqué lorsque le joueur a plus de 3 pions
        self.assertFalse(field.can_move(field.cell_list[(1, 7)], field.cell_list[(3, 4)]))

    def test_cant_move_a_pion_with_3_pion(self):
        field = Damier()
        field.cell_list[(1, 4)].player = field.get_current_player()
        field.cell_list[(4, 7)].player = field.get_current_player()
        field.cell_list[(1, 1)].player = field.get_current_player()
        field.cell_list[(1, 7)].player = field.get_not_current_player()
        field.cell_list[(7, 7)].player = field.get_not_current_player()
        field.cell_list[(7, 1)].player = field.get_not_current_player()
        # Test si le pion en 1,7 est pas détecté comme bloqué lorsque le joueur a 3 pions
        self.assertTrue(field.can_move(field.cell_list[(1, 7)], field.cell_list[(3, 4)]))


if __name__ == '__main__':
    unittest.main()

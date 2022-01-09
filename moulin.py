import os

from damier import *

from i18n.en import Translation

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
        return "①"
    if player.get_color() == "red":
        return "②"


def print_field(field):
    to_print = empty_game
    for position in Damier.position_list:
        player = field.get_cell(position).get_player()
        tmp_list = list(to_print[position[0]])
        tmp_list[position[1]] = get_player_symbol(player)
        to_print[position[0]] = "".join(tmp_list)
    for line in to_print:
        print(line)


def request_cell_from_field(field: Damier, message: str):
    try:
        input_position_xy = input(message)
        input_position = int(input_position_xy[0]), int(input_position_xy[1])
    except ValueError:
        raise Exception(Translation.get_translation("requestcell.enter.proper.number"))
    except IndexError:
        raise Exception(Translation.get_translation("requestcell.miminim.number"))
    try:
        return field.get_cell(input_position)
    except KeyError:
        raise Exception("Merci de rentrer un combo compris dans cette liste : {}\n".format(field.get_empty_position_list()))


def player_did_moulin(field : Damier):
    print("Bravo ! Le joueur {} a formé un moulin !".format(field.get_current_player().get_color()))
    while True:
        try:
            cell_kill = request_cell_from_field(field,Translation.get_translation("playerdidmoulin.cell.kill"))
        except Exception as ex:
            print(ex)
            continue
        if cell_kill.is_empty():
            print(Translation.get_translation("playerdidmoulin.cell.empty"))
            continue
        if cell_kill.get_player() == field.get_current_player():
            print(Translation.get_translation("playerdidmoulin.cell.yours"))
            continue
        if not field.can_get_killed(cell_kill):
            print(Translation.get_translation("playerdidmoulin.cell.in.moulin"))
            continue
        field.kill_cell(cell_kill)
        break


# CrÉer un plateau done
# Selectionne joueur 1 done
# Boucle tant que plateau.nombre_case.size<18 done
    # Attendre input du joueur done
    # # set player for case(case,player) done
    # vÉrifie la position : vide
    # si position est bonne
        # dÉfinie le joeur dans la case
        # switch_player
        # dÉfinir l'autre joueur comme joueur courant
# Boucle tant que plateau.is_finished
    # Attendre input du joueur pour la case À dÉplacer
    # vÉrifie si la case appartient au joueur et si la case en question est dÉplaÇable
    # Attendre input ud joue pour la destination
    # vÉrifie plateau.ismovable(case,new_case)
    # effectue le move done
    # est-ce que le move autorise le joueur a faire un kill
    # est-ceque l'adversaire a un pion hors moulin
    # si oui :
        # Attendre l'input du joueur pour le pion a faire sauter
        # vÉrifier la case
        # kill
    # changer de joueur

nb_turn = 0
number_of_pion_needed = 18
field = Damier()
if os.path.exists("./Sauvegarde_du_moulin") is True:
    load_save = input(Translation.get_translation("have.a.save"))
    if load_save == "o":
        field = field.reload_state()
while nb_turn != number_of_pion_needed and field.phase1 is True:
    nb_turn += 1
    print_field(field)
    print("C'est au joueur {} de jouer !\n".format(field.get_current_player().color))
    print(field.list_of_position_for_player(field.get_current_player()))
    try:
        chosen_cell = request_cell_from_field(field, Translation.get_translation("put.pion"))
    except Exception as ex:
        print(ex)
        continue
    if not chosen_cell.is_empty():
        print(Translation.get_translation("cell.not.empty"))
        continue
    chosen_cell.set_player(field.get_current_player())
    if nb_turn == number_of_pion_needed:
        field.switch_phase()
    if not field.can_kill(chosen_cell):
        field.switch_player()
        field.want_to_save()
        continue
    player_did_moulin(field)
    field.switch_player()
while not field.is_finished():
    while True:
        print_field(field)
        print("C'est au joueur {} de jouer !".format(field.get_current_player().get_color()))
        try:
            chosen_cell = request_cell_from_field(field, Translation.get_translation("cell.move"))
        except Exception as ex:
            print(ex)
            continue
        if chosen_cell.get_player() != field.get_current_player():
            print(Translation.get_translation("cell.not.your.color"))
            continue
        if not chosen_cell.is_movable():
            print(Translation.get_translation("cell.cant.move"))
            continue
        try:
            chosen_new_cell = request_cell_from_field(field, Translation.get_translation("cell.want.to.move"))
        except Exception as ex:
            print(ex)
            continue
        if not field.can_move(chosen_cell, chosen_new_cell):
            print(Translation.get_translation("cell.filled.or.not.linked"))
            continue
        break
    field.move(chosen_cell, chosen_new_cell)
    if not field.can_kill(chosen_new_cell):
        field.switch_player()
        field.want_to_save()
        continue
    player_did_moulin(field)
    field.want_to_save()

field.switch_player()
print("Félicitation au Joueur {} pour avoir remporté la partie !".format(field.get_current_player().get_color()))


if __name__ == '__main__':
    pass

class Translation:
    data = {
        "requestcell.enter.proper.number": "Merci de rentrer un chiffre entre 1 et 7\n",
        "requestcell.miminim.number": "Il faut rentrer 2 chiffres minimum\n",
        "requestcell.good.combo": "Cette case n'existe pas\n",
        "playerdidmoulin.cell.kill": "Donner la position xy du pion que vous voulez tuer : \n",
        "playerdidmoulin.cell.empty": "La case est vide !\n",
        "playerdidmoulin.cell.yours": "La case est à vous !\n",
        "playerdidmoulin.cell.in.moulin": "La case est immortelle, elle est dans un moulin ! \n",
        "have.a.save": "Une sauvegarde a été trouvé, voulez-vous la chargez ? o/n\n",
        "put.pion": "Donner la position xy où poser votre pion : \n",
        "cell.not.empty": "Tu n'as pas le droit de poser dans une case où il y a déjà un pion\n",
        "cell.move": "Donner la position xy du pion que vous voulez déplacer : \n",
        "cell.not.your.color": "Le pion choisi n'est pas de votre couleur\n",
        "cell.cant.move": "Le pion choisi ne peut pas bouger\n",
        "cell.want.to.move": "Donner la position xy de la case où vous voulez déplacer votre pion : \n",
        "cell.filled.or.not.linked": "La case rempli est soit déjà occupé, soit elle n'est pas contigue avec la première\n"




    }

    @staticmethod
    def get_translation(key: str):
        if key not in Translation.data:
            return "Unknown translation "+key
        return Translation.data[key]

# -*-coding:Utf-8 -*

"""Ce module contient la classe Carte."""

from labyrinthe import Labyrinthe # importation la classe Labyrinthe


class Carte:

    """Objet de transition entre un fichier et un labyrinthe."""

    ########################################################################

    def __init__(self, nom, chaine):
        self.nom = nom
        self.labyrinthe = Labyrinthe(chaine) # On créer un objet Labyrinthe

    def __repr__(self):
        return "<Carte {}>".format(self.nom)

    
    
# -*-coding:Utf-8 -*

"""Ce module contient la classe Carte."""

import pickle

from labyrinthe import Labyrinthe


class Carte:

    """Objet de transition entre un fichier et un labyrinthe."""


    def __init__(self, nom, chaine):
        self.nom = nom
        self.labyrinthe = Labyrinthe("X",chaine)

    def __repr__(self):
        return "<Carte {}>".format(self.nom)

    def sauvegarder(self):
    	"""Methode permettant de sauvegarder une carte dans un pickler"""

    	with open("en_cours","wb") as fichier:

    		mon_pickler = pickle.Pickler(fichier)
    		mon_pickler.dump(self)

    def recuperer_sauvegarde(cls):
    	"""Methode permettant de récupérer une carte dans un pickler"""

    	with open("en_cours","rb") as fichier:

    		mon_depickler = pickle.Unpickler(fichier)
    		return mon_depickler.load()


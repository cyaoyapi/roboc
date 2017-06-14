# -*-coding:Utf-8 -*

"""Ce module contient la classe Carte."""

import pickle

from labyrinthe import Labyrinthe # importation la classe Labyrinthe


class Carte:

    """Objet de transition entre un fichier et un labyrinthe."""

    ########################################################################

    def __init__(self, nom, chaine):
        self.nom = nom
        self.labyrinthe = Labyrinthe(chaine) # On créer un objet Labyrinthe

    def __repr__(self):
        return "<Carte {}>".format(self.nom)

    
    ########################################################################
    
    def sauvegarder(self):

    	"""Methode permettant de sauvegarder un jeu en cours.
    	 
    	 	La sauvegarde est faite ici dans un pickler

    	"""

    	with open("sauvegarde","wb") as fichier:

    		mon_pickler = pickle.Pickler(fichier)
    		mon_pickler.dump(self)


    ########################################################################
    
    def recuperer_sauvegarde(cls):

    	"""Methode de classe permet de récupérer un jeu en cours.

    		La sauvegarde est faite dans un un pickler. On utilise donc
    		un depickler pour la récupération.

    	"""

    	with open("sauvegarde","rb") as fichier:

    		mon_depickler = pickle.Unpickler(fichier)
    		return mon_depickler.load()

    # on indique à python que recuperer_sauvegarde est une méthode de classe
    		
    recuperer_sauvegarde = classmethod(recuperer_sauvegarde)


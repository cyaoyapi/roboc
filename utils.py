#-*- coding:utf-8 -*-

"""Ce module regroupe des fonctions utiles utilisés dans le projet."""

import os  # Module de gestion des fichiers et dossiers
# Module expressions regulières (ici pour tester la validité du choix de déplacement du robot)
import re 
from carte import Carte # importer la classe Carte


###############################################################
# Des constantes

INSTRUCTIONS = """\
Insctructions pour delpacer votre robot X :
===================================================================
    Q : Sauvegarder et quitter la partie en cours ;
    N : Vers le Nord (c'est-à-dire le haut de votre écran) ;
    E : Vers l'Est (c'est-à-dire la droite de votre écran) ;
    S : Vers le Sud (c'est-à-dire le bas de votre écran) ;
    O : Vers l'Ouest (c'est-à-dire la gauche de votre écran) ;
    Chacune des directions ci-dessus suivies d'un nombre permet 
    d'avancer de plusieurs cases (par exemple E3 pour avancer 
    de trois cases vers l'Est).

    Symboles :
    O : Un mur
    . : Une porte
    U : Une sortie
===================================================================
"""


#################################################################
def lister_cartes_existantes(dossier_cartes):

	""" Cette fonction ramène la liste des cartes existantes"""

	cartes = []
	for nom_fichier in os.listdir(dossier_cartes):
		if nom_fichier.endswith(".txt"):
			chemin = os.path.join(dossier_cartes, nom_fichier)
			nom_carte = nom_fichier[:-3].lower()
			with open(chemin, "r") as fichier:
				contenu = fichier.read()
				# Carte et ajout à la liste des cartes
				carte_obj = Carte(nom_carte,contenu)
				cartes.append(carte_obj)

	return cartes  # On retoune la les liste des cartes

#################################################################
def afficher_cartes_existantes(liste_cartes):

	""" Cette fonction affiche la liste des cartes existantes"""

	print("Labyrinthes existants :")
	for i, carte in enumerate(liste_cartes):
		print("  {} - {}".format(i + 1, carte.nom))

#################################################################

def saisir_numero_labyrinthe(liste_cartes):

	""" Cette fonction retourne le numéro de labyrinthe choisi 
		
		Elle contrôle la saisie de l'utilisateur

	"""

	numero_valide = False

	while not numero_valide:
		try:
			numero_labyrinthe = int(input("Entrez un numéro de labyrinthe pour commencer à jouer\n"))
			assert  numero_labyrinthe > 0 and numero_labyrinthe <= len(liste_cartes)
		except ValueError:
			print("Vous devez saisir un nombre entier valide")
		except AssertionError:
			print("Vous devez saisir un numéro de labyrinthe valide")
		else :
			numero_valide = True

	return numero_labyrinthe

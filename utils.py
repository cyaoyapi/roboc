#-*- coding:utf-8 -*-

"""Ce module regroupe des fonctions utiles utilisés dans le projet."""

import os  # Module de gestion des fichiers et dossiers
# Module expressions regulières (ici pour tester la validité du choix de déplacement du robot)
import re 
from carte import Carte # importer la classe Carte


###############################################################
# Des constantes

INSTRUCTIONS = """\
Insctructions du Jeu de labyrinthe multi-joueurs:
==============================================================================
    Q : Sauvegarder et quitter la partie en cours 

    Pour delpacer votre robot X 

    N : Vers le Nord (c'est-à-dire le haut de votre écran) 
    E : Vers l'Est (c'est-à-dire la droite de votre écran) 
    S : Vers le Sud (c'est-à-dire le bas de votre écran) 
    O : Vers l'Ouest (c'est-à-dire la gauche de votre écran) 

    Chacune des 4 précédentes directions ci-dessus suivies d'un 
    nombre permet d'avancer de plusieurs cases (par exemple E3 pour avancer 
    de trois cases vers l'Est).

    M : Permet de murer une porte (transformer une porte en mur)
    P : Permet de trouer un mur (transformer un mur en porte)

    Les 2 précédentes directives ci-dessus doivent être suivies d'une 
    orientation (N,S,E,O) pour indiquer le sens dans lequel se trouve
    la porte à murer ou le mur à trouer.

    Les Symboles 
    
    O : Un mur
    . : Une porte
    U : Une sortie
    X : Robot du Joueur sur son interface (petit (x) pour les autres joueurs)

==============================================================================
"""


#################################################################
def lister_cartes_existantes(dossier_cartes):

	""" Cette fonction ramène la liste des cartes existantes"""

	cartes = []
	for nom_fichier in os.listdir(dossier_cartes):
		if nom_fichier.endswith(".txt"):
			chemin = os.path.join(dossier_cartes, nom_fichier)
			nom_carte = nom_fichier[:-4].lower()
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
			print("Vous devez saisir un numéro de labyrinthe valide (O < numero <= {})".format(len(liste_cartes)))
		else :
			numero_valide = True

	return numero_labyrinthe



#################################################################

def determiner_nouvelle_position(sens,pas,x,y):

    """ Cette fonction permet de déterminer les coordonnée de la nouvelle position envisagéé par le joeur.
            
        - sens : le sens du déplacement
        - pas : le pas 

        Elle est utilisée dans la méthode 'deplacer_robot'

    """

    x_new = x
    y_new = y

    if sens in ["N","S"]:
    # On détermine les coordonnées de la position ou le joueur souhaite se deplacer
        if sens == "N" :
            x_new = x - pas
        else:
            x_new = x + pas

    else:

        # On détermine les coordonnées de la position ou le joueur souhaite se deplacer

        if sens == "O" :
            y_new = y - pas
        else:
            y_new = y + pas


    return x_new, y_new



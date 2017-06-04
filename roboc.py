# -*-coding:Utf-8 -*

"""Ce fichier contient le code principal du jeu.

Exécutez-le avec Python pour lancer le jeu.

"""

import os
import sys
import re

from carte import Carte

# On charge les cartes existantes
cartes = []
for nom_fichier in os.listdir("cartes"):
    if nom_fichier.endswith(".txt"):
        chemin = os.path.join("cartes", nom_fichier)
        nom_carte = nom_fichier[:-3].lower()
        with open(chemin, "r") as fichier:
            contenu = fichier.read()
            # Création d'une carte, à compléter
            carte_obj = Carte(nom_carte,contenu)
            cartes.append(carte_obj)

# On affiche les cartes existantes
print("Labyrinthes existants :")
for i, carte in enumerate(cartes):
    print("  {} - {}".format(i + 1, carte.nom))

# Si il y a une partie sauvegardée, on l'affiche, à compléter
if os.path.exists("en_cours") :
	cartes.append(Carte.recuperer_sauvegarde(Carte))
	print("  {} - {}".format(len(cartes), cartes[len(cartes) - 1].nom+"(En cours)"))


# ... Complétez le programme ...
numero_labyrinthe = int(input("Entrez un numéro de labyrinthe pour commencer à jour\n"))


carte_choisie = cartes[numero_labyrinthe - 1]

# Sauvegarder la carte avant de commencer à jouer
controles = """\
Insctructions pour delpacer votre robot X :
===================================================================
    Q : Sauvegarder et quitter la partie en cours ;
    N : Vers le Nord (c'est-à-dire le haut de votre écran) ;
    E : Vers l'Est (c'est-à-dire la droite de votre écran) ;
    S : Vers le Sud (c'est-à-dire le bas de votre écran) ;
    O : Vers l'Ouest q(c'est-à-dire la gauche de votre écran) ;
    Chacune des directions ci-dessus suivies d'un nombre permet 
    d'avancer de plusieurs cases (par exemple E3 pour avancer 
    de trois cases vers l'est).
===================================================================
"""
print(controles)

fin = False
message = ""

while not fin:
	carte_choisie.sauvegarder()
	carte_choisie.labyrinthe.afficher()
	regex = r"^[QNESO]([1-9][0-9]*)*$"
	choix_valide = False
	while not choix_valide:
		choix = input("Deplacez votre robot (X) \n")
		if re.match(regex, choix) is not None:
			choix_valide = True
		else :
			message = "Choix de déplacement non valide. reprenez !"
			print(message)
			print(controles)
	if choix == "Q":
		carte_choisie.sauvegarder()
		fin = True
		message = "Vous quittez le jeu. Aurevoir et à bientôt"
	else:
		fin, message = carte_choisie.labyrinthe.deplacer_robot(choix)
		if not fin:
			print(message)
			


print(message)
os.remove("en_cours")
sys.exit(0)

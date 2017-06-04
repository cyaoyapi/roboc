# -*-coding:Utf-8 -*

"""Ce fichier contient le code principal du jeu.

Exécutez-le avec Python pour lancer le jeu.

"""

import os
import sys

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


# ... Complétez le programme ...
numero_labyrinthe = int(input("Entrez un numéro de labyrinthe pour commencer à jour\n"))


carte_choisie = cartes[numero_labyrinthe - 1]

# Sauvegarder la carte avant de commencer à jouer
fin = False
message = ""

while not fin:
	carte_choisie.labyrinthe.afficher()
	choix = input("Deplacez votre robot\n")
	fin, message = carte_choisie.labyrinthe.deplacer_robot(choix)

	if not fin:
		print(message)

print(message)
sys.exit(0)

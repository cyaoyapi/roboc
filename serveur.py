#-*- coding:utf-8 -*-

############################################################
#########  Code de l'application Serveur ###################
############################################################

"""ce fichier contient le code principal de l'application serveur du jeu.

	Exécutez-le avec python( version 3) pour demarrer le jeu.

"""

import os  # Module de gestion des fichiers et dossiers
import sys # Module pour interragir avec le système
# Module expressions regulières (ici pour tester la validité du choix de déplacement du robot)
import re 

from carte import Carte # importer la classe Carte

# Chargement des cartes existantes
cartes = []
for nom_fichier in os.listdir("cartes"):
    if nom_fichier.endswith(".txt"):
        chemin = os.path.join("cartes", nom_fichier)
        nom_carte = nom_fichier[:-3].lower()
        with open(chemin, "r") as fichier:
            contenu = fichier.read()
            # Carte et ajout à la liste des cartes
            carte_obj = Carte(nom_carte,contenu)
            cartes.append(carte_obj)

# On affiche les cartes existantes
print("Labyrinthes existants :")
for i, carte in enumerate(cartes):
    print("  {} - {}".format(i + 1, carte.nom))


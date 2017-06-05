# -*-coding:Utf-8 -*

"""Ce fichier contient le code principal du jeu.

Exécutez-le avec Python pour lancer le jeu.

"""

import os  # Module de gestion de dossiers et fichiers
import sys # Module pour interagir avec le système
# Module Expressions regulières(Ici pour tester la validité du choix de déplacement du robot)
import re 

from carte import Carte # On importe la classe carte

# On charge les cartes existantes
cartes = []
for nom_fichier in os.listdir("cartes"):
    if nom_fichier.endswith(".txt"):
        chemin = os.path.join("cartes", nom_fichier)
        nom_carte = nom_fichier[:-3].lower()
        with open(chemin, "r") as fichier:
            contenu = fichier.read()
            # Création d'une carte et ajout à liste des cartes
            carte_obj = Carte(nom_carte,contenu)
            cartes.append(carte_obj)

# On affiche les cartes existantes
print("Labyrinthes existants :")
for i, carte in enumerate(cartes):
    print("  {} - {}".format(i + 1, carte.nom))

# Si il y a une partie sauvegardée (si un fichier encours existe), on l'affiche 
if os.path.exists("encours") :
	cartes.append(Carte.recuperer_sauvegarde())
	index_encours = len(cartes) -1
	numero_encours = len(cartes)
	print("  {} - {}".format(numero_encours, cartes[index_encours].nom+"(En cours)"))


# Récupérer le choix du numéro du labyrinthe saisi par l'utilisateur (Controle de la saisie)
numero_valide = False
while not numero_valide:
	try:
		numero_labyrinthe = int(input("Entrez un numéro de labyrinthe pour commencer à jour\n"))
		assert  numero_labyrinthe > 0 and numero_labyrinthe <= len(cartes)
	except ValueError:
		print("Vous devez saisir un nombre entier valide")
	except AssertionError:
		print("Vous devez saisir un numéro de labyrinthe valide")
	else :
		numero_valide = True

# La saisie est bonne on récupère le labyrinthe(carte) choisi 
carte_choisie = cartes[numero_labyrinthe - 1]

# Instructions de déplacement du robot
controles = """\
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

print(controles) # On affiche les instructions de déplacement du robot

fin = False
message = ""

#On entre dans une boucle, tant que fin n'est pas True
while not fin:
	carte_choisie.sauvegarder() # A chaque tour on sauvegarde la carte telle qu'elle se présente actuellement
	carte_choisie.labyrinthe.afficher() # On l'affiche le labyrinthe
	regex = r"^[NESO]([1-9][0-9]*)*$" # Motif de choix valide de déplacement du robot
	choix_valide = False
	# Tant que le choix n'est pas valide
	while not choix_valide:
		choix = input("Deplacez votre robot (X) \n")
		if re.match(regex, choix) is not None or choix == "Q":
			choix_valide = True
		else :
			message = "Choix de déplacement non valide. reprenez !"
			print(message)
			print(controles)
			carte_choisie.labyrinthe.afficher()
	# Si le choix est de quitter l'application
	if choix == "Q":
		carte_choisie.sauvegarder() # On sauvegarde le jeu en cours
		fin = True
		message = "Vous quittez le jeu. Aurevoir et à bientôt"

	# Si le choix de déplacement est valide
	else:
		fin, message = carte_choisie.labyrinthe.deplacer_robot(choix)
		if not fin:
			print(message)
			

# Lorsque fin est à True, on sort de la boucle

print(message) # On affiche le message de fin

# Si on n'est pas dans le cas où l'utilisateur veut quitter l'application
# Le jeu est donc terminé : L'utilisateur a par exemple perdu suite à une collision
if choix != "Q":
	os.remove("encours") # On supprime le fichier en cours (il n'y pas de jeu en cours)
sys.exit(0) # On sort de l'interpretateur python (On arrête le programme)

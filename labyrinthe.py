# -*-coding:Utf-8 -*

import random

"""Ce module contient la classe Labyrinthe."""
from obstacle.vide import Vide
from obstacle.mur import Mur
from obstacle.porte import Porte
from obstacle.sortie import Sortie
from joueur import Joueur

class Labyrinthe:

    """Classe représentant un labyrinthe."""


    # Définition d'une constante de classe pour la gestion des messages utilisateurs

    MSG = {
        "H":"Désolé ! Vous êtes hors de la zone du labyrithe : vous avez perdu !\n",
        "C":"Désolé ! Collision avec un mur : Vous avez perdu !\n",
        "B": "Bravo ! Vous avancez bien  : Continuez !\n",
        "F": "Félicitations ! Vous avez gagné !\n"

    }

    #################################################

    def __init__(self, contenu):

    	""" Constructeur d'un labyrinthe."""

    	contenu = contenu.split("\n") # transforme le contenu(chaine) en liste

    	self.joueurs = []  # La liste des joueurs de ce labyrinthe

    	# dictionnaire de symboles d'obstacles

    	symboles = {
    		" ": Vide,
    		"O": Mur,
    		".": Porte,
    		"U": Sortie,
    		"X": Joueur
    	}
    	
    	i = 0
    	self.grille = []  # la grille du la byrinthe : une liste de listes ([[],[],[]...[]])
    	
    	for ligne in contenu:
    		
    		j = 0
    		liste_ligne = [] # d'une chaine (ligne), on aura une liste d'objets(filles) obstacles
    		
    		for caractere in ligne:
    			classe_obstacle = symboles[caractere.upper()] # On recupère la classe de l'obstacle en fonction du caracrtère
    			obstacle = classe_obstacle(i,j) # on créer l'objet(fille) obstacle
    			liste_ligne.append(obstacle) # on l'ajoute à la liste(ligne)
    			j += 1 # On passe au caractère suivant

    		self.grille.append(liste_ligne) # On joute la nouvelle ligne à la grille
    		i += 1 # On passe à la ligne suivante



    #################################################

    def generer_contenu(self, joueur_encours):

    	"""Méthode permet de générer le contenu du labyrinthe sous forme de chaine de caractères"""


    	contenu = ""
    	for liste_ligne in self.grille:

    		j = 0
    		ligne =[]
    		for obstacle in liste_ligne:
    			if (obstacle in self.joueurs) and (obstacle is not joueur_encours):
    				ligne.append(obstacle.symbole.lower())
    			else:
    				ligne.append(obstacle.symbole)
    			j += 1
    			if j == len(liste_ligne):
    				ligne.append("\n")
    				break

    		ligne = ("").join(ligne) # On reconstruire la chaine à afficher à partir de la liste
    		contenu += ligne

    	return contenu


    #################################################

    def generer_postion_libre(self):

    	"""Méthode permet de générer une position aléatoire libre pour un nouveau joueur"""

    	i = 0
    	liste_vides = [] # Liste des espaces vides (Une liste de tuple(x,y))
    	
    	for liste_ligne in self.grille:
    		
    		j = 0
    		for obstacle in liste_ligne:
    			if obstacle.symbole == " ":
    				couple = (i,j)
    				liste_vides.append(couple)
    			j += 1
    		i += 1

    	vide_choisi = random.choice(liste_vides)

    	return vide_choisi[0], vide_choisi[1] 



   
    	
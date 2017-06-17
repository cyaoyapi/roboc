#-*- coding:utf-8 -*-

"""Module de tests unitaires pour le jeu de labyrinthe"""

import random ## Module pour faire du pseudo aléatoire
import re # Module pour la gestion des expressions regulières
import unittest
import socket

from obstacle.obstacle import Obstacle
from obstacle.mur import Mur
from obstacle.mur import Mur
from obstacle.porte import Porte
from obstacle.sortie import Sortie
from obstacle.vide import Vide
from joueur import Joueur
import utils
from labyrinthe import Labyrinthe
from carte import Carte



###################### Classe de test pour le module utils #########################################################

class UtilsTest(unittest.TestCase):

	""" Teste les fonctions du module 'utils' """

	#################################################

	def test_lister_cartes_existantes(self):

		""" Teste la fonction 'lister_cartes_existantes' """

		# Construction manuelle d'une liste de 3 cartes situées dans le dossier 'cartes'

		liste_cartes = []
		liste_noms = []

		nom1 = "facile"
		liste_noms.append(nom1)
		fichier1 = open("cartes/facile.txt","r")
		contenu1 = fichier1.read()
		fichier1.close()
		fichier.close()
		carte1 = Carte(nom1,contenu1)
		liste_cartes.append(carte1)

		nom2 = "difficile"
		liste_noms.append(nom2)
		fichier2 = open("cartes/difficile.txt","r")
		contenu2 = fichier2.read()
		fichier2.close()
		carte2 = Carte(nom2,contenu2)
		liste_cartes.append(carte2)

		nom3 = "prison"
		liste_noms.append(nom3)
		fichier3 = open("cartes/prison.txt","r")
		fichier3.close()
		contenu3 = fichier3.read()
		carte3 = Carte(nom3,contenu3)
		liste_cartes.append(carte3)

		# Construction automatique de la liste avec la fonction à tester
		liste_obtenue = utils.lister_cartes_existantes("cartes")

		# Tester si les deux listes(ici les noms) sont les mêmes
		for carte in liste_obtenue:
			self.assertIn(carte.nom,liste_noms)


	#################################################
	
	def test_saisir_numero_labyrinthe(self):

		""" Teste la fonction 'saisir_numero_labyrinthe' 

			Cette fonction fait le controle sur la saisie lors
			du choix du numéro de labyrinthe à lancer au démarrage du jeu.

		"""

		# Construction manuelle d'une liste de 3 cartes situées dans le dossier 'cartes'

		liste_cartes = []

		nom1 = "facile"
		fichier1 = open("cartes/facile.txt","r")
		contenu1 = fichier1.read()
		fichier1.close()
		carte1 = Carte(nom1,contenu1)
		liste_cartes.append(carte1)

		nom2 = "difficile"
		fichier2 = open("cartes/difficile.txt","r")
		contenu2 = fichier2.read()
		fichier2.close()
		carte2 = Carte(nom2,contenu2)
		liste_cartes.append(carte2)

		nom3 = "prison"
		fichier3 = open("cartes/prison.txt","r")
		contenu3 = fichier3.read()
		fichier3.close()
		carte3 = Carte(nom3,contenu3)
		liste_cartes.append(carte3)
		fichier3.close()

		liste_numeros = [1,2,3]

		# on recueille la saisie du numéro via la fonction à tester
		numero_obtenu = utils.saisir_numero_labyrinthe(liste_cartes)

		# Ce numéro est t-il valide ?
		self.assertIn(numero_obtenu, liste_numeros)


	#################################################
	
	def test_determiner_nouvelle_position(self):

		""" Teste la fonction 'test_determiner_nouvelle_position' 
			Cette fonctionne détermine les coordonnées de la nouvelle
			position où un joueur désire se rendre lors d'un déplacement
		"""

		# On genère des coordonnées actuelles, le sens, le pas aléatoirement

		x = random.randint(0,20)
		y = random.randint(0,20)
		sens = random.choice(['N', 'S', 'O', 'E'])
		pas = random.randint(1,50)

		# On détermine les coordonnées nouvelles manuellement
		if sens in ["N","S"]:
			if sens == "N":
				x_new = x - pas
			else:
				x_new = x + pas
			y_new = y
		else:
			x_new = x
			if sens == "O" :
				y_new = y - pas
			else:
				y_new = y + pas
		# On détermine les coordonnées avec la fonction à tester
		x_new_obtenu, y_new_obtenu = utils.determiner_nouvelle_position(sens,pas,x,y)
		#Les deux couples de coordonnées sont-ils égales ?
		self.assertEqual((x_new,y_new),(x_new_obtenu,y_new_obtenu))






###################### Classe de test pour la classe Labyrinthe #########################################################

class LabyrintheTest(unittest.TestCase):

	""" Teste les fonctionnalités du Labyrinthe """

	#################################################

	def test_Labyrinthe(self):

		""" Teste la création d'un labyrinthe via la création d'une carte """
		
		# On créer manuellement une carte et un labyrinthe manuellement
		nom_fichier = random.choice(["facile","prison","difficile"])
		path_fichier = "cartes/"+nom_fichier+".txt"
		fichier = open(path_fichier,"r")
		contenu = fichier.read()
		fichier.close()
		contenu_liste = contenu.split("\n")

		symboles = {
    		" ": Vide,
    		"O": Mur,
    		".": Porte,
    		"U": Sortie,
    		"X": Joueur,
    	}

		i = 0
		grille = []
		for ligne in contenu_liste:
			j = 0
			liste_ligne = []
			for caractere in ligne:
				classe_obstacle = symboles[caractere.upper()]
				obstacle = classe_obstacle(i,j)
				liste_ligne.append(obstacle)
				j += 1 
			grille.append(liste_ligne)
			i += 1 
		
		# On crée une carte(indirectemebt un labyrinthe) via le constructeur
		# de la classe Carte(indirectement de la classe Labyrinthe) 
		carte_obtenue = Carte(nom_fichier,contenu)

		# On teste si le résultat est idententique à la création manuelle
		self.assertEqual(carte_obtenue.nom,nom_fichier)
		self.assertEqual(len(carte_obtenue.labyrinthe.joueurs), 0)
		self.assertIsInstance(carte_obtenue, Carte) 
		self.assertIsInstance(carte_obtenue.labyrinthe, Labyrinthe)

		i = 0
		for ligne in carte_obtenue.labyrinthe.grille:
			j = 0
			for obstacle in ligne:
				self.assertIsInstance(obstacle, Obstacle)
				self.assertEqual(obstacle.nom,grille[i][j].nom)
				self.assertIs(obstacle.peut_traverser,grille[i][j].peut_traverser)
				self.assertEqual(obstacle.symbole,grille[i][j].symbole)
				self.assertEqual((obstacle.x,obstacle.y),(grille[i][j].x,grille[i][j].y))
				if j == len(ligne) -1:
					break 
				j += 1
				
			if i == len(carte_obtenue.labyrinthe.grille) -1:
				break		
			i += 1
			


	#################################################

	def test_generer_postion_libre(self):

		""" Teste la fonction 'generer_postion_libre' 
			Cette méthode de la classe Labyrinthe génère aléatoirement
			une positive libre qu'on peut attribuer à un joueur qui se
			connecte pour participer au jeu. 

		"""
		
		# On réalise l'opération manuelle sur une carte
		nom_fichier = random.choice(["facile","prison","difficile"])
		path_fichier = "cartes/"+nom_fichier+".txt"
		fichier = open(path_fichier,"r")
		contenu = fichier.read()
		fichier.close()
		contenu_liste = contenu.split("\n")

		i = 0
		liste_vides = []
		for ligne in contenu_liste:
			j = 0
			liste_ligne = []
			for caractere in ligne:
				if caractere == " ":
					liste_vides.append((i,j))
				j += 1 
			i += 1 

		# On réalise l'opération via la méthode à tester
		carte_obtenue = Carte(nom_fichier,contenu)
		position_libre_obtenu = carte_obtenue.labyrinthe.generer_postion_libre()
		#la position obtenue est t-elle dans la liste des positions
		#libres manuellement trouvées ?
		self.assertIn(position_libre_obtenu,liste_vides)



	#################################################

	def test_generer_contenu(self):

		""" Teste la fonction 'generer_contenu' 
			
			Cette méthode de la classe Labyrinthe permet de
			générer un affichage personnaliser du Labyrinthe
			sur l'interface d'un joueur :
			- Son robot apparait en grand X
			- les autres robots en petit x

		"""
		
		# On réalise l'opération manuelle sur une carte
		nom_fichier = random.choice(["facile","prison","difficile"])
		path_fichier = "cartes/"+nom_fichier+".txt"
		fichier = open(path_fichier,"r")
		contenu = fichier.read()
		fichier.close()
		carte_obtenue = Carte(nom_fichier,contenu)

		x1,y1 = carte_obtenue.labyrinthe.generer_postion_libre()
		socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ip1 = 'localhost'
		port1 = 12345
		joueur1 = Joueur(x1,y1,ip1,port1,socket1)
		carte_obtenue.labyrinthe.grille[x1][y1] = joueur1
		carte_obtenue.labyrinthe.joueurs.append(joueur1)

		x2,y2 = carte_obtenue.labyrinthe.generer_postion_libre()
		socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ip2 = 'localhost'
		port2 = 12348
		joueur2 = Joueur(x2,y2,ip2,port2,socket2)
		socket1.close()
		socket2.close()
		carte_obtenue.labyrinthe.grille[x2][y2] = joueur2
		carte_obtenue.labyrinthe.joueurs.append(joueur2)

		contenu_genere_pour_joueur1 = "" 
		for liste_ligne in carte_obtenue.labyrinthe.grille:
			j = 0
			ligne =[]
			for obstacle in liste_ligne:
				if (obstacle in carte_obtenue.labyrinthe.joueurs) and (obstacle is not joueur1):
					ligne.append(obstacle.symbole.lower())
				else:
					ligne.append(obstacle.symbole)
				j += 1
				if j == len(liste_ligne):
					ligne.append("\n")
					break

			ligne = ("").join(ligne) # On reconstruire la chaine à afficher à partir de la liste
			contenu_genere_pour_joueur1 += ligne

    	# On réalise l'opération via la méthode à tester
		contenu_genenre_obtenu = carte_obtenue.labyrinthe.generer_contenu(joueur1)
		# On test si les deux contenu obtenu sont idententiques
		self.assertEqual(contenu_genenre_obtenu,contenu_genere_pour_joueur1)



	#################################################

	def test_deplacer_robot(self):

		""" Teste la fonction 'deplacer_robot' 

			Cette méthode ramène deux variables si tout se passe bien

			- fin ( un booléen)
			- msg_a_envoyer (une chaine de caractères) présent dans
			  dans un dictionnaire de messages utilisateurs.
			  Ce dictionnaire(MSG)est une constante de la classe Labyrinthe 

		"""
		

		nom_fichier = random.choice(["facile","prison","difficile"])
		path_fichier = "cartes/"+nom_fichier+".txt"
		fichier = open(path_fichier,"r")
		contenu = fichier.read()
		fichier.close()
		carte_obtenue = Carte(nom_fichier,contenu)

		x1,y1 = carte_obtenue.labyrinthe.generer_postion_libre()
		socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ip1 = 'localhost'
		port1 = 12345
		joueur1 = Joueur(x1,y1,ip1,port1,socket1)
		carte_obtenue.labyrinthe.grille[x1][y1] = joueur1
		carte_obtenue.labyrinthe.joueurs.append(joueur1)

		x2,y2 = carte_obtenue.labyrinthe.generer_postion_libre()
		socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ip2 = 'localhost'
		port2 = 12348
		joueur2 = Joueur(x2,y2,ip2,port2,socket2)
		carte_obtenue.labyrinthe.grille[x2][y2] = joueur2
		carte_obtenue.labyrinthe.joueurs.append(joueur2)
		socket1.close()
		socket2.close()
		num_tour = random.randint(0,1)

		# Cas 1 : déplacement Nord, Sud, Est, Ouest sans précision du pas (mais en fait pas = 1)
		msg_recu = random.choice(['N','S','O','E'])
		fin, msg_a_envoyer = carte_obtenue.labyrinthe.deplacer_robot(num_tour,msg_recu)
		self.assertIn(fin,[True, False])
		self.assertIn(msg_a_envoyer,Labyrinthe.MSG.values())

		# Cas 2 : déplacement Nord, Sud, Est, Ouest sans précision du pas et p >= 1
		pas = random.randint(1,30)
		Np = "N"+ str(pas)
		Sp = "S"+ str(pas)
		Op = "O"+ str(pas)
		Ep = "E"+ str(pas)
		sg_recu = random.choice([Np,Sp,Op,Ep])
		fin, msg_a_envoyer = carte_obtenue.labyrinthe.deplacer_robot(num_tour,msg_recu)
		self.assertIn(fin,[True, False])
		self.assertIn(msg_a_envoyer,Labyrinthe.MSG.values())

		# Cas 3 : Murer(M) une porte ou Trouer(P) un mur
		pas = random.choice(['MN','MS','MO','ME','PN','PS','PO','PE'])
		fin, msg_a_envoyer = carte_obtenue.labyrinthe.deplacer_robot(num_tour,msg_recu)
		self.assertIn(fin,[True, False])
		self.assertIn(msg_a_envoyer,Labyrinthe.MSG.values())




###################### Si on exécute direcetement ce fichier #########################################################

if __name__ == "__main__":

	unittest.main()





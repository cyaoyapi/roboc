#-*- coding:utf-8 -*-

"""ce fichier contient le code principal de l'application serveur du jeu.

	Exécutez-le avec python( version 3) pour demarrer le jeu.

"""

###################### Import des modules #########################################################

import sys # Module pour interragir avec le système
import socket # Module socket pour créer des objets de connexion
import select # Module gérer des connexions multi-clients au serveur
import threading # Module pour la programmation parallèle

# On importe le module personnalisé utils qui regroupe des objets utiles pour le programme
import utils 
from joueur import Joueur

###################### Definition de tread pour la gestion simultanée des joueurs #################

class ThreadClient(threading.Thread):

	""" Objet thread gérant la réception des messages """

	def __init__(self, connexion):

		threading.Thread.__init__(self)
		self.connexion = connexion

	def run(self):
		
		global commencer
		while 1:
			msg_recu = self.connexion.recv(1024)
			msg_recu = msg_recu.decode()
			if msg_recu == "C":
				commencer = True
			print(commencer)

	
			


######################## Demarrage du Jeu : Choix du labyrinthe #####################################

# Chargement des cartes existantes
cartes = utils.lister_cartes_existantes("cartes")

# On affiche les cartes existantes
utils.afficher_cartes_existantes(cartes)

# Récupérer le choix du numéro du labyrinthe saisi par l'utilisateur (Controle de la saisie)
numero_labyrinthe = utils.saisir_numero_labyrinthe(cartes)

# La saisie est bonne on récupère le labyrinthe(carte) choisi 
carte_choisie = cartes[numero_labyrinthe - 1]



####################### Demarrage du serveur : En attente des connexions clients ######################


hote = '' # on s'attend à une connection de n'importe quel hote 
port = 12000 # port d'écoute du serveur

# connexion principale
connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Lié le serveur au port d'écoute
connexion_principale.bind((hote,port))

# Faire écouter le serveur
connexion_principale.listen(5)

print("On attend les joueurs")


####################### On écouter les connexions demandées jusqu'à ce que la partie commence(quelqu'un saisi C) ########################


commencer = False
while not commencer:

	connexions_demandees, wlist, xlist = select.select([connexion_principale],[],[],0.03)
	
	for connexion in connexions_demandees: 

		connexion_client, (ip, port) = connexion.accept()

		deja_connecte = False
		for joueur in carte_choisie.labyrinthe.joueurs:
			if joueur.ip == ip and joueur.port == port:
				deja_connecte = True

		if not deja_connecte:

			x, y = carte_choisie.labyrinthe.generer_postion_libre()
			joueur_new = Joueur(x,y,ip,port,connexion_client)
			carte_choisie.labyrinthe.grille[x][y] = joueur_new
			carte_choisie.labyrinthe.joueurs.append(joueur_new)
			
			thread_joueur = ThreadClient(connexion_client)
			thread_joueur.start()
			


			for joueur in carte_choisie.labyrinthe.joueurs:
				msg_a_envoyer = "Bienvenue, Joueur {} \n".format(joueur_new.num)
				joueur.socket.send(msg_a_envoyer.encode())
				msg_a_envoyer = carte_choisie.labyrinthe.generer_contenu(joueur)
				joueur.socket.send(msg_a_envoyer.encode())

				if Joueur.nombre > 1:
					msg_a_envoyer = "Jouer"
					joueur.socket.send(msg_a_envoyer.encode())
					msg_a_envoyer = "\nEntrez C pour commencer a jouer :\n"
					joueur.socket.send(msg_a_envoyer.encode())




####################### Le jeu commence et se dérole tant que fin = False ########################################



if commencer:
	for joueur in carte_choisie.labyrinthe.joueurs:
		joueur.socket.send("La partie commence !\n".encode())
		msg_labyrinthe = carte_choisie.labyrinthe.generer_contenu(joueur)
		joueur.socket.send(msg_labyrinthe.encode())


fin = False
message = ""

avancer = True
index = 0
while not fin:

	if avancer :
		joueur = carte_choisie.labyrinthe.joueurs[index]
		joueur.socket.send("T".encode())
		avancer = False
		index += 1
		if index == len(carte_choisie.labyrinthe.joueurs):
			index = 0
	else :
		continue



	
	
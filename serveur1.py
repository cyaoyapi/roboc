#-*- coding:utf-8 -*-

"""ce fichier contient le code principal de l'application serveur du jeu.

	Exécutez-le avec python( version 3) pour demarrer le jeu.

"""

######## Import de modules###############################################################

import sys # Module pour interragir avec le système
import socket # Module socket pour créer des objets de connexion
import select # Module gérer des connexions multi-clients au serveur
import threading # Module pour la programmation parallèle

import utils # Module contenant des objets usuelles du programme
from joueur import Joueur # Import de la classe Joueur (Robot)


######## Demarrage du jeu : choix de la carte(bayrinthe) #################################

# Chargement des cartes existantes
cartes = utils.lister_cartes_existantes("cartes")

# On affiche les cartes existantes
utils.afficher_cartes_existantes(cartes)

# Récupérer le choix du numéro du labyrinthe saisi par l'utilisateur (Controle de la saisie)
numero_labyrinthe = utils.saisir_numero_labyrinthe(cartes)

# La saisie est bonne on récupère le labyrinthe(carte) choisi 
carte_choisie = cartes[numero_labyrinthe - 1]


######## Threads pour la gestions des connexions clients #################################

verrou = threading.RLock()

class ThreadJouer(threading.Thread):

	""" Classe d'objets threads gérant les clients avant le commencement du jeu """

	def __init__(self, carte, joueur_new):

		threading.Thread.__init__(self)
		self.carte = carte
		self.joueur_new = joueur_new 

	def run(self):
		global commencer
		with verrou:
			for joueur in self.carte.labyrinthe.joueurs:
				msg_a_envoyer = "Bienvenue, Joueur {} \n".format(self.joueur_new.num)
				joueur.socket.send(msg_a_envoyer.encode())
				msg_a_envoyer = self.carte.labyrinthe.generer_contenu(joueur)
				joueur.socket.send(msg_a_envoyer.encode())

				# si le nombre de joueurs(attribut de classe Joueur) est > 1, possibilité de commencer le jeu
				if Joueur.nombre > 1:
					msg_a_envoyer = "\nEntrez C pour commencer a jouer :\n"
					joueur.socket.send(msg_a_envoyer.encode())

		msg_recu = joueur_new.socket.recv(1024)
		while True:

			msg_recu = msg_recu.decode()
		
			if not joueur_new.tour:
				msg_a_envoyer = "\nAttendez, ce n'est pas votre tour de parole :\n"
				joueur.socket.send(msg_a_envoyer.encode())
			
			elif not commencer and msg_recu.upper() == "C":
				commencer = True
				with verrou:
					for joueur in self.carte.labyrinthe.joueurs:
						joueur.tour = False
						msg_a_envoyer = "La partie commence !\n"
						joueur.socket.send(msg_a_envoyer.encode())
						msg_a_envoyer = self.carte.labyrinthe.generer_contenu(joueur)
						joueur.socket.send(msg_a_envoyer.encode())

			elif not commencer and msg_recu.upper() != "C" :
				msg_a_envoyer = "La saisie n'est pas bonne. Reprenez !\n"
				joueur_new.socket.send(msg_a_envoyer.encode())


			if commencer:
				fin = False
				message = ""

				num_joueur = 0
				while not fin:
					joueur = self.carte.labyrinthe.joueurs[num_joueur]
					joueur.tour = True
					msg_a_envoyer = "\nC'est votre tour !\n"
					joueur.socket.send(msg_a_envoyer.encode())
					msg_a_envoyer = "\nDeplacez votre votre robot(Grand X) : \n"
					joueur.socket.send(msg_a_envoyer.encode())
					msg_recu = joueur.socket.recv(1024)
					msg_recu = msg_recu.decode()
					print(msg_recu)
					num_joueur += 1
					if num_joueur == Joueur.nombre :
						num_joueur = 0
						
					# appel de la méthode déplacer du labyrinthe
					# A la sortie fait les tests de sortie soit pour arrêter, soit passer au joueur suivant
			

			msg_recu = joueur_new.socket.recv(1024)


######## Tentative de demarrage du serveur ###############################################


HOTE = '' # on s'attend à une connection de n'importe quel hote 
PORT = 12000 # port d'écoute du serveur

# connexion principale
connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Lié le serveur au port d'écoute
try :
	connexion_principale.bind((HOTE,PORT))
except socket.error :
	print("La liaison du serveur au port choisi a echoué\n")
	sys.exit()

# Faire écouter le serveur
connexion_principale.listen(5)

print("On attend les joueurs")

####################### Communication avec les clients ################################

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
			thread_joueur = ThreadJouer(carte_choisie, joueur_new)
			thread_joueur.start()
			

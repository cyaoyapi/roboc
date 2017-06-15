#-*- coding:utf-8 -*-

"""ce fichier contient le code principal de l'application serveur du jeu.

	Exécutez-le avec python( version 3) pour demarrer le jeu.

"""

###################### Import des modules #########################################################

import sys # Module pour interragir avec le système
import socket # Module socket pour créer des objets de connexion
import select # Module gérer des connexions multi-clients au serveur

# On importe le module personnalisé utils qui regroupe des objets utiles pour le programme
import utils 
from joueur import Joueur



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
try:
	connexion_principale.bind((hote,port))
except socket.error:
	print("La liason avec le port a echoué")
	sys.exit()

# Faire écouter le serveur
connexion_principale.listen(5)

print("On attend les joueurs")


####################### Selection des joueurs avant le début de la partie ########################


serveur_lancer = True
commencer = False
clients_connectes = []

while not commencer:

	connexions_demandees, wlist, xlist = select.select([connexion_principale],[],[],0.03)
	
	for connexion in connexions_demandees: 

		connexion_client, (ip, port) = connexion.accept()

		clients_connectes.append(connexion_client)

		deja_connecte = False
		for joueur in carte_choisie.labyrinthe.joueurs:
			if joueur.ip == ip and joueur.port == port:
				deja_connecte = True

		if not deja_connecte:

			x, y = carte_choisie.labyrinthe.generer_postion_libre()
			joueur_new = Joueur(x,y,ip,port,connexion_client)
			carte_choisie.labyrinthe.grille[x][y] = joueur_new
			carte_choisie.labyrinthe.joueurs.append(joueur_new)
			
			print("{} connecté(s)".format(Joueur.nombre))


			for joueur in carte_choisie.labyrinthe.joueurs:
				msg_a_envoyer = "Bienvenue, Joueur {} \n".format(joueur_new.num)
				joueur.socket.send(msg_a_envoyer.encode())
				msg_a_envoyer = carte_choisie.labyrinthe.generer_contenu(joueur)
				joueur.socket.send(msg_a_envoyer.encode())

				if Joueur.nombre > 1:
					msg_a_envoyer = "\nEntrez C pour commencer a jouer :\n"
					joueur.socket.send(msg_a_envoyer.encode())

	
	clients_a_lire = [] 
	try:
		clients_a_lire, wlist, xlist = select.select(clients_connectes,[],[],0.03)

	except select.error:
		pass

	else:
		for client in clients_a_lire:
			msg_recu = client.recv(1024)
			msg_recu = msg_recu.decode()
			print(msg_recu)

			if Joueur.nombre < 2:
				msg_a_envoyer = "Patientez qu'au moins un autre joueur se connecte !"
				client.send(msg_a_envoyer.encode())

			elif msg_recu.upper() == "C":
				commencer = True
				break

			else:
				msg_a_envoyer = "Saisie invalide. reprenez !"
				client.send(msg_a_envoyer.encode())

		if commencer:
			for joueur in carte_choisie.labyrinthe.joueurs:
				msg_a_envoyer = "La partie a commencé. Attendez que ce soit votre tour pour jouer !\n"
				joueur.socket.send(msg_a_envoyer.encode())

			break
 






####################### Le jeu commence et se dérole tant que fin = False ########################################

fin = False
message = ""

num_tour = 0

while not fin:
	
	joueur = carte_choisie.labyrinthe.joueurs[num_tour]
	msg_a_envoyer = "C'est votre tour! Deplacez votre robot(X)"
	joueur.socket.send(msg_a_envoyer.encode())
	msg_recu = joueur.socket.recv(2014)
	print(msg_recu.decode())

	#Mettre ici le code du deplacement

	if num_tour == Joueur.nombre - 1:
		num_tour = 0
	else:
		num_tour += 1








	
	
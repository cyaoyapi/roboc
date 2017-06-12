#-*- coding:utf-8 -*-

"""ce fichier contient le code principal de l'application serveur du jeu.

	Exécutez-le avec python( version 3) pour demarrer le jeu.

"""

###################### Import des modules #########################################################

import sys # Module pour interragir avec le système
import socket # Module socket pour créer des objets de connexion
import select # Module gérer des connexions multi-clients au serveur

# On importe le module utils qui regroupe des objets utiles pour le programme
import utils 


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


hote = '' # s'attend à une connection de n'importe quel hote 
port = 12000 # port d'écoute du serveur

# connexion principale
connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Lié le serveur
connexion_principale.bind((hote,port))

# Faire écouter le serveur
connexion_principale.listen(5)

print("On attend les joueurs")


####################### Gestion des connexions et communications avec les clients ########################

server_lance = True
clients_connectes = []


while server_lance:

	connexions_demandees, wlist, xlist = select.select([connexion_principale],[],[],0.03)

	for connexion in connexions_demandees:

		connexion_client, infos_connexion = connexion.accept()
		clients_connectes.append(connexion_client)

	clients_a_lire= []

	try:
		clients_a_lire, wlist, xlist = select.select(clients_connectes,[],[],0.03)

	except select.error:
		pass

	else:
		for client in clients_a_lire:
			msg_recu = client.recv(1024)
			print("Message recu : {}".format(msg_recu.decode()))
			client.send(b"Bien recu 5/5")

			if msg_recu == b"fin":
				server_lance = False


####################### Fin du programme ########################################################################


print("Fermeture de la connexion")

for client in clients_a_lire:
	client.close()

connexion_principale.close()
#-*- coding:utf-8 -*-

"""ce fichier contient le code principal de l'application serveur du jeu.

	Exécutez-le avec python( version 3) pour demarrer le jeu.

"""

###################### Import des modules #########################################################

import sys # Module pour interragir avec le système
import socket # Module socket pour créer des objets de connexion
import select # Module gérer des connexions multi-clients au serveur
import re # Module pour la gestion des expressions regulières
import time

from obstacle.vide import Vide
from joueur import Joueur

# On importe le module personnalisé utils qui regroupe des objets utilitaires
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
REGEX1 = r"^[NESO]([1-9][0-9]*)*$" # Motif de choix valide de déplacement du robot
REGEX2 = r"^[MP][NESO]$" # Motif de choix valide de déplacement du robot

num_tour = 1
while not fin:
	
	joueur = carte_choisie.labyrinthe.joueurs[num_tour - 1]
	msg_a_envoyer = "C'est votre tour! Deplacez votre robot(Grand X)"
	joueur.socket.send(msg_a_envoyer.encode())

	print("tour = {} VS num= {}".format(num_tour,joueur.num))

	######Mettre ici le code du deplacement#####
	choix_valide = False
	# Tant que le choix n'est pas valide
	while not choix_valide:

		msg_recu = joueur.socket.recv(2014)
		msg_recu = msg_recu.decode()
		if re.match(REGEX1,msg_recu.upper()) is not None or re.match(REGEX2,msg_recu.upper()) is not None or msg_recu.upper() == "Q":
			choix_valide = True
		else :
			msg_a_envoyer = "Choix de déplacement non valide. reprenez !\n"
			joueur.socket.send(msg_a_envoyer.encode())
	# Si le choix est de quitter l'application
	if msg_recu.upper() == "Q":

		if num_tour == len(carte_choisie.labyrinthe.joueurs):
			num_tour = 1
		#else:
			#num_tour = num_tour 
		
		vide = Vide(joueur.x,joueur.y)
		carte_choisie.labyrinthe.grille[joueur.x][joueur.y] = vide
		carte_choisie.labyrinthe.joueurs.remove(joueur)
		# On retrie les éléments restants
		carte_choisie.labyrinthe.joueurs = sorted(carte_choisie.labyrinthe.joueurs, key= lambda chaque_joueur: chaque_joueur.num)
		msg_a_envoyer = """
		Vous quittez la partie. 
		Vous serez déconnectés dans moins de 3 secondes.
		Faites CTRL + C pour vous deconnecté vous-même.
		Aurevoir et à bientôt !
		"""
		joueur.socket.send(msg_a_envoyer.encode())

		tps=time.time()

		while time.time() - tps < 3:
			pass

		print(carte_choisie.labyrinthe.joueurs)
		tps=time.time()

		while time.time() - tps < 5:
			pass
		for chaque_joueur in carte_choisie.labyrinthe.joueurs:
			msg_a_envoyer = "Le joueur {} vient de quitter la partie. Toutefois, elle se poursuit\n".format(joueur.num)
			chaque_joueur.socket.send(msg_a_envoyer.encode())
			msg_a_envoyer = carte_choisie.labyrinthe.generer_contenu(chaque_joueur)
			chaque_joueur.socket.send(msg_a_envoyer.encode())

		tps=time.time()

		while time.time() - tps < 5:
			pass


	# Si le choix de déplacement est valide
	else:
		fin, msg_a_envoyer = carte_choisie.labyrinthe.deplacer_robot(num_tour -1, msg_recu.upper())
		if not fin:
			joueur.socket.send(msg_a_envoyer.encode())
			msg_a_envoyer = "Patientez à nouveau que ce soit votre tour de jouer.\n"
			joueur.socket.send(msg_a_envoyer.encode())
			for chaque_joueur in carte_choisie.labyrinthe.joueurs:
				msg_a_envoyer = carte_choisie.labyrinthe.generer_contenu(chaque_joueur)
				chaque_joueur.socket.send(msg_a_envoyer.encode())
		else:
			joueur.socket.send(msg_a_envoyer.encode())
			msg_a_envoyer = carte_choisie.labyrinthe.generer_contenu(chaque_joueur)
			joueur.socket.send(msg_a_envoyer.encode())
			break


		if num_tour == len(carte_choisie.labyrinthe.joueurs):
			num_tour = 1
		else:
			num_tour += 1



		
			

	


#########"C'est la fin #####################


joueur_gangant = carte_choisie.labyrinthe.joueurs[num_tour - 1]

for chaque_joueur in carte_choisie.labyrinthe.joueurs:

	if chaque_joueur.ip != joueur_gangant.ip or chaque_joueur.port != joueur_gangant.port:
		msg_a_envoyer = "Le joueur {} a gagné la partie. Vous avez perdu !\n".format(joueur_gangant.num)
		chaque_joueur.socket.send(msg_a_envoyer.encode())
		msg_a_envoyer = carte_choisie.labyrinthe.generer_contenu(chaque_joueur)
		chaque_joueur.socket.send(msg_a_envoyer.encode())
	

	msg_a_envoyer = """
	C'est la fin de la partie. Merci et à bientôt.
	Votre client sera déconnecté dans moins de 15 sécondes.
	Faites CTRL + C pour arrêter vous-même votre client.
	"""
	chaque_joueur.socket.send(msg_a_envoyer.encode())

print("Le joueur {} a gagné la partie \n".format(joueur_gangant.num))
print("C'est la fin de la partie. Merci et à bientôt\n")


tps=time.time()

while time.time() - tps < 15 :
	pass

for chaque_joueur in carte_choisie.labyrinthe.joueurs:
	chaque_joueur.socket.close()



connexion_principale.close()
sys.exit()
	








	
	
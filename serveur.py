#-*- coding:utf-8 -*-

"""ce fichier contient le code principal de l'application serveur du jeu.

	Exécutez-le avec python( version 3) pour demarrer le jeu.

"""

###################### Import des modules #########################################################

import sys # Module pour interragir avec le système
import socket # Module socket pour créer des objets de connexion
import select # Module gérer des connexions multi-clients au serveur
import re # Module pour la gestion des expressions regulières
import time # Ici pour simuler des délais

from obstacle.vide import Vide
from joueur import Joueur

import utils # Module regroupant des objets utiles


######################## Demarrage du Jeu : Choix du labyrinthe ##################################

# Chargement des cartes existantes
cartes = utils.lister_cartes_existantes("cartes")

# On affiche les cartes existantes
utils.afficher_cartes_existantes(cartes)

# Récupérer le choix du numéro du labyrinthe saisi (Controle de la saisie)
numero_labyrinthe = utils.saisir_numero_labyrinthe(cartes)

# La saisie est bonne on récupère le labyrinthe(carte) choisi 
carte_choisie = cartes[numero_labyrinthe - 1]


####################### Demarrage du serveur : En attente des connexions clients #################


HOTE = '' # on s'attend à une connection de n'importe quel hote 
PORT = 12000 # port d'écoute du serveur

# connexion principale
connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Lié le serveur au port d'écoute
try:
	connexion_principale.bind((HOTE,PORT))
except socket.error:
	print("La liason avec le port a echoué")
	sys.exit()

# Faire écouter le serveur
connexion_principale.listen(5)

print("On attend les joueurs")


####################### Selection de joueurs avant le début de la partie ########################

commencer = False
clients_connectes = []

# Tant que la partie n'a pas encore commencer, on récupère les connexions démandées et les acceptent
while not commencer:

	# On récupère les connexions demandées avec select
	connexions_demandees, wlist, xlist = select.select([connexion_principale],[],[],0.03)
	
	for connexion in connexions_demandees: 
		connexion_client, (ip, port) = connexion.accept()
		clients_connectes.append(connexion_client)
		# On vérifie si ce client est déjà selectionné
		deja_connecte = False
		for joueur in carte_choisie.labyrinthe.joueurs:
			if joueur.ip == ip and joueur.port == port:
				deja_connecte = True
		# Si c'est un nouveau connecté, on l'ajoute au labyrinthe
		if not deja_connecte:
			x, y = carte_choisie.labyrinthe.generer_postion_libre()
			joueur_new = Joueur(x,y,ip,port,connexion_client)
			carte_choisie.labyrinthe.grille[x][y] = joueur_new
			carte_choisie.labyrinthe.joueurs.append(joueur_new)
			print("{} joueur(s) connecté(s)".format(Joueur.nombre))
			# On informe tous les joueurs selectionnés de l'arrivée du nouveau
			for joueur in carte_choisie.labyrinthe.joueurs:
				msg_a_envoyer = "Bienvenue, Joueur {} \n".format(joueur_new.num)
				joueur.socket.send(msg_a_envoyer.encode())
				msg_a_envoyer = carte_choisie.labyrinthe.generer_contenu(joueur)
				joueur.socket.send(msg_a_envoyer.encode())
				# Si le nombre de joueur est > 1, on peut commencer la partie si quelqu'un saisie "C"
				if Joueur.nombre > 1:
					msg_a_envoyer = "\nEntrez C pour commencer a jouer :\n"
					joueur.socket.send(msg_a_envoyer.encode())

	# On récupère à aprtie des connexions acceptées la liste
	# des connexion à lire (Ceux qui on envoyé un message au serveur)
	clients_a_lire = [] 
	try:
		clients_a_lire, wlist, xlist = select.select(clients_connectes,[],[],0.03)
	except select.error:
		pass
	else:
		for client in clients_a_lire:
			msg_recu = client.recv(1024)
			msg_recu = msg_recu.decode()
			# Si le joueur est seul
			if Joueur.nombre < 2:
				msg_a_envoyer = "Patientez qu'au moins un autre joueur se connecte !"
				client.send(msg_a_envoyer.encode())
			# Si le nombre de  joueurs est > 1 et que quelqu'un saisi "C", on commence la partie
			elif msg_recu.upper() == "C":
				commencer = True
				#Coté serveur
				print("La partie commence et est en cours...")
				break
			# Si la saisie n'est pas bonne (n'est pas "C")
			else:
				msg_a_envoyer = "Saisie invalide. reprenez !"
				client.send(msg_a_envoyer.encode())
		# La partie commence, on informe les joueurs selectionnés
		if commencer:
			for joueur in carte_choisie.labyrinthe.joueurs:
				msg_a_envoyer = "La partie commence.\n"
				joueur.socket.send(msg_a_envoyer.encode())
				joueur.socket.send(utils.INSTRUCTIONS.encode())
				msg_a_envoyer = carte_choisie.labyrinthe.generer_contenu(joueur)
				joueur.socket.send(msg_a_envoyer.encode())
				msg_a_envoyer = "Attendez que ce soit votre tour pour jouer !\n"
				joueur.socket.send(msg_a_envoyer.encode())
			# On ne prend plus de joueurs on sort de la boucle while
			break
 


####################### Le jeu commence et se dérole tant que fin = False ########################################

#drapeau de fin de jeu
fin = False
#Constantes et expressions regulières
REGEX1 = r"^[NESO]([1-9][0-9]*)*$" # Motif de validation du choix valide de déplacement du robot
REGEX2 = r"^[MP][NESO]$" # Motif de choix de validation pour Murer une porte ou Trouer un mur

num_tour = 1 # initialisation du numéro de tour 1 ( c'est le premier joueur qui commence la partie)
while not fin:
	# On récupère le joueur dont c'est le tour
	joueur = carte_choisie.labyrinthe.joueurs[num_tour - 1]
	msg_a_envoyer = "C'est votre tour! Deplacez votre robot(Grand X)"
	joueur.socket.send(msg_a_envoyer.encode())
	# On teste la saisie
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
		# Si c'était le tour du dernier joueur de la liste et qu'il veut quitter
		if num_tour == len(carte_choisie.labyrinthe.joueurs):
			num_tour = 1 # On retourne directement au premier joueur
		# Sinon On reprend la boucle avec le même numero de tour. On n'incrémente pas num_tour
		# En fait le nombre de joueurs a dimunué, le suivant devient celui qui est à la
		# position num_tour courante
		#else:
			#num_tour = num_tour 
		# On remplace la position du joueur qui quitte le jeu par un vide
		vide = Vide(joueur.x,joueur.y)
		carte_choisie.labyrinthe.grille[joueur.x][joueur.y] = vide
		carte_choisie.labyrinthe.joueurs.remove(joueur) # on le supprime de la liste des joueurs
		# On retrie la liste des joueurs restants par ordre croissant de numéro (attribut num d'un objet joueur : ordre de connexion au jeu)
		carte_choisie.labyrinthe.joueurs = sorted(carte_choisie.labyrinthe.joueurs, key= lambda chaque_joueur: chaque_joueur.num)
		msg_a_envoyer = """
		Vous quittez la partie. 
		Vous serez déconnectés dans moins de 3 secondes.
		Faites CTRL + C pour vous deconnecté vous-même.
		Aurevoir et à bientôt !
		"""
		joueur.socket.send(msg_a_envoyer.encode())
		# Pour ne pas que la déconnexion soit brutale (delai de 3 secondes)
		tps=time.time()
		while time.time() - tps < 3:
			pass
		# On ferme son socket
		joueur.socket.close()
		# On informe les autres de son départ
		for chaque_joueur in carte_choisie.labyrinthe.joueurs:
			msg_a_envoyer = "Le joueur {} vient de quitter la partie. Toutefois, elle se poursuit\n".format(joueur.num)
			chaque_joueur.socket.send(msg_a_envoyer.encode())
			msg_a_envoyer = carte_choisie.labyrinthe.generer_contenu(chaque_joueur)
			chaque_joueur.socket.send(msg_a_envoyer.encode())

		# On attend un délai de 2 sécondes pour passer au tour suivant
		tps=time.time()
		while time.time() - tps < 2:
			pass

	# Si le choix de déplacement est valide
	else:
		# On essaie de déplacer le joueur
		fin, msg_a_envoyer = carte_choisie.labyrinthe.deplacer_robot(num_tour -1, msg_recu.upper())
		# Si le resulat du déplacement n'implique pas la fin du jeu 
		if not fin:
			# On demande au joueur d'attendre son tour prochain avnt de joueur à nouveau
			joueur.socket.send(msg_a_envoyer.encode())
			msg_a_envoyer = "Patientez à nouveau que ce soit votre tour de jouer.\n"
			joueur.socket.send(msg_a_envoyer.encode())
			# On affiche pour tous le nouvel état du labyrinthe suite au déplacement récent du joueur dont c'était le tour
			for chaque_joueur in carte_choisie.labyrinthe.joueurs:
				msg_a_envoyer = carte_choisie.labyrinthe.generer_contenu(chaque_joueur)
				chaque_joueur.socket.send(msg_a_envoyer.encode())
		
		# Si le déplacement impliqiue la fin du jeu
		else:
			joueur.socket.send(msg_a_envoyer.encode())
			msg_a_envoyer = carte_choisie.labyrinthe.generer_contenu(chaque_joueur)
			joueur.socket.send(msg_a_envoyer.encode())
			# On sort de la boucle (fin = True)
			break

		# Si tout vas vient (ce n'es pas la fin ou le joeur ne quitte pas)
		# Si c'est le dernier joueur de la liste qui est en cours, on retourne au premier
		if num_tour == len(carte_choisie.labyrinthe.joueurs):
			num_tour = 1
		# Sinon on passe au suivant
		else:
			num_tour += 1



#########C'est la fin : on est sortie de la boucle #####################

# On récupère le joueur gagnant
joueur_gagnant = carte_choisie.labyrinthe.joueurs[num_tour - 1]

# On informe tous les joueurs
for chaque_joueur in carte_choisie.labyrinthe.joueurs:

	if chaque_joueur.ip != joueur_gagnant.ip or chaque_joueur.port != joueur_gagnant.port:
		msg_a_envoyer = "Le joueur {} a gagné la partie. Vous avez perdu !\n".format(joueur_gagnant.num)
		chaque_joueur.socket.send(msg_a_envoyer.encode())
		msg_a_envoyer = carte_choisie.labyrinthe.generer_contenu(chaque_joueur)
		chaque_joueur.socket.send(msg_a_envoyer.encode())
	

	msg_a_envoyer = """
	C'est la fin de la partie. Merci et à bientôt.
	Votre client sera déconnecté dans moins de 10 sécondes.
	Faites CTRL + C pour arrêter vous-même votre client.
	"""
	chaque_joueur.socket.send(msg_a_envoyer.encode())
# Coté serveur
print("Le joueur {} a gagné la partie \n".format(joueur_gagnant.num))
print("C'est la fin de la partie. Merci et à bientôt\n")

# On attent 10 secondes avant de tout arrêter pour ne pas que ce soit brusque
tps=time.time()
while time.time() - tps < 10 :
	pass

for chaque_joueur in carte_choisie.labyrinthe.joueurs:
	chaque_joueur.socket.close()

connexion_principale.close()
sys.exit()
	








	
	
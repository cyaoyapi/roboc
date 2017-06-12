#-*- coding:utf-8 -*-

"""Ce fichier contient le code l'application client.

	Exécutez-le avec python( version 3) pour connecter un joueur au serveur.

"""

###################### Import des modules #########################################################

import sys # Module pour interragir avec le système
import socket # Module socket pour créer des objets de connexion

# On importe le module utils qui regroupe des objets utiles pour le programme
import utils 


####################### Demarrage du client : Connexion avec le serveur######################


hote = 'localhost' # hostname du serveur
port = 12000 # port d'écoute du serveur

# création de d'objet socket pour la connexion avec le serveur
connexion_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# on se connecte au serveur
connexion_serveur.connect((hote,port))

print("Connexion établie avec le serveur")

####################### Gestion des communications avec le serveur ######################


msg_a_envoyer = b""

while msg_a_envoyer != b"fin":

	msg_a_envoyer = input("Entrez votre choix de déplacement : \n >")
	connexion_serveur.send(msg_a_envoyer.encode())
	msg_recu = connexion_serveur.recv(1024)
	print("Message reçu : {}".format(msg_recu.decode()))


####################### Fermeture de la connexion avec le serveur ######################

print("Fermeture de la connexion")
connexion_serveur.close()
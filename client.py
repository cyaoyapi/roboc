#-*- coding:utf-8 -*-

"""Ce fichier contient le code l'application client.

	Exécutez-le avec python( version 3) pour connecter un joueur au serveur.

"""

###################### Import des modules #########################################################

import sys # Module pour interragir avec le système
import socket # Module socket pour créer des objets de connexion
import threading # Module pour la programmation parallèle
import time # Ici pour simuler des délais

import utils # Module regroupant des objets utils


###################### Definition de 2 Threads : l'un pour l'envoi et l'autre la reception#########

class Recevoir(threading.Thread):

	"""Objet thread gérant la réception des messages"""

	def __init__(self, connexion):

		threading.Thread.__init__(self)
		self.connexion = connexion

	def run(self):

		while True:

			try:
				msg_recu = self.connexion.recv(1024)
			except socket.error:
				print("Vous êtes déconnecté du serveur")
				break
			else:
				msg_recu = msg_recu.decode()
				print(msg_recu)

		tps=time.time()

		while time.time() - tps < 3 :
			pass

		self.connexion.close()
		sys.exit()

		



class Envoyer(threading.Thread):

	"""objet thread gérant l'émission des messages"""

	def __init__(self, connexion):

		threading.Thread.__init__(self)
		self.connexion = connexion

	def run(self):

		while True:
			try:
				msg_a_envoyer = input()
			except socket.error:
				print("Vous êtes déconnecté du serveur")
			else:
				self.connexion.send(msg_a_envoyer.encode())
				if msg_a_envoyer.upper() == "Q":
					break

		tps=time.time()
		while time.time() - tps < 3 :
			pass

		self.connexion.close()
		sys.exit()


####################### Programme principal du client : Connexion avec le serveur######################

HOTE = 'localhost' # on s'attend à une connection de n'importe quel hote 
PORT = 12000 # port d'écoute du serveur

connexion_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	print("On tente de se connecter au serveur...\n")
	connexion_server.connect((HOTE, PORT))
except socket.error:
	print ("La connexion a échoué.")
	sys.exit()    
else :
	print("Connexion établie avec le serveur.")

# Dialogue avec le serveur : on lance deux threads pour gérer
# indépendamment l'émission et la réception des messages :
thread_envoi = Envoyer(connexion_server)
thread_reception = Recevoir(connexion_server)  

thread_reception.start()
thread_envoi.start()

thread_reception.join()
thread_envoi.join()







#-*- coding:utf-8 -*-

"""Ce fichier contient le code l'application client.

	Exécutez-le avec python( version 3) pour connecter un joueur au serveur.

"""

###################### Import des modules #########################################################

import sys # Module pour interragir avec le système
import socket # Module socket pour créer des objets de connexion
import threading # Module pour la programmation parallèle

# On importe le module utils qui regroupe des objets utiles pour le programme
import utils 


###################### Definition de 2 Threads : l'un pour l'envoi et l'autre la reception####

class ThreadReception(threading.Thread):

	"""Objet thread gérant la réception des messages"""

	def __init__(self, connexion):

		threading.Thread.__init__(self)
		self.connexion = connexion

	def run(self):

		while True:

			msg_recu = self.connexion.recv(1024)
			msg_recu = msg_recu.decode()
			print(msg_recu)

		self.connexion.close()
		sys.exit()

		



class ThreadEmission(threading.Thread):

	"""objet thread gérant l'émission des messages"""
	def __init__(self, connexion):

		threading.Thread.__init__(self)
		self.connexion = connexion

	def run(self):
		while True:
			msg_emis = input()
			self.connexion.send(msg_emis.encode())

		


####################### Programme principal du client : Connexion avec le serveur######################

hote = '' # on s'attend à une connection de n'importe quel hote 
port = 12000 # port d'écoute du serveur

connexion_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	print("On tente de se connecter au serveur...\n")
	connexion_server.connect((hote, port))
except socket.error:
	print ("La connexion a échoué.")
	sys.exit()    
else :
	print("Connexion établie avec le serveur.")

# Dialogue avec le serveur : on lance deux threads pour gérer
# indépendamment l'émission et la réception des messages :
thread_emission = ThreadEmission(connexion_server)
thread_reception = ThreadReception(connexion_server)  


thread_reception.start()
thread_emission.start()

thread_reception.join()
thread_emission.join()







# -*-coding:Utf-8 -*

"""Ce module contient la classe Joueur.

	Elle permet de créer des joeurs(robots)

"""

class Joueur:

    """Classe représentant un robot."""

    symbole = "X"

    nombre = 0
    
    def __init__(self, x, y, ip, port, socket):

        self.x = x  
        self.y = y
        self.ip = ip
        self.port = port
        self.socket = socket
        Joueur.nombre += 1
        self.num = Joueur.nombre

    def __repr__(self):
        return "<Joueur num ={} x={} y={}> connecté depuis {}:{}".format(self.num, self.x, self.y, self.ip, self.port)

    def __str__(self):
        return "Joueur {} [{},{}] connecté depuis {}:{}".format(self.num,self.x, self.y, self.ip, self.port)


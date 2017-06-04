# -*-coding:Utf-8 -*

"""Ce module contient la classe Labyrinthe."""

class Labyrinthe:

    """Classe représentant un labyrinthe."""

    def __init__(self, robot, obstacles):
        self.robot = robot
        self.grille = obstacles.split("\n")


    def afficher(self):

    	"""Méthode affichant le labyrinthe"""

    	for ligne in self.grille:
    		print(ligne)


    def detecter_position_robot(self):

    	"""Méthode retournant les coordonnées du robot"""

    	robot_ligne = 0
    	for ligne in self.grille:
    		if self.robot in ligne:
    			robot_colonne = ligne.find(self.robot)
    			break
    		else:
    			robot_ligne += 1
    			continue
    	return [robot_ligne,robot_colonne]


    #def deplacer_robot(self, choix)
    	
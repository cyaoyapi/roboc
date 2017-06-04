# -*-coding:Utf-8 -*

"""Ce module contient la classe Labyrinthe."""

class Labyrinthe:

    """Classe représentant un labyrinthe."""

    def __init__(self, robot, obstacles):
        self.robot = robot
        self.grille = obstacles.split("\n")
        self.obstacle_anterieur = robot


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


    def deplacer_robot(self, choix):

        """Methode permettant de controler le deplacement du robot"""

        message = ""


        robot_ligne_actuelle, robot_colonne_actuelle = self.detecter_position_robot()

        if len(choix) == 1 :
            orientation = choix[0]
            pas = 1
        else :
            orientation = choix[0]
            pas = int(choix[1:])


    	# En fonction de l'orientation

        if orientation == "N" :

            robot_ligne_nouvelle = robot_ligne_actuelle - pas
            robot_colonne_nouvelle = robot_colonne_actuelle

            if robot_ligne_nouvelle < 0 :
                message = "H"

            # Vérification d'obstacles intermédiares

            elif pas > 1:
                i = robot_ligne_actuelle - 1
                collision = False
                while i < robot_ligne_nouvelle:
                    if self.grille[i][robot_colonne_actuelle] == "O":
                        collision = True
                        break
                if collision :
                    message = "Désolé : Collision avec un mur!\nPartie perdue"
                else:
                    self.obstacle_anterieur = self.grille[robot_ligne_nouvelle][robot_colonne_nouvelle]
                    


            



        elif orientation == "S" :

            robot_ligne_nouvelle = robot_ligne_actuelle + pas
            robot_colonne_nouvelle = robot_colonne_actuelle

            if robot_ligne_nouvelle > len(self.grille) :
                message = "H"

        elif orientation == "E" :

            robot_ligne_nouvelle = robot_ligne_actuelle 
            robot_colonne_nouvelle = robot_colonne_actuelle + pas

            if robot_colonne_nouvelle > len(self.grille[0]) :
                message = "H"

        else:

            robot_ligne_nouvelle = robot_ligne_actuelle 
            robot_colonne_nouvelle = robot_colonne_actuelle - pas

            if robot_colonne_nouvelle < 0 :
                message = "H"


        return message

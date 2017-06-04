# -*-coding:Utf-8 -*

"""Ce module contient la classe Labyrinthe."""

class Labyrinthe:

    """Classe représentant un labyrinthe."""


    # Définition d'une constante de classe pour la gestion des messages utilisateurs

    MSG = {
        "H":"Désolé ! Vous êtes hors de la zone du labyrithe : vous avez perdu !",
        "C":"Désolé ! Collision avec un mur : Vous avez perdu !",
        "B": "Bravo ! Vous avancez bien  : Continuez !",
        "F": "Félicitations ! Vous avez gagné !"

    }


    def __init__(self, robot, contenu):
        self.robot = robot

        # On construit la grille du Labyrinthe à partir du contenu du fichier(carte)
        self.grille = contenu.split("\n") 

        # prend la valeur de l'obstacle avant de le remplacer par le robot
        # utile pour l'affiche quand le robot quitte a nouveau cette position
        self.obstacle_anterieur = " "  


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



    def gerer_lignes_deplacement_y(self,robot_ligne_actuelle, robot_colonne_actuelle,robot_ligne_nouvelle, robot_colonne_nouvelle ):

        """Cette méthode permet de reconstruire les lignes impactées par le déplacement vertical(N et S) du robt
            
            Deux lignes sont impactées lors d'un déplacement horizontal :
            -la ligne actuelle où se trouve le robot
            -la ligne nouvelle où on désir positionner le robot.

        """
        
        robot_ligne_actuelle = int(robot_ligne_actuelle)
        robot_colonne_actuelle = int(robot_colonne_actuelle)
        robot_ligne_nouvelle = int(robot_ligne_nouvelle)
        robot_colonne_nouvelle = int(robot_colonne_nouvelle)

        # Gestion de l'apparence de la ligne actuelle après le déplacement du robot
        ligne_actuelle = self.grille[robot_ligne_actuelle]
        ligne_actuelle_2_list = list(ligne_actuelle) # On transforme la ligne(chaine de caractères) en liste(objet mutable)
        ligne_actuelle_2_list[robot_colonne_actuelle] = self.obstacle_anterieur
        ligne_actuelle = ("").join(ligne_actuelle_2_list) # On reconstruire la chaine de caractère à partir de la liste modifiée
        self.grille[robot_ligne_actuelle] = ligne_actuelle

        # Conserver l'obstacle actuelle de la zone que va occuper le robot après son déplacement
        self.obstacle_anterieur = self.grille[robot_ligne_nouvelle][robot_colonne_nouvelle]

        # Gestion de l'apparence de la ligne futur qui accueil le robot après son déplacement
        ligne_nouvelle = self.grille[robot_ligne_nouvelle]
        ligne_nouvelle_2_list = list(ligne_nouvelle) # On transforme la ligne(chaine de caractères) en liste(objet mutable)
        ligne_nouvelle_2_list[robot_colonne_nouvelle] = "X"
        ligne_nouvelle = ("").join(ligne_nouvelle_2_list) # On reconstruire la chaine de caractère à partir de la liste modifiée
        self.grille[robot_ligne_nouvelle] = ligne_nouvelle



    def gerer_ligne_deplacement_x(self,robot_ligne_actuelle, robot_colonne_actuelle,robot_ligne_nouvelle, robot_colonne_nouvelle ):

        """Cette méthode permet de reconstruire la ligne impactée par le déplacement horizontale(E et O) du robt
            
            Une seule ligne est impactée par un déplacement vertical :
            le robot reste sur la même ligne. seule les colonnes avant et 
            après déplacement sont impactés.

        """
        
        robot_ligne_actuelle = int(robot_ligne_actuelle)
        robot_colonne_actuelle = int(robot_colonne_actuelle)
        robot_ligne_nouvelle = int(robot_ligne_nouvelle)
        robot_colonne_nouvelle = int(robot_colonne_nouvelle)

        # Gestion de l'apparence de la ligne actuelle après le déplacement du robot
        ligne_actuelle = self.grille[robot_ligne_actuelle]
        ligne_actuelle_2_list = list(ligne_actuelle) # On transforme la ligne(chaine de caractères) en liste(objet mutable)
        ligne_actuelle_2_list[robot_colonne_actuelle] = self.obstacle_anterieur

            # Conserver l'obstacle actuelle de la zone que va occuper le robot après son déplacement
        self.obstacle_anterieur = self.grille[robot_ligne_nouvelle][robot_colonne_nouvelle]

        ligne_actuelle_2_list[robot_colonne_nouvelle] = "X"
        ligne_actuelle = ("").join(ligne_actuelle_2_list) # On reconstruire la chaine de caractère à partir de la liste modifiée
        self.grille[robot_ligne_actuelle] = ligne_actuelle



    def deplacer_robot(self, choix):

        """Methode permettant de controler le deplacement du robot
            
            Elle retourne 2 paramètre :

            - fin (Boolean) : Qui inqique si on continue le jeu(False) ou si on arrête(True)
            - message : Un message explicite à l'endroit de l'utilisateur

        """

        fin = False
        message = ""

        # on recupère les coordonnées actuelles du robot

        robot_ligne_actuelle, robot_colonne_actuelle = self.detecter_position_robot()

        # On détermine l'orientation du déplacement et si possible le pas

        if len(choix) == 1 :
            orientation = choix[0]
            pas = 1
        else :
            orientation = choix[0]
            pas = int(choix[1:])


    	# Si l'orientation de déplacement est le N : Nord

        if orientation == "N" :

            robot_ligne_nouvelle = robot_ligne_actuelle - pas
            robot_colonne_nouvelle = robot_colonne_actuelle

            # Si le déplacement amène le robot hors de la zone du labyrinthe
            if robot_ligne_nouvelle < 0 :
                fin = True
                message = Labyrinthe.MSG["H"]

            # Si le pas est grand que 1 : exemple N2 (Gestion des obstacles intermédiares possibles)

            elif pas > 1:
                i = robot_ligne_actuelle - 1
                collision = False
                while i > robot_ligne_nouvelle:
                    if self.grille[i][robot_colonne_actuelle] == "O":
                        collision = True
                        break
                    i -= 1

                if collision :
                    fin = True
                    message = message = Labyrinthe.MSG["C"]

                # Si passe par la sortie
                elif self.grille[robot_ligne_nouvelle][robot_colonne_nouvelle] == "U":
                    fin = True
                    message = message = Labyrinthe.MSG["F"]

                else:
                    self.gerer_lignes_deplacement_y(robot_ligne_actuelle,robot_colonne_actuelle,robot_ligne_nouvelle,robot_colonne_nouvelle)
                    fin = False
                    message = message = Labyrinthe.MSG["B"]
                    
            # Si le pas est 1

            else:
                # S'il y a collision
                if self.grille[robot_ligne_nouvelle][robot_colonne_nouvelle] == "O":
                    fin = True
                    message = message = Labyrinthe.MSG["C"]

                # Si passe par la sortie
                elif self.grille[robot_ligne_nouvelle][robot_colonne_nouvelle] == "U":
                    fin = True
                    message = message = Labyrinthe.MSG["F"]
                else:
                    self.gerer_lignes_deplacement_y(robot_ligne_actuelle,robot_colonne_actuelle,robot_ligne_nouvelle,robot_colonne_nouvelle)
                    fin = False
                    message = message = Labyrinthe.MSG["B"]

            

        # Si l'orientation est S : Sud        

        elif orientation == "S" :

            robot_ligne_nouvelle = robot_ligne_actuelle + pas
            robot_colonne_nouvelle = robot_colonne_actuelle

            # Si le déplacement amène le robot hors de la zone du labyrinthe
            if robot_ligne_nouvelle > len(self.grille) :
                fin = True
                message = message = Labyrinthe.MSG["H"]


            # Si le pas est grand que 1 : exemple S2 (Gestion des obstacles intermédiares possibles)

            elif pas > 1:
                i = robot_ligne_actuelle + 1
                collision = False
                while i < robot_ligne_nouvelle:
                    obstacle = self.grille[i][robot_colonne_actuelle]
                    if  obstacle == "O":
                        collision = True
                        break
                    i += 1

                if collision :
                    fin = True
                    message = message = Labyrinthe.MSG["C"]

                # S'il n'y a pas d'obstacles intermédiares

                # Si passe par la sortie
                elif self.grille[robot_ligne_nouvelle][robot_colonne_nouvelle] == "U":
                    fin = True
                    message = message = Labyrinthe.MSG["F"]

                else:
                    self.gerer_lignes_deplacement_y(robot_ligne_actuelle,robot_colonne_actuelle,robot_ligne_nouvelle,robot_colonne_nouvelle)
                    fin = False
                    message = message = Labyrinthe.MSG["B"]

            # Si le pas est 1

            else:
                # S'il y a collision
                if self.grille[robot_ligne_nouvelle][robot_colonne_nouvelle] == "O":
                    fin = True
                    message = message = Labyrinthe.MSG["C"]

                # Si passe par la sortie
                elif self.grille[robot_ligne_nouvelle][robot_colonne_nouvelle] == "U":
                    fin = True
                    message = message = Labyrinthe.MSG["F"]
                else:
                    self.gerer_lignes_deplacement_y(robot_ligne_actuelle,robot_colonne_actuelle,robot_ligne_nouvelle,robot_colonne_nouvelle)
                    fin = False
                    message = message = Labyrinthe.MSG["B"]





        # Si l'orientation est E : Est

        elif orientation == "E" :

            robot_ligne_nouvelle = robot_ligne_actuelle 
            robot_colonne_nouvelle = robot_colonne_actuelle + pas

            # Si le déplacement amène le robot hors de la zone du labyrinthe
            if robot_colonne_nouvelle > len(self.grille[0]) :
                fin = True
                message = message = Labyrinthe.MSG["H"]

            # Si le pas est grand que 1 : exemple E2 (Gestion des obstacles intermédiares possibles)

            elif pas > 1:
                i = robot_colonne_actuelle + 1
                collision = False
                while i < robot_colonne_nouvelle:
                    if  self.grille[robot_ligne_actuelle][i] == "O":
                        collision = True
                        break
                    i += 1

                if collision :
                    fin = True
                    message = message = Labyrinthe.MSG["C"]

                # Si passe par la sortie
                elif self.grille[robot_ligne_nouvelle][robot_colonne_nouvelle] == "U":
                    fin = True
                    message = message = Labyrinthe.MSG["F"]

                else:
                    self.gerer_ligne_deplacement_x(robot_ligne_actuelle,robot_colonne_actuelle,robot_ligne_nouvelle,robot_colonne_nouvelle)
                    fin = False
                    message = message = Labyrinthe.MSG["B"]
            # Si le pas est 1

            else:

                # S'il y a collision
                if self.grille[robot_ligne_nouvelle][robot_colonne_nouvelle] == "O":
                    fin = True
                    message = message = Labyrinthe.MSG["C"]

                # Si passe par la sortie
                elif self.grille[robot_ligne_nouvelle][robot_colonne_nouvelle] == "U":
                    fin = True
                    message = message = Labyrinthe.MSG["F"]
                else:
                    self.gerer_ligne_deplacement_x(robot_ligne_actuelle,robot_colonne_actuelle,robot_ligne_nouvelle,robot_colonne_nouvelle)
                    fin = False
                    message = message = Labyrinthe.MSG["B"]


        # Si l'orientation est O : Ouest           

        else:

            robot_ligne_nouvelle = robot_ligne_actuelle 
            robot_colonne_nouvelle = robot_colonne_actuelle - pas

            if robot_colonne_nouvelle < 0 :
                fin = True
                message = message = Labyrinthe.MSG["H"]

            # Si le pas est grand que 1 : exemple O2 (Gestion des obstacles intermédiares possibles)

            elif pas > 1:
                i = robot_colonne_actuelle - 1
                collision = False
                while i > robot_colonne_nouvelle:
                    if  self.grille[robot_ligne_actuelle][i] == "O":
                        collision = True
                        break
                    i -= 1

                if collision :
                    fin = True
                    message = message = Labyrinthe.MSG["C"]

                # Si passe par la sortie
                elif self.grille[robot_ligne_nouvelle][robot_colonne_nouvelle] == "U":
                    fin = True
                    message = message = Labyrinthe.MSG["F"]

                else:
                    self.gerer_ligne_deplacement_x(robot_ligne_actuelle,robot_colonne_actuelle,robot_ligne_nouvelle,robot_colonne_nouvelle)
                    fin = False
                    message = message = Labyrinthe.MSG["B"]
            # Si le pas est 1

            else:

                # S'il y a collision
                if self.grille[robot_ligne_nouvelle][robot_colonne_nouvelle] == "O":
                    fin = True
                    message = message = Labyrinthe.MSG["C"]

                # Si passe par la sortie
                elif self.grille[robot_ligne_nouvelle][robot_colonne_nouvelle] == "U":
                    fin = True
                    message = message = Labyrinthe.MSG["F"]
                else:
                    self.gerer_ligne_deplacement_x(robot_ligne_actuelle,robot_colonne_actuelle,robot_ligne_nouvelle,robot_colonne_nouvelle)
                    fin = False
                    message = message = Labyrinthe.MSG["B"]




        return fin, message

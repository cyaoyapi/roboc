# -*-coding:Utf-8 -*

"""Ce module contient la classe Labyrinthe."""

class Labyrinthe:

    """Classe représentant un labyrinthe."""

    def __init__(self, robot, obstacles):
        self.robot = robot
        self.grille = obstacles.split("\n")
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

        """Cette méthode permet de reconstruire les lignes impactées par le déplacement vertical(N et S) du robt"""
        
        robot_ligne_actuelle = int(robot_ligne_actuelle)
        robot_colonne_actuelle = int(robot_colonne_actuelle)
        robot_ligne_nouvelle = int(robot_ligne_nouvelle)
        robot_colonne_nouvelle = int(robot_colonne_nouvelle)

        # Gestion de l'apparence de la ligne actuelle après le déplacement du robot
        ligne_actuelle = self.grille[robot_ligne_actuelle]
        ligne_actuelle_2_list = list(ligne_actuelle)
        ligne_actuelle_2_list[robot_colonne_actuelle] = self.obstacle_anterieur
        ligne_actuelle = ("").join(ligne_actuelle_2_list)
        self.grille[robot_ligne_actuelle] = ligne_actuelle

        # Conserver l'obstacle actuelle de la zone que va occuper le robot après son déplacement
        self.obstacle_anterieur = self.grille[robot_ligne_nouvelle][robot_colonne_nouvelle]

        # Gestion de l'apparence de la ligne futur qui accueil le robot après son déplacement
        ligne_nouvelle = self.grille[robot_ligne_nouvelle]
        ligne_nouvelle_2_list = list(ligne_nouvelle)
        ligne_nouvelle_2_list[robot_colonne_nouvelle] = "X"
        ligne_nouvelle = ("").join(ligne_nouvelle_2_list)
        self.grille[robot_ligne_nouvelle] = ligne_nouvelle



    def gerer_ligne_deplacement_x(self,robot_ligne_actuelle, robot_colonne_actuelle,robot_ligne_nouvelle, robot_colonne_nouvelle ):

        """Cette méthode permet de reconstruire la ligne impactée par le déplacement horizontale(E et O) du robt"""
        
        robot_ligne_actuelle = int(robot_ligne_actuelle)
        robot_colonne_actuelle = int(robot_colonne_actuelle)
        robot_ligne_nouvelle = int(robot_ligne_nouvelle)
        robot_colonne_nouvelle = int(robot_colonne_nouvelle)

        # Gestion de l'apparence de la ligne actuelle après le déplacement du robot
        ligne_actuelle = self.grille[robot_ligne_actuelle]
        ligne_actuelle_2_list = list(ligne_actuelle)
        ligne_actuelle_2_list[robot_colonne_actuelle] = self.obstacle_anterieur

            # Conserver l'obstacle actuelle de la zone que va occuper le robot après son déplacement
        self.obstacle_anterieur = self.grille[robot_ligne_nouvelle][robot_colonne_nouvelle]

        ligne_actuelle_2_list[robot_colonne_nouvelle] = "X"
        ligne_actuelle = ("").join(ligne_actuelle_2_list)
        self.grille[robot_ligne_actuelle] = ligne_actuelle



    def deplacer_robot(self, choix):

        """Methode permettant de controler le deplacement du robot"""

        fin = False
        message = ""


        robot_ligne_actuelle, robot_colonne_actuelle = self.detecter_position_robot()

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
                message = "Désolé ! Vous êtes hors de la zone du labyrithe : vous avez perdu !"

            # Si le pas est grand que 1 : exemple N2 (Gestion des obstacles intermédiares possibles)

            elif pas > 1:
                i = robot_ligne_actuelle - 1
                collision = False
                while i < robot_ligne_nouvelle:
                    i += 1
                    if  self.grille[i][robot_colonne_actuelle] == "O":
                        collision = True
                        break
                if collision :
                    fin = True
                    message = "Désolé ! Collision avec un mur : Vous avez perdu !"

                # Si passe par la sortie
                elif self.grille[robot_ligne_nouvelle][robot_colonne_nouvelle] == "U":
                    fin = True
                    message = "Félicitations ! Vous avez gagné !"

                else:
                    self.gerer_lignes_deplacement_y(robot_ligne_actuelle,robot_colonne_actuelle,robot_ligne_nouvelle,robot_colonne_nouvelle)
                    fin = False
                    message = "Bravo ! Vous avancez bien  : Continuez !"
            # Si le pas est 1

            else:

                # Si passe par la sortie
                if self.grille[robot_ligne_nouvelle][robot_colonne_nouvelle] == "U":
                    fin = True
                    message = "Félicitations ! Vous avez gagné !"
                else:
                    self.gerer_lignes_deplacement_y(robot_ligne_actuelle,robot_colonne_actuelle,robot_ligne_nouvelle,robot_colonne_nouvelle)
                    fin = False
                    message = "Bravo ! Vous avancez bien : Continuez !"

            

        # Si l'orientation est S : Sud        

        elif orientation == "S" :

            robot_ligne_nouvelle = robot_ligne_actuelle + pas
            robot_colonne_nouvelle = robot_colonne_actuelle

            # Si le déplacement amène le robot hors de la zone du labyrinthe
            if robot_ligne_nouvelle > len(self.grille) :
                fin = True
                message = "Désolé ! Vous êtes hors de la zone du labyrithe : vous avez perdu !"


            # Si le pas est grand que 1 : exemple S2 (Gestion des obstacles intermédiares possibles)

            elif pas > 1:
                i = robot_ligne_actuelle + 1
                collision = False
                while i < robot_ligne_nouvelle:
                    obstacle = self.grille[i][robot_colonne_actuelle]
                    i += 1
                    if  obstacle == "O":
                        collision = True
                        break
                if collision :
                    fin = True
                    message = "Désolé ! Collision avec un mur : Vous avez perdu !"

                # S'il n'y a pas d'obstacles intermédiares

                # Si passe par la sortie
                elif self.grille[robot_ligne_nouvelle][robot_colonne_nouvelle] == "U":
                    fin = True
                    message = "Félicitations ! Vous avez gagné !"

                else:
                    self.gerer_lignes_deplacement_y(robot_ligne_actuelle,robot_colonne_actuelle,robot_ligne_nouvelle,robot_colonne_nouvelle)
                    fin = False
                    message = "Bravo ! Vous avancez bien  : Continuez !"

            # Si le pas est 1

            else:

                # Si passe par la sortie
                if self.grille[robot_ligne_nouvelle][robot_colonne_nouvelle] == "U":
                    fin = True
                    message = "Félicitations ! Vous avez gagné !"
                else:
                    self.gerer_lignes_deplacement_y(robot_ligne_actuelle,robot_colonne_actuelle,robot_ligne_nouvelle,robot_colonne_nouvelle)
                    fin = False
                    message = "Bravo ! Vous avancez bien  : Continuez !"





        # Si l'orientation est E : Est

        elif orientation == "E" :

            robot_ligne_nouvelle = robot_ligne_actuelle 
            robot_colonne_nouvelle = robot_colonne_actuelle + pas

            # Si le déplacement amène le robot hors de la zone du labyrinthe
            if robot_colonne_nouvelle > len(self.grille[0]) :
                fin = True
                message = "Désolé ! Vous êtes hors de la zone du labyrithe : vous avez perdu !"

            # Si le pas est grand que 1 : exemple E2 (Gestion des obstacles intermédiares possibles)

            elif pas > 1:
                i = robot_colonne_actuelle + 1
                collision = False
                while i < robot_colonne_nouvelle:
                    i += 1
                    if  self.grille[robot_ligne_actuelle][i] == "O":
                        collision = True
                        break
                if collision :
                    fin = True
                    message = "Désolé ! Collision avec un mur : Vous avez perdu !"

                # Si passe par la sortie
                elif self.grille[robot_ligne_nouvelle][robot_colonne_nouvelle] == "U":
                    fin = True
                    message = "Félicitations ! Vous avez gagné !"

                else:
                    self.gerer_ligne_deplacement_x(robot_ligne_actuelle,robot_colonne_actuelle,robot_ligne_nouvelle,robot_colonne_nouvelle)
                    fin = False
                    message = "Bravo ! Vous avancez bien : Continuez !"
            # Si le pas est 1

            else:

                # Si passe par la sortie
                if self.grille[robot_ligne_nouvelle][robot_colonne_nouvelle] == "U":
                    fin = True
                    message = "Félicitations ! Vous avez gagné !"
                else:
                    self.gerer_ligne_deplacement_x(robot_ligne_actuelle,robot_colonne_actuelle,robot_ligne_nouvelle,robot_colonne_nouvelle)
                    fin = False
                    message = "Bravo ! Vous avancez bien : Continuez !"


        # Si l'orientation est O : Ouest           

        else:

            robot_ligne_nouvelle = robot_ligne_actuelle 
            robot_colonne_nouvelle = robot_colonne_actuelle - pas

            if robot_colonne_nouvelle < 0 :
                fin = True
                message = "Désolé ! Vous êtes hors de la zone du labyrithe : vous avez perdu !"

            # Si le pas est grand que 1 : exemple O2 (Gestion des obstacles intermédiares possibles)

            elif pas > 1:
                i = robot_colonne_actuelle - 1
                collision = False
                while i < robot_colonne_nouvelle:
                    i += 1
                    if  self.grille[robot_ligne_actuelle][i] == "O":
                        collision = True
                        break
                if collision :
                    fin = True
                    message = "Désolé ! Collision avec un mur : Vous avez perdu !"

                # Si passe par la sortie
                elif self.grille[robot_ligne_nouvelle][robot_colonne_nouvelle] == "U":
                    fin = True
                    message = "Félicitations ! Vous avez gagné !"

                else:
                    self.gerer_ligne_deplacement_x(robot_ligne_actuelle,robot_colonne_actuelle,robot_ligne_nouvelle,robot_colonne_nouvelle)
                    fin = False
                    message = "Bravo ! Vous avancez bien : Continuez !"
            # Si le pas est 1

            else:

                # Si passe par la sortie
                if self.grille[robot_ligne_nouvelle][robot_colonne_nouvelle] == "U":
                    fin = True
                    message = "Félicitations ! Vous avez gagné !"
                else:
                    self.gerer_ligne_deplacement_x(robot_ligne_actuelle,robot_colonne_actuelle,robot_ligne_nouvelle,robot_colonne_nouvelle)
                    fin = False
                    message = "Bravo ! Vous avancez bien : Continuez !"




        return fin, message

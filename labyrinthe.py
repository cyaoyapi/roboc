# -*-coding:Utf-8 -*

"""Ce module contient la classe Labyrinthe."""

class Labyrinthe:

    """Classe représentant un labyrinthe."""


    # Définition d'une constante de classe pour la gestion des messages utilisateurs

    MSG = {
        "H":"Désolé ! Vous êtes hors de la zone du labyrithe : vous avez perdu !\n",
        "C":"Désolé ! Collision avec un mur : Vous avez perdu !\n",
        "B": "Bravo ! Vous avancez bien  : Continuez !\n",
        "F": "Félicitations ! Vous avez gagné !\n"

    }

    #################################################

    def __init__(self, robot, contenu):
        self.robot = robot

        # On construit la grille du Labyrinthe à partir du contenu du fichier(carte)
        self.grille = contenu.split("\n") 

        # prend la valeur de l'obstacle avant de le remplacer par le robot
        # utile pour l'affiche quand le robot quitte a nouveau cette position
        self.obstacle_anterieur = " "  


    #################################################

    def afficher(self):

    	"""Méthode affichant le labyrinthe"""

    	for ligne in self.grille:
    		print(ligne)


    #################################################

    def detecter_position_robot(self):

    	"""Méthode retournant les coordonnées du robot"""

    	robot_x = 0 # ligne du sur laquelle le robot se trouve
    	for ligne in self.grille:
    		if self.robot in ligne:
    			robot_y = ligne.find(self.robot) # colonne sur laquelle le robot se trouve
    			break
    		else:
    			robot_x += 1
    			continue

    	return [robot_x,robot_y]


    

    #################################################

    def obstacles_intermediaires(self,sens, robot_x, robot_y, robot_x_new, robot_y_new):

        """Cette méthode vérifie s'il y a des obstacles intermédiaires dans le cas ou le pas > 1 (exemple O3; E2; ...)

            - sens : orientation de deplacement
            - robot_x : ligne actuelle où se trouve le 
            - robot_y : colonne colonne où se trouve le robot
            - robot_x_new : nouvelle ligne où va se retrouver le robot après deplacement
            - robot_y_new : nouvelle colonne où va se retrouver le robot après deplacement
            
            Cette méthode est appelée dans la méthode 'deplacement_dans_labyrinthe'

        """

        collision = False # un boolean que drapeau du détecter une collision

        # On test les obstacles intermédiares pour voir si il y a collision

        if sens == "N":
            i = robot_x - 1
            while i >= robot_x_new:
                if self.grille[i][robot_y] == "O":
                    collision = True
                    break
                i -= 1
        elif sens == "S":
            i = robot_x + 1
            while i <= robot_x_new:
                if  self.grille[i][robot_y] == "O":
                    collision = True
                    break
                i += 1

        elif sens == "E":
            i = robot_y + 1
            while i <= robot_y_new:
                if  self.grille[robot_x][i] == "O":
                    collision = True
                    break
                i += 1
        else :
            i = robot_y - 1
            while i >= robot_y_new:
                if  self.grille[robot_x][i] == "O":
                    collision = True
                    break
                i -= 1
        # s'il y a collision avec un mur 
                
        if collision:
            return True
            
           
        
    #################################################

    def gerer_lignes_deplacement_y(self,robot_x, robot_y,robot_x_new, robot_y_new):

        """Cette méthode permet de reconstruire les lignes impactées par un déplacement vertical(Nord ou Sud) du robt
            
            - robot_x : ligne actuelle où se trouve le 
            - robot_y : colonne colonne où se trouve le robot
            - robot_x_new : nouvelle ligne où va se retrouver le robot après deplacement
            - robot_y_new : nouvelle colonne où va se retrouver le robot après deplacement
            
            Deux lignes sont impactées lors d'un déplacement verticale :
            - Celle la ligne actuelle
            - Et la la ligne future (nouvelle)

            Cette méthode est appelée dans la méthode 'deplacement_dans_labyrinthe'

        """
        
        robot_x = int(robot_x)
        robot_y = int(robot_y)
        robot_x_new = int(robot_x_new)
        robot_y_new = int(robot_y_new)

        # Gestion de l'apparence de la ligne actuelle après le déplacement du robot
        ligne_x = self.grille[robot_x]
        ligne_x_to_list = list(ligne_x) # On transforme la ligne(chaine de caractères) en liste(objet mutable)
        ligne_x_to_list[robot_y] = self.obstacle_anterieur
        ligne_x = ("").join(ligne_x_to_list) # On reconstruire la chaine de caractère à partir de la liste modifiée
        self.grille[robot_x] = ligne_x

        # Conserver l'obstacle actuelle de la zone que va occuper le robot après son déplacement
        self.obstacle_anterieur = self.grille[robot_x_new][robot_y_new]

        # Gestion de l'apparence de la ligne futur qui accueil le robot après son déplacement
        ligne_x_new = self.grille[robot_x_new]
        ligne_x_new_to_list = list(ligne_x_new) # On transforme la ligne(chaine de caractères) en liste(objet mutable)
        ligne_x_new_to_list[robot_y_new] = "X"
        ligne_x_new = ("").join(ligne_x_new_to_list) # On reconstruire la chaine de caractère à partir de la liste modifiée
        self.grille[robot_x_new] = ligne_x_new


    


    #################################################

    def gerer_ligne_deplacement_x(self,robot_x, robot_y,robot_x_new, robot_y_new):

        """Cette méthode permet de reconstruire la ligne impactées par un déplacement horizontal(Est ou Ouest) du robot
            - robot_x : ligne actuelle où se trouve le 
            - robot_y : colonne colonne où se trouve le robot
            - robot_x_new : nouvelle ligne où va se retrouver le robot après deplacement
            - robot_y_new : nouvelle colonne où va se retrouver le robot après deplacement

            Une seule ligne est impactée, la ligne actuelle, seule les colonnes d'origine et d'arrivée change
            
            Cette méthode est appelée dans la méthode 'deplacement_dans_labyrinthe'

        """
        
        robot_x = int(robot_x)
        robot_y = int(robot_y)
        robot_x_new = int(robot_x_new)
        robot_y_new = int(robot_y_new)

        # Gestion de l'apparence de la ligne actuelle après le déplacement du robot
        ligne_x = self.grille[robot_x]
        ligne_x_to_list = list(ligne_x) # On transforme la ligne(chaine de caractères) en liste(objet mutable)
        ligne_x_to_list[robot_y] = self.obstacle_anterieur

            # Conserver l'obstacle actuelle de la zone que va occuper le robot après son déplacement
        self.obstacle_anterieur = self.grille[robot_x_new][robot_y_new]

        ligne_x_to_list[robot_y_new] = "X"
        ligne_x = ("").join(ligne_x_to_list) # On reconstruire la chaine de caractère à partir de la liste modifiée
        self.grille[robot_x] = ligne_x



    #################################################

    def deplacement_hors_labyrinthe(self, sens, robot_x_new, robot_y_new):

        """Cette méthode determine si le de placement voulu est hors dela zone du layrinthe

            - sens : orientation de deplacement
            - robot_x_new : nouvelle ligne où va se retrouver le robot après deplacement
            - robot_y_new : nouvelle colonne où va se retrouver le robot après deplacement
            
            Cette méthode est appelée dans la méthode 'deplacer_robot'
            
        """
        
        if (sens == "N" and robot_x_new < 0) or \
           (sens == "S" and robot_x_new >= len(self.grille)) or \
           (sens == "E" and robot_y_new >= len(self.grille[0])) or \
           (sens == "O" and robot_y_new < 0) :

           return True


    #################################################

    def deplacement_dans_labyrinthe(self,sens,pas,robot_x,robot_y,robot_x_new, robot_y_new):

        """Cette méthode gère un déplcament dans la zone des limites du labyrinthe
            - sens : orientation du déplacement 
            - robot_x : ligne actuelle où se trouve le 
            - robot_y : colonne colonne où se trouve le robot
            - robot_x_new : nouvelle ligne où va se retrouver le robot après deplacement
            - robot_y_new : nouvelle colonne où va se retrouver le robot après deplacement
            
            Deux cas :
            - pas > 1
            - et pas = 1

            Cette méthode faire appel aux méthodes :

            - 'obstacles_intermediaires'
            - 'gerer_lignes_deplacement_y'
            - et 'gerer_ligne_deplacement_x'

            Elle est elle même appelée dans 'deplacer_robot'

        """


        fin = False
        message = ""

        # gérer le cas des collisions selon le pas (Si le robot passe par "O")

        if (pas > 1 and self.obstacles_intermediaires(sens,robot_x,robot_y,robot_x_new,robot_y_new)) or\
           (pas == 1 and self.grille[robot_x_new][robot_y_new] == "O"):
            
            return True, Labyrinthe.MSG["C"]

        
        # Si le robot passe par la sortie ("U")
        elif self.grille[robot_x_new][robot_y_new] == "U":
            return True, Labyrinthe.MSG["F"]

        else:
            if sens in ["N","S"]:
                self.gerer_lignes_deplacement_y(robot_x,robot_y,robot_x_new,robot_y_new)
            else :
                self.gerer_ligne_deplacement_x(robot_x,robot_y,robot_x_new,robot_y_new)
            
            return False, Labyrinthe.MSG["B"]

            

    #################################################

    def deplacer_robot(self, choix):

        """Methode permettant de controler le deplacement du robot
            
            Elle retourne 2 paramètres :

            - fin (Boolean) : Qui inqique si on continue le jeu(False) ou si on arrête(True)
            - message : Un message explicite à l'endroit de l'utilisateur

            Elle utilise les méthodes :

            - 'detecter_position_robot'
            - 'deplacement_hors_labyrinthe'
            -et 'deplacement_dans_labyrinthe'

        """

        fin = False
        message = ""

        # on recupère les coordonnées(la position) actuelles du robot

        robot_x, robot_y = self.detecter_position_robot()

        # On détermine l'orientation(sens) du déplacement et le pas à partir du choix
        
        if len(choix) == 1 :
            sens = choix[0]
            pas = 1
        else :
            sens = choix[0]
            pas = int(choix[1:])


    	# Si l'orientation de déplacement est le N : Nord

        if sens == "N" :

            robot_x_new = robot_x - pas
            robot_y_new= robot_y

            # Si le robot est hors de la zone du labyrinthe
            if self.deplacement_hors_labyrinthe("N",robot_x_new,robot_y_new) :
                fin = True
                message = message = Labyrinthe.MSG["H"]

            # Si le déplacement est dans la zone du labyrinthe
            else:
                fin, message = self.deplacement_dans_labyrinthe("N",pas,robot_x,robot_y,robot_x_new,robot_y_new)
                
                

        # Si l'orientation est S : Sud        

        elif sens == "S" :

            robot_x_new = robot_x + pas
            robot_y_new = robot_y

            # Si le robot est hors de la zone du labyrinthe
            if self.deplacement_hors_labyrinthe("S",robot_x_new,robot_y_new) :
                fin = True
                message = message = Labyrinthe.MSG["H"]


            # Si le déplacement est dans la zone du labyrinthe
            else:
                fin, message = self.deplacement_dans_labyrinthe("S",pas,robot_x,robot_y,robot_x_new,robot_y_new)
                


        # Si l'orientation est E : Est

        elif sens == "E" :

            robot_x_new = robot_x 
            robot_y_new = robot_y + pas

            # Si le robot est hors de la zone du labyrinthe
            if self.deplacement_hors_labyrinthe("E",robot_x_new,robot_y_new) :
                fin = True
                message = message = Labyrinthe.MSG["H"]

            # Si le déplacement est dans la zone du labyrinthe
            else:
                fin, message = self.deplacement_dans_labyrinthe("S",pas,robot_x,robot_y,robot_x_new,robot_y_new)
                

        # Si l'orientation est O : Ouest           

        else:

            robot_x_new = robot_x 
            robot_y_new = robot_y - pas

            # Si le robot est hors de la zone du labyrinthe
            if self.deplacement_hors_labyrinthe("O",robot_x_new,robot_y_new) :
                fin = True
                message = message = Labyrinthe.MSG["H"]

            # Si le déplacement est dans la zone du labyrinthe
            else:
                fin, message = self.deplacement_dans_labyrinthe("O",pas,robot_x,robot_y,robot_x_new,robot_y_new)



        return fin, message

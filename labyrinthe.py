# -*-coding:Utf-8 -*

"""Ce module contient la classe Labyrinthe."""

import os
import random ## Module pour faire du pseudo aléatoire
import re # Module pour la gestion des expressions regulières

from obstacle.vide import Vide
from obstacle.mur import Mur
from obstacle.porte import Porte
from obstacle.sortie import Sortie
from joueur import Joueur

# On importe le module personnalisé utils qui regroupe des objets utilitaires
import utils

class Labyrinthe:

    """Classe représentant un labyrinthe.
    
    Elle contient :

    * Des constantes :
        - MSG : dictionnaires de messages utilisateurs
        - REGEX1 et REGEX2 : motifs d'expressions regulièrement pour la validation des saisies utilisateurs

    * Les méthodes :

        - 'generer_contenu' : générant le contenu du labyrinthe sous forme de chaine de caractères
        - 'generer_postion_libre' : générant une position aléatoire libre sur le labyrinthe
        - 'obstacles_intermediaires' : Teste s'il y a pas d'obstacles intermédiares pour un déplacement de pas > 1
        - 'gerer_lignes_deplacement_y': gère la reconstruction des lignes imapctées en cas de déplacement verticale (N et S)
        - 'gerer_ligne_deplacement_x': gère la reconstruction de la ligne impactée en cas de déplacement horizontale (O et E)
        - 'deplacement_hors_labyrinthe' : Teste si le déplacement n'est pas hors des limites du labyrinthe
        - 'deplacement_dans_labyrinthe' : gère le dplacement quand on est dans des limites du labyrinthe
        - 'routine_deplacement' : routine utilisée dans la méthode principale de déplacement "deplacer_robot"
        - 'declencher_action' : permet soit de murer une porte ou de trouer un mur
        - 'deplacer_robot' : méthode principale qui gère le déplacement d'un robot

    """


    # Définition d'une constante de classe pour la gestion des messages utilisateurs

    MSG = {
        "H":"Attention, deplacement impossible! Vous allez hors de la zone du labyrithe.\n",
        "C":"Attention, deplacement impossible!\nCollision avec un obstacle infranchissable ou un joueur !\n",
        "B": "Bien joué, Vous avancez bien !\n",
        "M": "Bien joué ! Vous venez de murer une porte !\n",
        "MI": "Attention ! Action impossible. Vous ne pouvez murer qu'une porte(.)\n",
        "P": "Bien joué ! Vous venez de trouer un mur !\n",
        "PI": "Attention ! Action impossible. Vous ne pouvez trouer qu'un mur(O)\n",
        "F": "Félicitations ! Vous avez gagné la partie \n",
    }

    REGEX1 = r"^[NESO]([1-9][0-9]*)*$" # Motif de choix valide de déplacement du robot
    REGEX2 = r"^[MP]([NESO]$" # Motif de choix valide de déplacement du robot


    #################################################

    def __init__(self, contenu):

    	""" Constructeur d'un labyrinthe."""

    	contenu = contenu.split("\n") # transforme le contenu(chaine) en liste

    	self.joueurs = []  # La liste des joueurs de ce labyrinthe

    	# dictionnaire de symboles d'obstacles

    	symboles = {
    		" ": Vide,
    		"O": Mur,
    		".": Porte,
    		"U": Sortie,
    		"X": Joueur
    	}
    	
    	i = 0
    	self.grille = []  # la grille du la byrinthe : une liste de listes ([[],[],[]...[]])
    	
    	for ligne in contenu:
    		
    		j = 0
    		liste_ligne = [] # d'une chaine (ligne), on aura une liste d'objets(filles) obstacles
    		
    		for caractere in ligne:
    			classe_obstacle = symboles[caractere.upper()] # On recupère la classe de l'obstacle en fonction du caracrtère depuis le dictionnaire 'symboles'
    			obstacle = classe_obstacle(i,j) # on créer l'objet(fille) obstacle
    			liste_ligne.append(obstacle) # on l'ajoute à la liste(ligne)
    			j += 1 # On passe au caractère suivant

    		self.grille.append(liste_ligne) # On joute la nouvelle ligne à la grille
    		i += 1 # On passe à la ligne suivante



    #################################################

    def generer_postion_libre(self):

        """Méthode permettant de générer une position aléatoire libre pour un nouveau joueur"""

        i = 0
        liste_vides = [] # Liste des espaces vides (Une liste de tuple(x,y))
        
        for liste_ligne in self.grille:
            
            j = 0
            for obstacle in liste_ligne:
                if obstacle.symbole == " ":
                    couple = (i,j)
                    liste_vides.append(couple)
                j += 1
            i += 1

        vide_choisi = random.choice(liste_vides)

        return vide_choisi[0], vide_choisi[1] 




    #################################################

    def generer_contenu(self, joueur_encours):

    	"""Méthode permettant de générer le contenu du labyrinthe sous forme de chaine de caractères

            Cette permet de générer un affichage personnalisé du 
            Labyrinthe sur l'interface d'un joueur :
            - Son robot apparait en grand X
            - les autres robots en petit x

        """


    	contenu = ""
    	for liste_ligne in self.grille:

    		j = 0
    		ligne =[]
    		for obstacle in liste_ligne:
    			if (obstacle in self.joueurs) and (obstacle is not joueur_encours):
    				ligne.append(obstacle.symbole.lower())
    			else:
    				ligne.append(obstacle.symbole)
    			j += 1
    			if j == len(liste_ligne):
    				ligne.append("\n")
    				break

    		ligne = ("").join(ligne) # On reconstruire la chaine à afficher à partir de la liste
    		contenu += ligne

    	return contenu


    


    #################################################

    def obstacles_intermediaires(self, sens, x, y, x_new, y_new):

        """Cette méthode vérifie s'il y a des obstacles intermédiaires dans le cas ou le pas > 1 (exemple O3; E2; ...)

            - sens : orientation de deplacement
            - x : ligne actuelle où se trouve le robot
            - y : colonne colonne où se trouve le robot
            - x_new : nouvelle ligne où va se retrouver le robot après deplacement
            - y_new : nouvelle colonne où va se retrouver le robot après deplacement
            
            Cette méthode est appelée dans la méthode 'deplacement_dans_labyrinthe'
            
            Elle return un boolean 'collision'

        """

        x = int(x)
        y = int(y)
        x_new = int(x_new)
        y_new = int(y_new)

        collision = False # un boolean comme drapeau pour détecter une collision

        # On test les obstacles intermédiares pour voir si il y a collision

        if sens == "N":
            i = x - 1
            while i >= x_new:
                if not self.grille[i][y].peut_traverser :
                    collision = True
                    break
                i -= 1
        elif sens == "S":
            i = x + 1
            while i <= x_new:
                if not self.grille[i][y].peut_traverser :
                    collision = True
                    break
                i += 1

        elif sens == "E":
            i = y + 1
            while i <= y_new:
                if not self.grille[x][i].peut_traverser :
                    collision = True
                    break
                i += 1
        else :
            i = y - 1
            while i >= y_new:
                if not self.grille[x][i].peut_traverser :
                    collision = True
                    break
                i -= 1
        
        # On retourne la valeur de collision
        return collision
            


    #################################################

    def gerer_lignes_deplacement_y(self, num_tour, x, y, x_new, y_new):

        """Cette méthode permet de reconstruire les lignes impactées par un déplacement vertical(Nord ou Sud) du robt
            
            - x : ligne actuelle où se trouve le 
            - y : colonne colonne où se trouve le robot
            - x_new : nouvelle ligne où va se retrouver le robot après deplacement
            - y_new : nouvelle colonne où va se retrouver le robot après deplacement
            
            Deux lignes sont impactées lors d'un déplacement verticale :
            - la ligne actuelle
            - Et la la ligne future (nouvelle)

            Cette méthode est appelée dans la méthode 'deplacement_dans_labyrinthe'

        """
        
        x = int(x)
        y = int(y)
        x_new = int(x_new)
        y_new = int(y_new)

        self.joueurs[num_tour].x = x_new
        self.joueurs[num_tour].y = y_new

        # Gestion de l'apparence de la ligne actuelle après le déplacement du robot
        ligne_liste_x = self.grille[x]
        ligne_liste_x[y] = self.joueurs[num_tour].obstacle_anterieur
        self.grille[x] = ligne_liste_x

        # Conserver l'obstacle actuelle de la zone que va occuper le robot après son déplacement
        self.joueurs[num_tour].obstacle_anterieur = self.grille[x_new][y_new]

        # Gestion de l'apparence de la ligne futur qui accueil le robot après son déplacement
        ligne_liste_x_new = self.grille[x_new]
        ligne_liste_x_new[y_new] = self.joueurs[num_tour]
        self.grille[x_new] = ligne_liste_x_new


    


    #################################################

    def gerer_ligne_deplacement_x(self, num_tour, x, y, x_new, y_new):

        """Cette méthode permet de reconstruire la ligne impactée par un déplacement horizontal(Est ou Ouest) du robot
            - x : ligne actuelle où se trouve le 
            - y : colonne colonne où se trouve le robot
            - x_new : nouvelle ligne où va se retrouver le robot après deplacement
            - y_new : nouvelle colonne où va se retrouver le robot après deplacement

            Une seule ligne est impactée, la ligne actuelle, seule les colonnes d'origine et d'arrivée changent
            
            Cette méthode est appelée dans la méthode 'deplacement_dans_labyrinthe'

        """
        
        x = int(x)
        y = int(y)
        x_new = int(x_new)
        y_new = int(y_new)
        self.joueurs[num_tour].x = x_new
        self.joueurs[num_tour].y = y_new

        # Gestion de l'apparence de la ligne actuelle après le déplacement du robot
        ligne_liste_x = self.grille[x]
        ligne_liste_x[y] = self.joueurs[num_tour].obstacle_anterieur

            # Conserver l'obstacle actuelle de la zone que va occuper le robot après son déplacement
        self.joueurs[num_tour].obstacle_anterieur = self.grille[x_new][y_new]

        ligne_liste_x[y_new] = self.joueurs[num_tour]
        self.grille[x] = ligne_liste_x






    #################################################

    def deplacement_hors_labyrinthe(self, sens, x_new, y_new):

        """Cette méthode determine si le de placement voulu est au-dela de la zone du layrinthe

            - sens : orientation de deplacement
            - x_new : nouvelle ligne où va se retrouver le robot après deplacement
            - y_new : nouvelle colonne où va se retrouver le robot après deplacement
            
            Cette méthode est appelée dans la méthode 'deplacer_robot'
            
        """
        
        if (sens == "N" and x_new < 0) or \
           (sens == "S" and x_new >= len(self.grille)) or \
           (sens == "E" and y_new >= len(self.grille[0])) or \
           (sens == "O" and y_new < 0) :

           return True



    #################################################

    def deplacement_dans_labyrinthe(self,sens,pas,num_tour,x,y,x_new,y_new):

        """Cette méthode gère un déplcament dans la zone des limites du labyrinthe.

            - sens : orientation du déplacement 
            - pas : le pas
            - num_tour = le numéro du joueur
            - x : ligne actuelle où se trouve le robot
            - y : colonne colonne où se trouve le robot
            - x_new : nouvelle ligne où va se retrouver le robot après deplacement
            - y_new : nouvelle colonne où va se retrouver le robot après deplacement
            
            Deux cas :
            - pas > 1
            - et pas = 1

            Cette méthode faire appel aux méthodes :

            - 'obstacles_intermediaires'
            - 'gerer_lignes_deplacement_y'
            - 'gerer_ligne_deplacement_x'

            Elle est elle même appelée dans 'routine_deplacement'

        """


        # gérer le cas des collisions selon le pas (Si le robot passe par un obtacle infranchissable ou un autre joueur)

        if (pas > 1 and self.obstacles_intermediaires(sens,x,y,x_new,y_new)) or\
           (pas == 1 and not self.grille[x_new][y_new].peut_traverser):
            
            return False, Labyrinthe.MSG["C"]

        
        else:
            # Si on arrive à une sortie , il faut retourner fin = True
            if self.grille[x_new][y_new].nom == "sortie":

                if sens in ["N","S"]:
                    self.gerer_lignes_deplacement_y(num_tour,x,y,x_new,y_new)
                else :
                    self.gerer_ligne_deplacement_x(num_tour,x,y,x_new,y_new)
                
                return True, Labyrinthe.MSG["F"]

            else:

                if sens in ["N","S"]:
                    self.gerer_lignes_deplacement_y(num_tour,x,y,x_new,y_new)
                else :
                    self.gerer_ligne_deplacement_x(num_tour,x,y,x_new,y_new)
                
                return False, Labyrinthe.MSG["B"]

            


    ################################################


    def routine_deplacement(self,sens,pas,num_tour,x,y,x_new,y_new):

        """Methode est une routine appelé lors du déplacement 

            - sens : orientation du déplacement 
            - pas : le pas de déplacement
            - num_tour = le numéro du joueur
            - x : ligne actuelle où se trouve le robot
            - y : colonne colonne où se trouve le robot
            - x_new : nouvelle ligne où va se retrouver le robot après deplacement
            - y_new : nouvelle colonne où va se retrouver le robot après deplacement
            
            
            Elle retourne 2 paramètres :

            - fin (Boolean) : Qui inqique si on continue le jeu(False) ou si on arrête(True)
            - message : Un message explicite à l'endroit de l'utilisateur

            Elle utilise les méthodes :

            - 'deplacement_hors_labyrinthe'
            - 'deplacement_dans_labyrinthe'

            Elle est elle même appelée dans 'deplacer_robot'

        """
        fin = False
        msg_a_envoyer = ""

        # Si le déplacement est hors de la zone du labyrinthe
        if self.deplacement_hors_labyrinthe(sens,x_new,y_new) :
            fin = False
            msg_a_envoyer = Labyrinthe.MSG["H"]

        # Si le déplacement est dans la zone du labyrinthe
        else:
            fin, msg_a_envoyer = self.deplacement_dans_labyrinthe(sens,pas,num_tour,x,y,x_new,y_new)
                
        return fin, msg_a_envoyer


            
    ################################################



    def declencher_action(self, action, x_new, y_new):

        """ Cette méthode permet de réaliser soit de murer une porte ou trouer un mur;

            - action : action à réaliser soit M(Murer une porte) ou P(Trouer un mur) 
            - x_new : la ligne de l'élément sur lequel on peut mener l'action
            - y_new : la colonne de l'élément sur lequel on peut mener l'action
            

            Elle est appelée dans la méthode 'deplacer_robot'

        """

        # Si on veut murer une porte 
        if action == "M":

            if self.grille[x_new][y_new].nom == "porte":

                mur = Mur(x_new,y_new)
                self.grille[x_new][y_new] = mur
                return False, Labyrinthe.MSG["M"] 
            else:

                return False, Labyrinthe.MSG["MI"] 
            
        # Si on veut trouer un mur               
        else:

            if self.grille[x_new][y_new].nom == "mur":

                porte = Porte(x_new,y_new)
                self.grille[x_new][y_new] = porte
                return False, Labyrinthe.MSG["P"]
            else:
                return False, Labyrinthe.MSG["PI"]





    #################################################

    def deplacer_robot(self, num_tour, msg_recu):

        """Methode permettant de controler le deplacement du robot
            


            Elle retourne 2 paramètres :

            - fin (Boolean) : Qui inqique si on continue le jeu(False) ou si on arrête(True)
            - message : Un message explicite à l'endroit de l'utilisateur

            Elle utilise les méthodes :

            - 'routine_deplacement'
            - 'declencher_action'
            - et la fonction : utils.determiner_nouvelle_position (du module personalisé utils)

        """

        fin = False
        msg_a_envoyer = ""

        # on recupère les coordonnées(la position) actuelles du joueur(robot)
        x, y = self.joueurs[num_tour].x, self.joueurs[num_tour].y

        # Deplacement normal N, S, E, O
        if re.match(Labyrinthe.REGEX1, msg_recu) is not None:

            # On détermine l'orientation(sens) du déplacement et le pas à partir du choix
        
            if len(msg_recu) == 1 :
                sens = msg_recu[0]
                pas = 1
            else :
                sens = msg_recu[0]
                pas = int(msg_recu[1:])

            # On détermine les coordonnées de la position où le joueur veut se déplacer
            x_new, y_new = utils.determiner_nouvelle_position(sens,pas,x,y)

            fin, msg_a_envoyer = self.routine_deplacement(sens,pas,num_tour,x,y,x_new,y_new)


        # Murer(M) une porte ou Percer(P) un mur
        else:

            action = msg_recu[0]
            sens = msg_recu[1]
            pas = 1

            # On détermine la position de l'élément sur lequel va porter l'action
            x_new, y_new = utils.determiner_nouvelle_position(sens,pas,x,y)

            # On déclenche l'action
            fin, msg_a_envoyer = self.declencher_action(action,x_new,y_new)


        # A la fin de cette methode 'deplacer_robot', on retourne 'fin' et 'message'        
        return fin, msg_a_envoyer



   
    	
from obstacle.obstacle import Obstacle

class Vide(Obstacle):

    """Classe représentant un vide, un obstacle passable."""

    peut_traverser = True
    nom = "vide"
    symbole = " "
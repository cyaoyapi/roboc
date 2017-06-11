############# ROBOC Client-Serveur Muliti-joueurs #######################

Votre mission est de reprendre le code du labyrinthe développé à la partie précédente : Roboc. Vous devrez y ajouter les fonctionnalités suivantes :

    On ne doit plus jouer au jeu en console. À la place, le jeu doit être une application serveur. Il faut également créer les applications clients pour jouer à plusieurs au labyrinthe. Chaque joueur aura son propre robot. Au lieu de le placer à un endroit précis sur la carte, il apparaîtra aléatoirement ;
    Le jeu multi-joueurs se jouera au tour par tour, chaque robot faisant un seul mouvement par tour. Le joueur pourra toujours demander au robot d'aller trois fois vers l'est, par exemple, mais le jeu ne fera bouger le robot qu'une fois avant de demander le coup de l'autre joueur ;
    Le jeu doit inclure une série de tests unitaires qui permettront de valider son fonctionnement. Les tests doivent vérifier la constitution d'un labyrinthe standard, la création d'un labyrinthe depuis une chaîne et les fonctionnalités du jeu multi-joueurs ;
    Les robots peuvent maintenant murer des portes (changer une porte en mur) ou percer une porte dans un mur. Pour ces deux fonctionnalités, il faudra créer deux nouvelles commandes, voir le détail plus bas.

 
Contrôle du robot

Le système est un peu plus compliqué en interne, mais en pratique c'est la même chose : le client peut envoyer des commandes au serveur pour déplacer le robot. Les commandes sont identiques pour se déplacer. On ajoute également :

    La commande m pour murer une porte suivie de la lettre représentant la direction. Par exemple, la commande me demandra au robot de murer la porte qui se trouve juste à côté à l'est. Murer transforme tout simplement une porte en mur, piégant le robot adverse dans la pièce, temporairement du moins ;
    La commande p pour percer une porte dans un mur. Cette commande est également suivie de la lettre représentant la direction. Par exemple pn crée une porte dans le mur se trouvant juste au nord.

 
Affichage du labyrinthe

L'affichage doit être identique. Cette fois, c'est le serveur qui gère réellement les déplacements et commandes et qui envoie le nouveau labyrinthe au client après avoir joué. Le serveur doit envoyer le nouveau labyrinthe à tous les clients pour que chacun voie les coups des adversaires. Vous pourrez voir un extrait de console (du serveur et d'un client) plus bas.

Notez cependant qu'il y a une différence, puisque plusieurs robots doivent être visibles dans le labyrinthe. Il vous faut trouver un moyen de différencier son propre robot de ceux des adversaires.
 
Fonctionnalités du jeu

Les fonctionnalités du jeu sont identiques à celles proposées dans la version précédente, hormis les modifications indiquées. Notez cependant que, cette fois-ci, il n'est pas utile d'enregistrer les parties : les rejouer demandrait que tous les clients se reconnectent et ce serait un peu difficile à gérer.
 
Au lancement du programme

On doit lancer le serveur en premier. On doit préciser la carte (comme on le faisait auparavant) dans le serveur. Une fois la carte choisie, les clients peuvent se connecter.

Le ou les client(s) doi(ven)t être lancé(s) une fois la carte sélectionnée. Un nouveau robot sera créé automatiquement et placé dans le labyrinthe pour chaque client qui se connecte tant que la partie n'a pas commencé. Notez que des cartes indépendantes pourront être proposées par la suite, mais ce n'est pas dans la liste de vos objectifs actuels.

Chaque robot sera placé aléatoirement sur la carte : pour ce faire, le plus simple est de sélectionner aléatoirement une case vide (sans obstacle ni autre robot déjà placé). Notez que cela pourra donner des parties assez courtes, si un robot est placé aléatoirement tout près d'une sortie. Là encore, il pourra être utile par la suite de faire en sorte que le placement soit relativement équilibré, mais ce n'est pas nécessaire pour l'heure.

Enfin, quand suffisamment de clients se sont connectés, n'importe quel client pourra entrer la commande c pour commencer la partie. Cette commande ne pourra être utilisée qu'une fois. Une fois la partie commencée, de nouveaux clients ne pourront pas s'y joindre.
 
Petite précision côté client

Le client est un peu plus difficile à mettre en place dans le sens où il doit à la fois demander au joueur d'entrer des commandes et écouter le serveur pour des réponses. En théorie, il est possible de ne demander des commandes à l'utilisateur que quand son tour est venu de jouer. En pratique, cela est peu souhaitable et vous pourriez à terme mettre en place des commandes spécifiques (par exemple pour parler à tous les joueurs de la partie). Ce type de commande n'a pas besoin d'attendre le tour du joueur.

Pour attendre à la fois des commandes de l'utilisateur et écouter les réponses du serveur, il peut être utile d'utiliser la programmation parallèle. Ce n'est pas la seule solution mais c'est celle qui reste la plus expliquée dans ce cours. Libre à vous d'implémenter cette fonctionnalité autrement si vous le désirez.
 
Vous serez notés sur

    Le fait d'arriver à développer les fonctionnalités de l'exercice : si l'on peut lancer vos programmes (serveur et client) et qu'ils tournent sans modification, vous aurez la note maximale, peu importe le code source derrière ;
    La lisibilité du code : votre code source doit être aussi agréable à lire que possible. Les noms de vos variables, fonctions, classes, modules doivent être cohérents. La présentation de votre code source ne suit pas une règle spécifique, mais elle doit être cohérente (si vous faite un choix de nommage dans un module, faites le même choix dans un autre) ;
    Le découpage de votre projet : essayez de bien réfléchir à la façon dont vous découperez votre projet. Les fonctions, classes, modules et éventuellement packages formeront la structure de votre projet. Puisque votre code supportera deux applications, veillez à bien réfléchir aux fonctionnalités qui seront partagées par les deux ;
    La documentation de votre code : indiquez de loin en loin des commentaires et documentations (sous forme de docstring, pour vos classes et fonctions), afin de rendre votre code plus compréhensible pour quelqu'un qui le regarde ;
    La pertinence des tests : vos tests doivent être fonctionnels et utiles. Il ne faut pas seulement qu'ils fonctionnent, il faut qu'ils prouvent que le programme peut tourner correctement ;
    L'ouverture à l'amélioration : ce dernier point est donné quand votre code est aussi séparé que possible et permettrait sans difficulté des modifications, comme l'ajout d'autres obstacles dans le labyrinthe, l'utilisation de cartes 3D avec des escaliers pour circuler de niveau en niveau, l'utilisation d'un affichage graphique avec l'une des bibliothèques existantes, l'intégration de caractéristiques (la vie et le mouvement) aux robots, la création de nouvelles commandes, la création d'outils, etc. Si votre code est bien hiérarchisé, l'amélioration est généralement plus simple. Notez bien que vous n'avez pas à coder ces fonctionnalités, juste à garder en tête que votre programme pourrait évoluer par la suite.

 
Exemples de retour

Vous trouverez ci-dessous ce qu'on pourrait voir en exécutant le programme. Notez que :

    Les symboles utilisés sont O pour un mur, . pour une porte (sur laquelle le robot peut passer), U pour la sortie et X pour le robot lui-même ;
    Dans l'exemple ci-dessous, on lance le serveur puis deux clients. Les différents retours sont clairement identifiés ;
    Quand le robot passe une porte, elle devient invisible et s'affiche de nouveau quand le robot est passé ;
    Le robot ne peut pas passer à travers les murs ;
    Les robots adverses sont notés en minuscule x ;
    L'exemple ci-dessous est un exemple de la carte facile.

 

Côté serveur

python serveur.py
Labyrinthes existants :
  1 - facile.
  2 - prison.
Entrez un numéro de labyrinthe pour commencer à jouer : 1
On attend les clients.

Connexion du client 1

On tente de se connecter au serveur...
Connexion établie avec le serveur.
Bienvenue, joueur 2.

OOOOOOOOOO
O O    O O
O . OO   O
O O O x XO
O OOOO O.O
O O O    U
O OOOOOO.O
O O      O
O O OOOOOO
O . O    O
OOOOOOOOOO


Entrez C pour commencer à jouer :
c
La partie commence !

OOOOOOOOOO
O O    O O
O . OO   O
O O O X xO
O OOOO O.O
O O O    U
O OOOOOO.O
O O      O
O O OOOOOO
O . O    O
OOOOOOOOOO

Le joueur 1 peut ensuite jouer (un message l'informe que c'est son tour) et entrer les commandes comme il le faisait auparavant. Quand le jeu est fini (l'un des robots a atteint la sortie), les clients sont déconnectés.

 
À inclure dans votre correction

Vous devrez proposer en correction un fichier zip qui devra contenir :

    L'ensemble de votre code source. L'application serveur (à exécuter en premier) doit s'appeler serveur.py et doit se trouver à la racine de votre code source. L'application client (à exécuter après, autant de fois que de client à connecter) doit s'appeler client.py et se trouver au même endroit ;
    Une liste des cartes proposées par le programme. Le plus simple reste de créer un dossier cartes dans lequel se trouve les cartes. Là encore, le programme fourni doit être capable de les trouver sans modification du code ;
    Les tests unitaires, présents dans un sous-dossier test. Notez qu'il doit être possible de lancer tous les tests unitaires en entrant simplement python -m unittest à la racine du projet.

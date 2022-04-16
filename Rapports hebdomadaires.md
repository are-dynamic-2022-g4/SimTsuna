# Semaine du 14 mars au 20 mars

Nous avons décidé de nous nommer SimTsuna qui est un anagramme de tsunami.

Ensuite il a fallu faire des recherches dans le cadre de la séance biblio.
Nous avons trouvé beaucoup d'informations intéressantes à travers le net, et nous avons insisté particulièrement sur l'aspect préventif, des mesures mises en place face à ces catastrophes ainsi que les dégâts causés par les tsunamis.


Cette semaine, nous avons décidé de commencer la forme "béta"// le prototype de notre projet.


Nous comptons mettre en place une grille de vecteur (probablement une classe ayant la force et la direction du vecteur) afin de simuler la vague (en simulant le courant et la puissance du tsunami). Ces vecteurs vont en premier lieu rentrer en contact avec des formes qui représenteront les infrastructures que l'on souhaite tester afin de limiter les dégâts. Dans un deuxième temps, la vague rentrera en contact avec la ville/village, causant des dégâts ou non. À terme, nous analyserons les résultats obtenus (nombre de survivants, taux de destructions, budget restant, infrastructures encore fonctionnelles) l'utilisateur pourra en déduire l'efficacité des défences testées. 



Nous hésitons encore sur le language de programmation, nous préférrons évidemment le python (et le scratch !) cependant cela ne semble pas optimal. Nous hésitons donc entre les languages rust, java, C#, c++, que nous n'avons pas encore expérimenté.






# Semaine du 21 mars au 27 mars


Cette semaine nous avons commencé à coder.
Nous allons donc dans un premier temps mettre en place une "base", en codant une version simplifié de ce que l'on veut faire. 
Pour ce faire, nous allons chacun coder de nôtre côté, puis nous mettrons en commun et adopteront la méthode qui nous satisfait le plus.

L'idée de base pour cette "beta" serait d'implémenter le système suivant:
-3 matrices interagissant entre elles pour au final retourner une matrice avec différentes informations telles que le taux de destruction de la ville, de survivant... on pourra ensuite calculer des moyennes et données. 
  
  -Avoir une matrice représentant la ville, avec  chaque élément de cette matrice étant un objet de la classe 
  batiment(self,types:int , resistance:int, hauteur:int, etat:float, coords:tuple ): #altitude.
  

        
        types: 0-10 : représente le type de batiment à des coordonnes fixées (déterminera partiellement (avec hauteur)la safety des civils)
        
        resistance: échelle 0-10 en fonction des normes de résistances fixées
        
        hauteur: hauteur en mètres, permet de savoir si les civils sont safe ici (doit être cohérent avec le type)
        
        etat : pourcentage du taux de destruction (update après meeting) ++ dégât post vague
        
        coords: coordonnée du batiment   (permet de calculer la distance euclidienne par rapport à l'épicentre de la vague)
                <=> et quand la vague va tapper ces coordonnées
        

  
  -Avoir une matrice différente pour les civils, que l'on pourra superposer avec la matrice de la ville pour "tuer" des gens quand un immeuble est détruit.  
  Chaque case aura un objet de classe civil:
  Civil(qté:int,etat:float,coords:tuple)
  

    
    qté représente la qté de civil dans la zone (case) 
    
    etat représente le pourcentage de bléssés/morts
    
    coords permet de définir la zone étudié

  
  -Avoir une matrice pour la vague, ayant par case des éléments de la classe Vague:
  Vague(self, magnitude:int, hauteur:int, epicentre:tuple )
  

        
        hauteur: hauteur en mètres du batiment (permet de voir si l'endroit est safe pour les civils || si il va être détruit par la vague à 100% 
        (rapport de taille))
        
        epicentre: (coords) permet d'étudier la propagation initiale, et les distances euclidiennes par rapport à un endroit donnée
        
        magnitude: int(0-9) respectant l'échelle (permet de déterminer la "puissance" initiale du tsunami )

# Semaine du 28 mars au 03 avril

Partie rust réalisée par Philippe : 

During this week we've started working on the fluid simulation part of the project. We will use a lattice Boltzmann method, modified to support free-surface fluid simulations. For now, the simulation cannot handle collisions and free surfaces.

Fluid information is stored in a D3Q27 lattice.

Partie python réalisée par Hugo :


Un programme permettant d'initialiser 5 matrices différentes.
Les 4 premières sont mise bout à bout:
-La première celle de la ville, il s'agit de représenter une ville avec les éléments de la classe batiment. 
    
-Sur les mêmes dimensions, celle des civils, dans lesquels on stocke les civils à certaines coordonnées. 
-Création d'un littoral à taille variable, sur lequel on pourra venir construire des défenses.
-Une mer, avec différentes profondeurs générés selons les paramètres tailles et profondeur max 

la 5 eme matrice serait idéalement :
-de la taille toute les matrices mise bout à bout
-Permet de stocker dans chaque cases les infos théoriques de la vague à telles coordonnées, selon des calculs fait (magnitude,vitesse,hauteur,force,distance_epicentre) que l'on va recaculer apres chaque collision.


L'étape suivante serait d'implémenter une telle matrice, et de créer une fonction simulant la collision et la propagation de la vague dans la ville. 

# Semaine du 04 avril au 10 avril

-Le code a pris forme, il faut maintenant implémenter les collisions.

    -Début de l'implémentation des calculs, il faut donc trouver un moyen d'éxecuter les collisions, et en définir les paramètres.
    -Cependant ce n'est pas simple, car la physique(pour l'amplitude, la masse, la vitesse, les longueurs d'ondes...) des vagues est très variable et complexe. Il faudra donc simplifier énormément le système... 
    -De plus, nous n'avons pas trouvé de "norme anti-tsunami" comme il en existe pour les avalanches et séisme, c'est un gros hic car il n'y a donc pas de données concrète de résistance, il faut donc les calculer nous mêmes... (:c)
    Donc recherche de formules...



# Semaine du 11 avril au 17 avril
-Petite mise au point du projet:

    -Pour la vague nous allons donner les propriétés de la vague (hauteur, vitesse...)  en fonction de sa magnitude, selon l'échelle de Imamura.
    -Avec ces données nous pouvons déterminer l'Energie de la vague, avec laquelle on pense pouvoir trouver des formules pour la collision... (on espère !) 


  -Réalisations:
  
            -Recherche formule collision
            -implémentation d'une fonction de collision
            -Réalisation du rapport sur le "site"

Retappage du code python en une version plus claire, il n'y a désormais plus que 3 matrice,

    -1 grande matrice environnement avec la ville, le littoral et la mer,
    -une matrice des civils, de même dimensions que la ville, les civils sont placé où il y a des bâtiments
    -une matrice vague, où on stocke les informations de la vague pour chaque coordonnées.












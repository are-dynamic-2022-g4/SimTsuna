 # -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 18:57:50 2022

@author: MikaV

vitesse aux côtes = 50km/h

new methode:
    1 MPa = 0.00000981kg/m^2
    m = p * v (kg)
        masse volumique de l'eau = 997 kg/m^-3
        volume de l'eau ? = ...
        m^3 = surface en m^2 * épaisseur

résistance matériau:
    https://www.dynacast.com/fr-fr/ressources/dynamic-process-metal-selector
    https://www.holcimpartner.ch/fr/betonpraxis/proprietes-mecaniques-du-beton-durci
    

"""
from math import ceil
import random
import numpy as np

class Batiment:
    def __init__(self, resistance, hauteur, etat, coords):
        self.resi=resistance #1-10
        self.hauteur=hauteur #25-150
        self.etat=etat #100-0
        self.coords=coords #(i,j)
        self.mat=ceil(resistance/2)
        
    """def set_value_resi(self, valeur:int): #si besoin de set une value
        self.resi = valeur"""
        
    def __repr__(self):
        return "% s % s % s % s % s" % (self.resi, self.hauteur, self.etat, self.mat, self.coords)
    
    def detruit(self):
        self.resi=0
        self.hauteur=0
        self.etat=0
        self.mat=0
        
class Vague:
    def __init__(self, force, coords):
        #self.sens=sens #1,1.5,2,-1.5,-1,-0.5,0,0.5 == w, nw, n, ne, e, se, s, sw
        if force==-1:
            self.hauteur = 0.5
        elif force==0:
            self.hauteur = 1
        elif force==1:
            self.hauteur = 2
        elif force==2:
            self.hauteur = random.randint(4, 6)
        elif force==3:
            self.hauteur = random.randint(10, 20)
        elif force==4:
            self.hauteur = random.randint(20, 30)
        volume=100*self.hauteur #50m^2 car sur une case de 100m2 la vague != 100% de celle-ci
        m = 997 * volume
        pression_kg = m*10 #calcul trop compliqué donc estimation d'après la v et m^2 (/m^2)
        self.pression = round(pression_kg*0.00000981,2)
        self.force=force #(-1 à 4 sur l'échelle d'Imamura et Lida)
        self.coords=coords
        
    def __repr__(self):
        return "% s % s % s % s" % (self.force, self.hauteur, self.pression, self.coords)

class Civil:
    def __init__(self, nb_total, nb_blesse, coords):
        self.nb_total = nb_total
        self.nb_blesse = nb_blesse
        self.coords=coords
        
    def __repr__(self):
        return "% s % s % s" % (self.nb_total, self.nb_blesse, self.coords)

class Protection:
    def __init__(self, types, niv_protection):
        self.types = types #1-3 0=detruit
        self.niv_protection = niv_protection #1-5 0=detruit
        if types==0:
            self.hauteur = 0
        if types==1:
            self.hauteur = 2
        elif types==2:
            self.hauteur = niv_protection
        elif types==3:
            self.hauteur = niv_protection*3
        self.mat = niv_protection
        
def show(matrice):
    for i in matrice:
        print(i)
    print(" ")
    
def show_mat(ville, coords):
    i, j = coords
    if isinstance(ville[i][j][0], Batiment):
        print(lst_materiaux[ville[i][j][0].mat])
        print(" ")
        return
    if isinstance(ville[i][j][0], Protection):
        print(lst_materiaux[ville[i][j][0].mat])
        print(" ")
        return
    else:
        print("Ce n'est pas un batiment !")
        print(" ")
        return
        
def crea_ville(taille):
        ville = [[0 for x in range(taille)] for y in range(taille)]
        return ville

def crea_batiment(ville, taille):
    '''
    permet de setup la plage avec des valeurs à 0
    '''
    taille_ville = int((taille/3)*2)
    for i in range(taille):
        for j in range(taille_ville):
            bat = [Batiment(random.randint(1, 10),random.randint(25,150),100,(i,j))]
            ville[i][j] = bat
        ville[i][taille_ville-1] = [Batiment(0,0,100,(i,taille_ville-1))]
    return ville

def crea_vague(ville, force, taille):
    '''
    permet de créer le point d'origine du tsunami avec son sens et sa force
    '''
    for i in range(taille):
        for j in range(taille):
            if ville[i][j]==0:
                ville[i][j] = [Vague(force, (i,j))]
    return ville

def liste_voisins(coord:tuple, taille: int) -> list:
    """
    Prends en paramètre un couple de coordonnées et une taille et retourne tous les voisins des coordonnées.
    """
    i, j = coord
    return [(i+k, j+l) for k in range(-1,2) for l in range(-1,2)
            if not ((l==k) and (l==0)) and i+k >= 0 and i+k < taille
            and j+l >=0 and j+l < taille]

def liste_all(taille):
    lst=[]
    for i in range(taille):
        for j in range(taille):
           lst.append((i,j))
    return lst
    
def civilisation(ville, taille, densite):
    """ 
    permet d'attribuer les civils à la ville d'après une densité dans une échelle de 
    donnée par la liste lst_densite
    """
    mat_civil = crea_ville(taille)
    nb_civil_total = 0
    for i in range(taille):
        for j in range(taille):
            if isinstance(ville[i][j][0], Batiment):
                ht = ville[i][j][0].hauteur
                nb_civil = round(densite*ht)
                nb_civil_total = nb_civil_total + nb_civil 
                mat_civil[i][j] = [Civil(nb_civil, 0, (i,j))]
            else:
                mat_civil[i][j] = [Civil(0, 0, (i,j))]
    return mat_civil, nb_civil_total

def budget_ville(ville, taille, lst_prix):
    budget_ville=0
    for i in range(taille):
        for j in range(taille):
            if isinstance(ville[i][j][0],Batiment)==True:
                etage = int(ville[i][j][0].hauteur/3.3)
                budget_bat = lst_prix[ville[i][j][0].resi]*etage*100
                budget_ville+= budget_bat
            elif isinstance(ville[i][j][0], Protection)==True:
                print("pas encore fait...")
    print(" ")
    return budget_ville
                
def tsunami(ville, taille, mat_civil, nb_civil_total):
    f_v = 0
    h_v = 0   
    p_v = 0
    for i in range(taille):
        for j in reversed(range(taille)):
            temp.append((i,j))
            if isinstance(ville[i][j][0],Vague)==True: #mise a jour de la force et la hauteur de la vague
                h_v = ville[i][j][0].hauteur
                p_v = ville[i][j][0].pression
            if isinstance(ville[i][j][0], Batiment)==True: #calcul de la collision
                if ville[i][j][0].hauteur*1.1<h_v: #marge de 10%
                    ville[i][j][0].detruit()
                    nb_civil_total -= mat_civil[i][j][0].nb_total
                    mat_civil[i][j][0].nb_total = 0
                    h_v = h_v*0.9
                    p_v = p_v*0.9
                elif ville[i][j][0].hauteur*1.1>=h_v and ville[i][j][0].hauteur*0.9<=h_v:
                    #calcul si le batiment fait environ la meme taille que la vague
                    #dépend donc des "stats" de celui-ci
                elif ville[i][j][0].hauteur*0.9<h_v:
                    #calcul si la vague est peu "dangereuse" pour la batiment
                    
            if isinstance(ville[i][j][0], Protection)==True: #calcul collision avec les protections
                #à faire
    return ville

###############################################################################
#On set toutes les variables utiles pour les tests
lst_densite = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
lst_prix = [1000, 1150, 1300, 1450, 1600, 1750, 1900, 2050, 2200, 2350]
lst_materiaux = ["détruit", "brique", "bois", "béton", "roche", "béton fibré"] #[20,30,50,150,250]
lst_protection = ["détruit", "brise-lames", "digue", "mur"]
taille = 5

ville_test = crea_ville(taille)
print("Ville vide")
show(ville_test) #test création d'une matrice vide pour la ville

ville_test = crea_batiment(ville_test,taille)
print("Ville avec batiment et plage")
show(ville_test) #test creation de la ville

force = 4
ville_test = crea_vague(ville_test, force, taille)
print("Ville complete (ville + plage + vague)")
show(ville_test) #test creation de la vague

temp = []
lst_all = liste_all(taille)
mat_civil, nb_civil_total = civilisation(ville_test, taille, lst_densite[0])
print("Civils dans la ville:", nb_civil_total)
show(mat_civil) #test matrice des civils

budget_ville = budget_ville(ville_test, taille, lst_prix)
print("Le budget pour cette ville est: ", budget_ville) #test fn du budget (faite par Hugo)

show_mat(ville_test, (0,0)) #test verif d'un matériau

#ville_test = tsunami(ville_test, taille, mat_civil, nb_civil_total)
print("Ville après tsunami")
show(ville_test) #test des collisions du tsunami (fn coeur)
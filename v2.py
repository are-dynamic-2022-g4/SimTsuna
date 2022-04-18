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
        self.mat=ceil(resistance/2) #1-5
        
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
    def __init__(self, nb_total, coords):
        self.nb_total = nb_total
        self.coords=coords
        
    def __repr__(self):
        return "% s % s" % (self.nb_total, self.coords)

class Protection:
    def __init__(self, types, niv_protection, coords):
        self.types = types #1-3 0=detruit
        self.niv_protection = niv_protection #1-5 0=detruit # sert à connaitre le matériau
        if types==0:
            self.hauteur = 0
        if types==1:
            self.hauteur = 2
        elif types==2:
            self.hauteur = niv_protection
        elif types==3:
            self.hauteur = niv_protection*3
        self.mat = niv_protection
        self.coords = coords
        
    def detruit(self):
        self.types=0
        self.niv_protection=0
        self.hauteur=0
        self.mat = 0
        
    def __repr__(self):
        return "% s % s % s % s % s" % (self.types, self.niv_protection, self.hauteur, self.mat, self.coords)
        
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
            bat = [Batiment(random.randint(1, 10),random.randint(15,100),100,(i,j))]
            ville[i][j] = bat
        ville[i][taille_ville-1] = '_'
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

def crea_protection(ville, taille, types, niv_protection):
    for i in range(taille):
        for j in range(taille):
            if ville[i][j]=='_':
                ville[i][j]=[Protection(types, niv_protection, (i,j))]
    return ville
    
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
                mat_civil[i][j] = [Civil(nb_civil, (i,j))]
            else:
                mat_civil[i][j] = [Civil(0, (i,j))]
    return mat_civil, nb_civil_total

def budget_ville(ville, taille, lst_prix): #eh merce hugo
    budget_ville=0
    for i in range(taille):
        for j in range(taille):
            if isinstance(ville[i][j][0],Batiment)==True:
                etage = int(ville[i][j][0].hauteur/3.3)
                budget_bat = lst_prix[ville[i][j][0].resi]*etage*100 #car surface==100m2 ?
                budget_ville+= budget_bat
            elif isinstance(ville[i][j][0], Protection)==True:
                budget_protection = lst_prix[ville[i][j][0].mat*2]*ville[i][j][0].hauteur*50
                budget_ville += budget_protection
                #faire deux budget différents ? 
    return budget_ville
                
def tsunami(ville, taille, mat_civil):
    h_v = 0
    p_v = 0
    nb_civil_total = 0
    for i in range(taille):
        for j in reversed(range(taille)):
            #♥print(h_v, p_v) #debuggage
            if isinstance(ville[i][j][0],Vague)==True: #mise a jour de la force et la hauteur de la vague
                h_v = ville[i][j][0].hauteur
                p_v = ville[i][j][0].pression
            if isinstance(ville[i][j][0], Batiment)==True: #calcul de la collision
                if ville[i][j][0].hauteur*1.1<h_v: #marge de 10%
                    ville[i][j][0].detruit()
                    mat_civil[i][j][0].nb_total = 0
                    h_v = h_v*0.9
                    p_v = p_v*0.9
                elif ville[i][j][0].hauteur*1.1>=h_v:
                    #dépend donc des "stats" de celui-ci
                    if p_v>lst_resi[ville[i][j][0].mat]:
                        temp = p_v - lst_resi[ville[i][j][0].mat] #si la vague est + puissante
                        pourcentage = (100*temp/p_v)
                        h_v = h_v - (h_v*pourcentage)/100
                        p_v = temp
                        ville[i][j][0].etat = int(ville[i][j][0].etat - (ville[i][j][0].etat*pourcentage)/100)
                        mat_civil[i][j][0].nb_total = int((pourcentage*mat_civil[i][j][0].nb_total)/100)
                        nb_civil_total += mat_civil[i][j][0].nb_total
                    if p_v<lst_resi[ville[i][j][0].mat]:
                        temp = lst_resi[ville[i][j][0].mat] - p_v #si le mur résiste 
                        pourcentage = (100*temp)/lst_resi[ville[i][j][0].mat]
                        ville[i][j][0].resi =  int(ville[i][j][0].resi - (ville[i][j][0].resi*pourcentage)/100)
                        h_v = (h_v*pourcentage)/100
                        p_v = (pourcentage*p_v)/100
                        ville[i][j][0].etat = int(ville[i][j][0].etat - (ville[i][j][0].etat*pourcentage)/100)
                        mat_civil[i][j][0].nb_total = int((pourcentage*mat_civil[i][j][0].nb_total)/100)
                        nb_civil_total += mat_civil[i][j][0].nb_total
            if isinstance(ville[i][j][0], Protection)==True: #calcul collision avec les protections
                if ville[i][j][0].hauteur*1.1<h_v:
                    ville[i][j][0].detruit()
                elif ville[i][j][0].hauteur*1.1>h_v:
                    if p_v>lst_resi[ville[i][j][0].mat]:
                        temp = p_v - lst_resi[ville[i][j][0].niv_protection]
                        pourcentage = (100*temp/p_v)
                        h_v = h_v - (h_v*pourcentage)/100
                        p_v = temp
                    if p_v<lst_resi[ville[i][j][0].mat]:
                        temp = lst_resi[ville[i][j][0].niv_protection] - p_v #si le mur résiste 
                        pourcentage = (100*temp)/lst_resi[ville[i][j][0].niv_protection]
                        ville[i][j][0].niv_protection =  int(ville[i][j][0].niv_protection - (ville[i][j][0].niv_protection*pourcentage)/100)
                        h_v = (h_v*pourcentage)/100
                        p_v = (pourcentage*p_v)/100
    return ville, mat_civil, nb_civil_total

def main():
    #mise en place des listes pour la suite
    lst_densite = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    lst_prix = [1000, 1150, 1300, 1450, 1600, 1750, 1900, 2050, 2200, 2350, 2500]
    lst_materiaux = ["détruit", "brique", "bois", "béton", "roche", "béton fibré"] #[20,30,50,150,250]
    lst_resi = [0, 20, 30, 50, 150, 250]
    lst_protection = ["détruit", "brise-lames", "digue", "mur"]
    
    #mise en place de la ville
    taille = int(input("Taille matrice de la ville: "))
    force = int(input("Force du tsunami (d'après l'échelle d'Imamura: "))
    ville = crea_ville(taille)
    ville = crea_batiment(ville, taille)
    ville = crea_vague(ville, force, taille)  
    
    #mise en place civil & budget
    densite = int(input('Niveau de densité de population: '))
    mat_civil, nb_civil_total = civilisation(ville, taille, lst_densite[densite])
    return 
###############################################################################
#On set toutes les variables utiles pour les tests
lst_densite = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
lst_prix = [1000, 1150, 1300, 1450, 1600, 1750, 1900, 2050, 2200, 2350, 2500]
lst_materiaux = ["détruit", "brique", "bois", "béton", "roche", "béton fibré"] #[20,30,50,150,250]
lst_resi = [0, 20, 30, 50, 150, 250]
lst_protection = ["détruit", "brise-lames", "digue", "mur"]
taille = 7
force = 4

ville_test = crea_ville(taille)
ville_test = crea_batiment(ville_test,taille)
ville_test = crea_vague(ville_test, force, taille)

mat_civil, nb_civil_total = civilisation(ville_test, taille, lst_densite[0])
print("Civils dans la ville:", nb_civil_total)
show(mat_civil) #test matrice des civils

budget = budget_ville(ville_test, taille, lst_prix)
print("Le budget pour cette ville est: ", budget, "€") #test fn du budget (faite par Hugo)

ville_test = crea_protection(ville_test, taille, 1, 5)
budget2 = budget_ville(ville_test, taille, lst_prix)
print("Le budget pour cette ville+protection est: ", budget2, "€")

show(ville_test)
ville_test, mat_civil, new_nb_civil_total = tsunami(ville_test, taille, mat_civil)
print("Ville après tsunami")
print("Civils dans la ville:", new_nb_civil_total, ", Nombre de pertes :", nb_civil_total-new_nb_civil_total)
show(ville_test) #test des collisions du tsunami (fn coeur)
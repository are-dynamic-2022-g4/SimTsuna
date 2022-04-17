# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 18:13:01 2022

@author: Gogo
"""
import numpy as np
from random import randint
from math import sqrt
# from random import randrange
import random

#ville==10x10
#ville=np.zeros((10,10))
taille=10

#print("Carte de la ville: \n",ville)
print(" ")

print(" ")


class Batiment: 
    
    def __init__(self,norme_Securité:int, resistance:int, hauteur:int, etat:float, coords:tuple ): #altitude
        """
        types: 0-10 : représente le type de batiment à des coordonnes fixées (déterminera partiellement (avec hauteur)la safety des civils)
        resistance: échelle 0-10 en fonction des normes de résistances fixées
        hauteur: hauteur en mètres, permet de savoir si les civils sont safe ici (doit être cohérent avec le type)
        etat : pourcentage du taux de destruction (update après meeting) ++ dégât post vague
        coords: coordonnée du batiment   (permet de calculer la distance euclidienne par rapport à l'épicentre de la vague)
                <=> et quand la vague va tapper ces coordonnées
        
        
        pour l'affichage: 
            norme =objet[0]
            resistance =objet[1]
            hauteur =objet[2]
            etat=objet[3]
            coords =objet[4]
            
        """
        self.norme=norme_Securité
        self.resi=resistance
        self.hauteur=hauteur
        self.coords=coords
        self.etat=etat
        
    def __repr__(self):
        return "% s % s % s % s % s" % (self.norme,self.resi, self.hauteur, self.etat, self.coords)
        #return "Batiment resi:% s hauteur:% s etat:% s" % (self.resi, self.hauteur, self.etat) 

Maison1=Batiment(5,4,10,1,(2,5))
print("Maison1: ",Maison1)
class Vagues:
    def __init__(self, vitesse:float, coords:tuple,hauteur=1 ): #débri ? #distance euclidienne par rapport à l'épicentre == distance -> par rapport à la magnitude
#donne ptt la hauteur
        """
        hauteur: hauteur en mètres du batiment (permet de voir si l'endroit est safe pour les civils)
        epicentre: (coords) permet d'étudier la propagation initiale
        magnitude: int(0-4) échelle d'Imamura 
        l'amplitude dépend de la magnitude selon :hauteur_magnitude={-1: (0,0.5), 0:(0.5,1), 1: (1,2), 2: (4,6), 3: (10,20), 4:(20,50) }
        la vitesse lors de l'arrivée sur la côte est 
        """
        vitesse=50
        
        
        #self.magnitude=magnitude 
        self.vitesse=vitesse
        self.coords=coords
        self.hauteur=hauteur
        
                
    def __repr__(self):
        return "% s % s % s" % ( self.vitesse, self.hauteur, self.coords)






Vague1=Vagues(2,50,(3,3))
print("Vague1: ",Vague1)
###############################################################################################
def getnorme(moy,ecart_type):
    """fonction qui permet de générer une valeur aléatoire en connaissant une moyenne et un écart type
    la moyenne correspond aux "normes moyenne" de la ville, l'écart type est ajouté manuellement(pour avoir des variations au sein de la ville) 
    mais pas de formule pour cela (chercher ? peu probable de trouver )
    return une norme moyenne pour le batiment 
    """
    
    """problème: on attribue ici un batiment en fonction de la norme obtenue donc les maisons sont tjrs <3 par exemple
                soit [0,5,7,9,2,1,2,3,5]  -> 4-5 maisons, 2 mega immeubles new tech 1 immeuble un peu vieux mais en norme 
        sinon on peut faire l'inverse et générer un nombre aléatoire de maison 
        
    """
    
    
    mu = moy
    sigma = ecart_type
    result=-1

    data= np.random.randn(10000) * sigma + mu               #10000 valeurs générées 
    #print("data: ",data, min(data),max(data))
    while result<0 or result>10: #pour éviter les batiments au caractéristiques =0 (sol) ou négatif (pas gérable)
        result=np.random.choice(data)
    return int(result)



#print("hehe boiiii: ",gettypes(5, 2)) #valeurs prise aléatoirement pour les tests

def getresi(norme): #calc à partir de type et pas de norme 
    """calcule de manière aléatoire (mais limité par branche) la résistance en fonction de la norme du batiment
    on présuppose les normes de 0 à 10 
    la résistance est entre 0 et 100
    """
    #print("types pour rési: ", types)
    #print("dunno: ",(int(types)*10)-10,int(types)*10+10)
    result=randint((int(norme)*10)-10,int(norme)*10+10)
    #print("résult of type: ",result)
    return result




def gethauteur(norme):
    """fonction permettant de générer une hauteur cohérente en fonction du type de batiment (maison immeuble gratte ciel cabane) et de la norme
    on admet que les normes face au tsunamis sont murement réfléchies et efficaces (un batiment de norme 10 ne peut pas etre haut de 1,5m)"""
    #utiliser des preset? avec un dico (norme: tuple ) randint sur tuple + croiser avec un dico en fonction des batiments (ptt prendre le min et le max des 2 (de l'union))
    
    """il faut présupposer des tailles min max pour chaque type de batiments, soit: 
        1->cabane//barraque à frite->[2,5m]
        [2,3]->maison->[5,8m]
        [4,5]->petit immeuble->[8-28m]
        [6,7]-> immeuble moyen ->[28,50m] 
        [8,9]-> très grand immeubles -> [50,120m]
        10 ->mega bunker anti tsunami-> taille==0
        
        """
    # if types==10:
    #     return (800,800)
    #print("types: ",types)
    if norme==-1 or norme>10:
        raise ValueError("norme trop basse ou trop haute",norme)
    ref=[(800,800),(3,5),(5,8),(5,8),(8,28),(8,28),(28,50),(28,50),(50,120),(50,120),(120,300)]  #on pick 800 pour le bunker ultrasafe pck la hauteur n'importe pas (en vrai si mais ptt plus tard)
    
    
    return randint(ref[norme][0],ref[norme][1]) #sometimes we get list index out of range (nani)
#########################################################




def aff(objet,taillex,tailley,what):
    M=[[0 for x in range(tailley)] for y in range(taillex)]
    for i in range(taillex):
        for j in range(tailley):
            if objet[i][j]==0:
                M[i][j]=0
            else:
                if what=="hauteur":
                    M[i][j]=objet[i][j][0].hauteur
                elif what=="resi":
                    M[i][j]=objet[i][j][0].resi
            # if isinstance (objet[i][j][0],Batiment)==True:
            #     print("IT WORKED:" ,objet[i][j][0].hauteur )
            # else:
            #     print(0)
    for i in range(taillex):
        print(M[i])


def liste_voisins(coords:tuple,taille:int)->list:
    """fonction qui prend en paramètre les coordonnées d'un point et la taille du tableau, et qui retourne la liste
    des coordonnées des points voisins """
    
    i,j=coords
    a=[]
    if i!=0:
        for k in range(-1,2):
            if j!=0:
                for l in range(-1,2):
                    if not ((l==k) and (l==0)) and i+k<taille and j+l>=0 and j+l<taille and j<taille:
                        a.append((i+k,j+l))
            else:
                for l in range(0,2):
                    if not ((l==k) and (l==0)) and i+k<taille and j+l>=0 and j+l<taille:
                        a.append((i+k,j+l))
    else:
        for k in range(0,2):
            if j!=0:
                for l in range(-1,2):
                    if not ((l==k) and (l==0)) and i+k<taille and j+l>=0 and j+l<taille and j<taille:
                        a.append((i+k,j+l))
            else:
                for l in range(0,2):
                    if not ((l==k) and (l==0)) and i+k<taille and j+l>=0 and j+l<taille:
                        a.append((i+k,j+l))
    #if a==[]: condition si coords pas dans le tableau ->return une erreur au lieu de simplement []
    #qd i  ou j>taille
    return a



def genBoard(taille_ville:int ,taille_littoral:int ,taille_mer:int ,norme_moyenne:int ,nb_bats:int,nb_civils:int,infos_murs:list,profondeur_max):
    """
    

    Parameters
    ----------
    taille_ville : int
        taille de la partie ville de la matrice 
    taille_littoral : int
        taille de la partie littoral de la matrice 
    taille_mer : int
        taille de la partie mer de la matrice
    norme_moyenne : int
        norme moyenne des batiments de la ville (0-9)
    nb_bats : int
        nombre de batiments posés dans la ville
    nb_civils : int
        nombre de civils présent dans la ville
    infos_murs : list
         [[(coords y départ, épaisseur mur),(hauteur x départ, taille du mur),hauteur,resistance],[]].

    Returns
    -------
    None.

    """
    taille_totale=taille_ville+taille_littoral+taille_mer       #taille totale sur y de la matrice 
    taille=taille_ville #hauteur de la matrice//taille sur x 
    #print(taille_totale)
    board=[[0 for x in range(taille_totale)] for y in range(taille)]
    ####################################################
    #Partie ville
    coords_bat=[]
    x=0
    y=0
    for i in range(taille):
        print(board[i])
    print(" ")
    while len(coords_bat)<nb_bats:
        x=randint(0,taille_ville-1)
        y=randint(0,taille-1)
        if (x,y) not in coords_bat:
            coords_bat.append((x,y))    
    for i,j in coords_bat:
        norme=getnorme(norme_moyenne,2) #on prend "manuellement" comme écart type 2 afin d'avoir des variations dans le paysage, comme dans la vraie vie
        resi=getresi(norme)
        hauteur=gethauteur(norme)
        board[i][j]=[Batiment(norme,resi,hauteur,1,(i,j))]
    board[0][0]=[Batiment(norme,resi,hauteur,1,(i,j))]
    print("for i in range(taille_ville)")
    for i in range(taille_ville):
        print(board[i][:taille_ville])
    print("\nAffichage hauteur de la ville: \n")
    aff(board,taille_ville,taille,"hauteur")
    ##########################################
    #Partie Littoral
    print("\npartie littoral: \n")
    print("for i in range(taille_ville,taille_ville+taille_littoral")
    for i in infos_murs:
        x_mur=i[0][0]
        épaisseur_mur=i[0][1]
        y_mur=i[1][0]
        longueur_mur=i[1][1]
        hauteur_mur=i[2]
        resistance_mur=i[3]
        for i in range(taille_ville+x_mur,taille_ville+x_mur+épaisseur_mur):
            for j in range(y_mur,y_mur+longueur_mur): 
                board[j][i]=(resistance_mur,hauteur_mur)
                #board[j][i]=(hauteur_mur)
    for i in range(taille):
        print(board[i][taille_ville:taille_ville+taille_littoral])
    
    #########################################################
    #Partie Mer
    print("\npartie Mer: \n")
    print("for i in range(taille_ville+taille_littoral,taille_totale)")
    prof=0
    ratio=(profondeur_max/taille_mer*1)
    print("get ratioed, :",ratio)
    lvoisins=[]
    val_voisins=[1,2]
    vu=[]
    for j in range(taille_ville+taille_littoral,taille_totale):
        for i in range(taille):
            lvoisins=liste_voisins((j,i), taille_mer)
            vu.append((i,j))
            for k,p in (lvoisins):
                if (k,p) not in vu and k<taille and p<taille_mer:
                    val_voisins.append(board[k][p])
            
            b=randint(min(val_voisins)+prof,val_voisins[int(len(val_voisins)/2)]+prof)
            #b=round(random.uniform(min(val_voisins)+prof,val_voisins[int(len(val_voisins)/2)]+prof))
           
            if b<profondeur_max:
                board[i][j]=b
            else:
                print("oméga banana") 
                board[i][j]=profondeur_max
        #     a=random.choice(val_voisins)
        #     print("a: ",a,prof)
        #     if not (a==val_voisins[int(len(val_voisins)/2)]):
        #         b=randint(a+prof,val_voisins[int(len(val_voisins)/2)]+prof)
        #     else:
        #         b=a
        #     print("b: ",b)
        #     Mmer[i][j]=b
        prof+=int(ratio) 
        #prof+=ratio
    for i in range(taille):
        print(board[i][taille_ville+taille_littoral:taille_totale])
    print(" ")
    #########################################################################
    #Partie civile
    print("Partie civile : \n")
    print("stockée dans Mcivil")
    coords_bat=[]
    for i in range(taille):
        for j in range(taille):
            if board[i][j]!=0:
                coords_bat.append((i,j))
    print("il y a ",len(coords_bat)," batiments !")
    nb_bats=len(coords_bat)
    a=0
    b=0
    compteur=0
    result=-1
    nb_civil_restant=nb_civils
    Mcivil = [[0 for _ in range(taille) ] for _ in range(taille)]
    while nb_civil_restant>0:
        #print("nb civil restant : ",nb_civil_restant)
        #coords=(randint(0,taille-1),randint(0,taille-1))
        coords=random.choice(coords_bat)            #refaire ca 
        if nb_civil_restant<int(nb_civils/90): #mettre un pourcentage de nb_civil (10%?)
            #les mettre ensemble dans un spot libre 
            reroll=randint(0,nb_bats-1)
            Mcivil[coords_bat[reroll][0]][coords_bat[reroll][1]]+=nb_civil_restant
            nb_civil_restant-=nb_civil_restant
        result=randint(0,nb_civil_restant// 10)
        #print("result: ",result)
        #print(" ")
        #print("compteur: ",compteur)
        if Mcivil[coords[0]][coords[1]]==0 and compteur<=nb_bats-1:
            Mcivil[coords[0]][coords[1]]=result
            coords_bat.append(coords)
            nb_civil_restant-=result
            compteur+=1
        if compteur>=nb_bats :
            reroll=randint(0,nb_bats-1)
            Mcivil[coords_bat[reroll][0]][coords_bat[reroll][1]]+=result
            nb_civil_restant-=result
    for i in range(taille):
        for j in range(taille):
            if Mcivil[i][j]!=0:
                a+=1
                b+=Mcivil[i][j]
        print(Mcivil[i])
        
    print(" ")
    #########################################################################
    #Partie Vague 
    print("Partie Vague à supprimer")
    Vague=[[0 for x in range(taille_totale)] for y in range(taille)]
    for i in range(taille):
        print(Vague[i])
    print(" ")
    """
    on peut calculer l'amplitude d'une vague avec la relation suivante:
        a=(E**1/2)*(D**-1/2)*(P**-1/4) avec E= énergie de la vague, D la distance à l'épicentre, P la profondeur 
        et on sait que l'energie E se calcule: 
        E=1/16*(p*g*h**2) avec p la densité de l'eau de mer (==1024) g l'intensité de gravité (9.81) et h la hauteur de la vague
        et on suppose que les hauteurs sont tirées de la magnitude (Imamura)
    """
    z=0
    for j in reversed(range(taille_ville+taille_littoral,taille_totale)):
        for i in range(taille):
            Vague[i][j]=z
        z+=1
    for i in range(taille):
        print(Vague[i])
    
    ####################################################################
    #global
    print("Environnement: ")
    for i in range(taille):
        for k in range(taille_ville):
            if board[i][k]!=0:
                if isinstance(board[i][k][0],Batiment)==True:
                    #board[i][k]=board[i][k][0].norme                        #ici on ne CONSERVE que les normes
                    pass
        print(board[i])
    return board,Mcivil



    
hauteur=10
resistance=50

info_mur=[[(0,1),(1,8),hauteur,resistance],[(3,1),(1,8),hauteur,resistance]]

env1,mc1=genBoard(10,5,20,4,20,10000,info_mur,50)
#genBoard(taille_ville,taille_littoral,taille_mer,norme_moy,nb_bats,nb_civils,infor_mur,prof_max)

#hauteur=(251136**1/2)*(distance_epicentre**-1/2)*(profondeur**-1/4)



def distance(a:tuple,b:tuple):
    """
    distance euclidienne entre 2 points de coordonnées dans un milieu 2 dimensions
    """
    xa=a[0]
    ya=a[1]
    xb=b[0]
    yb=b[1]
    return sqrt((xa-xb)**2-(ya-yb)**2)


print(distance((3,3),(400,50)))


print(" ")



def hauteur_max(magnitude):
    """
    fonction générant des amplitudes plausibles en suivant l'échelle d'Imamura
    *100 pour convertir en cm
    """
    moy=0
    if magnitude==-1:
        hauteur = 0.5*100
        moy=5 #5cm
    elif magnitude==0:
        hauteur = 1*100
        moy=10 #10cm
    elif magnitude==1:
        hauteur = 2*100
        moy=randint(25-5,25+5)
    elif magnitude==2:
        hauteur = random.randint(4*100, 6*100)
        moy=randint(50-10,50+10)
    elif magnitude==3:
        hauteur = random.randint(10*100, 20*100)
        moy=randint(100-10,100+10)
    elif hauteur==4:
        hauteur = random.randint(20*100, 30*100)
        moy=randint(200-10,200+10)
    elif hauteur>4:
        #la mort de tlm, méga tsunami de >30m
        raise ValueError("wrong magnitude (>4)")
    return hauteur,moy

def Tsunami3(board,taille_ville,taille_littoral,taille_mer,magnitude):
    """
    On conserve la profondeur, et on crée une matrice pour la vague à côté
    """
    print("Tsunamising (amplitude en centimètre): ")
    taille_totale =len(board[0])
    taille=len(board)
    Vague=[[0 for x in range(taille_totale)] for y in range(taille)]
    vitesse=50
    #z=Vagues(magnitude,vitesse,(0,0))
    hauteur,moy=hauteur_max(magnitude)
    for j in range(taille_ville+taille_littoral,taille_totale):   #de gauche à droite
    #for j in reversed(range(taille_ville+taille_littoral,taille_totale)):       #de droite à gauche
        for i in range(taille):
            Vague[i][j]=Vagues(vitesse,(i,j),hauteur)
            #Vague[i][j]=Vague[i][j].hauteur #permet de return QUE l'AMPLITUDE
        while hauteur-moy>0:
            hauteur-=moy     #ICI METTRE FORMULE CALCULE DE LA HAUTEUR
            #faire passer la hauteur en cm  ? (évite le -=0.3
        hauteur=randint(int(moy-moy*0.2),int(moy+moy*0.2))
        #FAIRE LES CALCULS DE LA VITESSE AUSSI  // ET ENERGIE ? 
        
    for i in range(taille):
        for j in range(taille_totale):
            if isinstance(Vague[i][j],Vagues):
                Vague[i][j]=Vague[i][j].hauteur #affiche que l'amplitude 
        print(Vague[i])
    return Vague

v9=Tsunami3(env1,10,5,10,2)

def Tsunami4(board,taille_ville,taille_littoral,taille_mer,magnitude):
    """
    même chose que tsunami3, mais la vague est A LA PLACE DE LA MER

    Parameters
    ----------
    board : TYPE
        DESCRIPTION.
    taille_ville : TYPE
        DESCRIPTION.
    taille_littoral : TYPE
        DESCRIPTION.
    taille_mer : TYPE
        DESCRIPTION.
    magnitude : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    taille_totale =len(board[0])
    taille=len(board)
    print(taille,taille_totale)
    Vague=[[0 for x in range(taille_totale)] for y in range(taille)]
    vitesse=50
    z=Vagues(magnitude,vitesse,(0,0))
    hauteur=hauteur_max(magnitude)
    print("zzz: ",z)
    #for j in range(taille_ville+taille_littoral,taille_totale)):   #de gauche à droite
    for j in reversed(range(taille_ville+taille_littoral,taille_totale)):       #de droite à gauche
        for i in range(taille):
            board[i][j]=Vagues(magnitude,vitesse,(i,j),hauteur)
            board[i][j]=board[i][j].hauteur
        hauteur+=5        #ICI METTRE FORMULE CALCULE DE LA HAUTEUR
        #FAIRE LES CALCULS DE LA VITESSE AUSSI  // ET ENERGIE ? 
        
    for i in range(taille):
        for j in range(taille_totale):
            if isinstance(Vague[i][j],Vagues):
                board[i][j]=board[i][j].hauteur
        print(board[i])


print(" ")


def choc(coords:tuple,ville,vague,mcivil):
    #print("Gros choc: ")
    """ 
    coords tuple 
    ville la ville
    vague la vague
    civil matrice civil
    si objet[coords[0]][coords[1]][0].resistance< seuil: on tue les civils et on détruit le bat en mettant -1 au spot
    ou add dans un dictionnaire
    """
    """
    on peut calculer le nombre d'étage en faisant nb_étages=int(ville[x][y]/3.3)
    de là on peut calculer le nb de personne max
    il faut présupposer une surface 
    """
    """
    il faut réupdate les valeurs dans vague pendant le choc
    
    
    
    """ 
    
    seuil=50
    mort=0
    x=coords[0]
    y=coords[1]   
    
    #print("wave height (en metre): ",vague[0][15]/100)
    if ville[x][y]!=0 and ville[x][y]!=-1:
        print(ville[x][y])
        if isinstance(ville[x][y][0],Batiment):
            if ville[x][y][0].norme>0 and ville[x][y][0].resi<seuil or ville[x][y][0].norme/2<(vague[0][10])/100:
                print("Destruction de: ",(x,y))
                mort+=mcivil[x][y]
                mcivil[x][y]=0  #on efface les morts
                ville[x][y]=-1#on efface le batiment
            else:
                print("there was no change on: ",(x,y))
        else:
            print(ville[x][y])
            raise ValueError("not a bat")
        
    #print ("il y a eu ",mort," morts.")
    
    # for i in range(len(ville)):
    #     print(ville[i])
    return mort,ville









print("ville:\n")
for i in range(10):
    print(env1[i][:10])



# print("there was ",np.sum(mc1)," civilians")


# m=0
# v=0
# for i in range(10):
#     for j in range(10):
#         c,v=choc((i,j),env1,v9,mc1)
#         m+=c
# print("nb mort: ",m)
# for i in range(10):
#     print(v[i])











def cout(objet):
    """
    objet est direct une case batiment,  on définit le budget sur la norme ou alors sur un calcul via norme + hauteur
    
    """
    cout_construction=0
    prix_resi=[0,1000,1200,1350,1500,1600,1750,2000,2100,2300,2500]#prix par étage
    if objet!=0:
        if isinstance(objet,Batiment):
            hauteur=objet.hauteur
            rési=objet.resi
            etage=int(hauteur/3.3)
            #on crée une échelle pour la rési (admettons par étage de 100m² (ce qui est notre cas parfait))
               
            cout_construction=prix_resi[int(rési/10)]*1.2*etage*100

        else: #si c un mur du littoral
            rési=objet[0]
            hauteur=objet[1] #à vérifier 
            cout_construction=prix_resi[int(rési/10)]*hauteur*50*1.2
    return cout_construction           
    #prix d'une case vide en dégât ? 
    

print(cout(env1[0][0][0]))
print(cout(Batiment(3,34,15,1,(3,3))))



print("environnement: ")


for i in range(len(env1)):
    print(env1[i])

def budget(board,taille_ville,taille_littoral):
    """
    calcule le budget de la VILLE
    puis des murs
    ou alors on les calculs via infos_mur
    """
    budget_ville=0
    budget_littoral=0
    nb_mur=0
    hauteur_moy_mur=0
    resi_moy_mur=0
    budget_total=0
    nb_immeuble=0
    hauteur_moy_ville=0
    resi_moy_ville=0
    coords_vu=[]
    u=0
    for i in range(len(board)):
        for j in range(taille_ville):
            if env1[i][j]!=0:
                if isinstance(board[i][j][0],Batiment):
                    hauteur_moy_ville+=board[i][j][0].hauteur
                    resi_moy_ville+=board[i][j][0].resi
                    nb_immeuble+=1
                    budget_ville+=cout(board[i][j][0])
    
    
    for i in range(len(board)):
        for j in range(taille_ville,taille_ville+taille_littoral):
            if board[i][j]!=0: #si c un mur 
                budget_littoral+=cout(board[i][j])
                if j not in coords_vu:
                    nb_mur+=1   #se calcule lorsque l'axe y est différent
                    coords_vu.append(j)
                u+=1
                resi_moy_mur+=board[i][j][0]
                hauteur_moy_mur+=board[i][j][1]
    resi_moy_ville=resi_moy_ville/nb_immeuble
    hauteur_moy_ville=hauteur_moy_ville/nb_immeuble
    resi_moy_mur=resi_moy_mur/u
    hauteur_moy_mur=hauteur_moy_mur/u
    
    
    budget_total=budget_littoral+budget_ville

    #la même pour littoral
    print("\n Budget total de la ville: ",budget_ville,"€ pour ",nb_immeuble," immeubles.")
    print("resi et hauteurs moyennes: ", resi_moy_ville,hauteur_moy_ville)
    print("\n Budget total du littoral: ",budget_littoral,"€ pour ",nb_mur," mur.")
    print("resi et hauteurs moyennes: ", resi_moy_mur,hauteur_moy_mur)
    
    print("budget total attribué: ",budget_total,"€")



budget(env1,10,5)













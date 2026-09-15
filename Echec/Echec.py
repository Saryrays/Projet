import tkinter
import tkinter as tk
from tkinter import *
from tkinter import messagebox

# ------ Initialisation des constantes globales ------#
TAILLE_PIXEL = 90 # C'est la taille d'1 pixel, ce qui nous permet de représenter les colonnes & lignes de la grille
RANGEE = 8        # c'est le nombre de pixel par rangee
COLONNE = 8       # c'est le nombre de pixel par colonne
HAUTEUR = RANGEE * TAILLE_PIXEL
LARGEUR = COLONNE * TAILLE_PIXEL

# ------ Initialisation des variables globales ------#
images_cache =[]        # permet de stocker les images dans une liste
joueur = "Blancs"       # permet de savoir la couleur du joueur
pion_selection = False  # permet de savoir les coordonées du pion selectionner
Echec = False           # le roi de la couleur du joueur est en echec
temps_blanc = 601       # 10 minutes = 600 secondes
temps_noir = 600
timer_id = None

label_temps_blanc = None
label_temps_noir = None
#------ Initialisation des dictionnaire de chaque piece-----#
Blancs =[{"Type": "pions", "pos": [0, 6]}, {"Type": "pions", "pos": [1, 6]}, {"Type": "pions", "pos": [2, 6]}, {"Type": "pions", "pos": [3, 6]},{"Type": "pions", "pos": [4, 6]}, {"Type": "pions", "pos": [5, 6]}, {"Type": "pions", "pos": [6, 6]}, {"Type": "pions", "pos": [7, 6]},{"Type": "tour", "pos": [0, 7]},{"Type": "cavalier", "pos": [1, 7]},{"Type": "fou", "pos": [2, 7]},{"Type": "dame", "pos": [3, 7]},{"Type": "roi", "pos": [4, 7]},{"Type": "fou", "pos": [5, 7]},{"Type": "cavalier", "pos": [6, 7]},{"Type": "tour", "pos": [7, 7]}]
Noirs = [{"Type": "pions", "pos": [0, 1]}, {"Type": "pions", "pos": [1, 1]}, {"Type": "pions", "pos": [2, 1]}, {"Type": "pions", "pos": [3, 1]},{"Type": "pions", "pos": [4, 1]}, {"Type": "pions", "pos": [5, 1]}, {"Type": "pions", "pos": [6, 1],},{"Type": "pions", "pos": [7, 1]},{"Type": "tour", "pos": [0, 0]},{"Type": "cavalier", "pos": [1, 0]},{"Type": "fou", "pos": [2, 0]},{"Type": "dame", "pos": [3, 0]},{"Type": "roi", "pos": [4, 0]},{"Type": "fou", "pos": [5, 0]},{"Type": "cavalier", "pos": [6, 0]},{"Type": "tour", "pos": [7, 0]}]
for element in Blancs:
    element["compteur"] =0
    element["vivant"]= True
    element["selection"]=False
    element["couleur"] = "Blancs"
for element in Noirs:
    element["compteur"] =0
    element["vivant"]= True
    element["selection"]=False
    element["couleur"] = "Noirs"



def dessiner_tout():

    canva.delete("all")

    creer_grille()
    créer_pion()
    lettre_chiffre()
    echec_et_mat()

def fermer():
    """ fnc : fermer la fenetre quand on click sur la croix en haut a droite
        args : none
        return : none
    """
    global window
    window.destroy()

def creer_grille():
    """ fnc : créer la grille aux couleurs qu'on choisi en l'ocurence vert et beige
        args : non
        return : none
    """
    for x in range(COLONNE):
        for y in range(RANGEE):
            # Si COLONNE et RANGEE sont pairs ou COLONNE et RANGEE sont impairs, on attribue la couleur Blanche
            if (x % 2 == 0 and y % 2 == 0) or (x % 2 != 0 and y % 2 != 0):
                couleur = '#F8EFD4'
            else:
                couleur = '#75954F'
            # on apelle la fonction dessiner plateau
            dessiner_plateau(x, y, couleur)

def dessiner_plateau(colonne, rangee, couleur):
    """ fnc : fonction qui permet de dessiner des cases dans le canva à une certaine position
        args : int, int, str
        return : none
    """
    colonne_aff, rangee_aff = coord_affichage(colonne, rangee)

    x1 = colonne_aff * TAILLE_PIXEL
    y1 = rangee_aff * TAILLE_PIXEL
    x2 = (colonne_aff + 1) * TAILLE_PIXEL
    y2 = (rangee_aff + 1) * TAILLE_PIXEL
    # On dessine l'objet de (x1, y1) à (x2, y2) avec une couleur de fond et une couleur de bordure
    canva.create_rectangle(x1, y1, x2, y2, fill = couleur, outline = "grey")


def manger(pion):
    """ fnc : permet de verfier si on a manger une piece et on la fait disparaitre/suprime
        args : dict()
        return : none
    """
    global Blancs, Noirs, joueur, pion_selection
    for pion_blanc in Blancs :
        for pion_noir in Noirs:
            if pion_blanc["pos"] == pion_noir["pos"]:   # si 2 pions on les même position alors
                if joueur == "Blancs":
                    pion_noir["vivant"] = False         # le pion_noir est mort
                else :
                    pion_blanc["vivant"] = False         # le pion_blanc est mort
    # change c'est a qui de jouer
    if joueur == "Blancs":
        joueur ="Noirs"
    else :
        joueur = "Blancs"


    #promotions
    if pion["Type"] == "pions" : #on verifie si le pion peux avoir une promotions c'est a dire quand il est au bord le plus bas si c'est un pion noirs ou au plus haut si c'est un pion blancs
        if joueur == "Blancs" and pion["pos"][1] == 7 :
            promotions(pion)
        elif joueur == "Noirs" and pion["pos"][1] == 0:
            promotions(pion)
    dessiner_tout()

def echec():
    """fnc : renvoyer True si le roi du joueur est en echec
       args : None
       return : Booloean
    """
    global Noirs,Blancs
    Echec = False       # on definie d'abord que le roi n'est pas en echec
    liste_case_autoriser = []
    if joueur == "Blancs" :
        for pieces in Noirs :
            if pieces["vivant"]== True:     # si la piece ne s'est pas fait manger
                liste_case_autoriser += attaque(pieces)  #ajouter dans la liste les case_autoriser de chaque piece
        for pieces in Blancs :
            if  pieces["Type"] == "roi" :
                roi_coordonner = pieces["pos"]  # roi_coordonner retiens les coordonnées du roi

    elif joueur == "Noirs" :
        for pieces in Blancs :
            if pieces["vivant"]== True:     # si la piece ne s'est pas fait manger
                liste_case_autoriser += attaque(pieces)  #ajouter dans la liste les case_autoriser de chaque piece
        for pieces in Noirs :
            if  pieces["Type"] == "roi" :
                roi_coordonner = pieces["pos"]  # roi_coordonner retiens les coordonnées du roi

    if roi_coordonner in liste_case_autoriser : # si le roi est dans l'une des cases disponibles de l'adversaire alors le roi est en echec donc Echec = True
        Echec = True
        return Echec
    else :
        return Echec

def echec_et_mat():
    global Blancs, Noirs, joueur
    if echec() == False:
        return  # pas en échec, rien à faire

    # Le joueur est en échec : cherche s'il existe au moins un coup légal
    if joueur == "Noirs":
        equipe = Noirs
    else:
        equipe = Blancs

    for pieces in equipe:
        if pieces["vivant"] == False:
            continue
        liste = case_autoriser(pieces)
        liste = case_autoriser_Echec(pieces, liste)
        if len(liste) > 0:
            return  # au moins un coup légal existe → pas mat
    fin_de_partie(equipe)

def fin_de_partie(equipe):
    """fnc : regarde si un des 2 roi est mort si oui execute la fonction recommencer
       args : None
       return : Booleen
    """
    global Blancs, Noirs
    fenetre_choix = tk.Toplevel(window)
    if equipe == Blancs :
        fenetre_choix.title("Partie terminée les noirs ont gagnés")
    else :
        fenetre_choix.title("Partie terminée les blancs ont gagnés")
    fenetre_choix.geometry("400x200")
    fenetre_choix.grab_set()  # bloque les interactions avec la fenêtre principale
    if equipe == Blancs :
        tk.Label(fenetre_choix,text="Les noirs ont gagnés. Voulez-vous recommencez ?",font=("Arial", 12),pady=20).pack(pady=10)
    else :
        tk.Label(fenetre_choix,text="Les blancs ont gagnés. Voulez-vous recommencez ?",font=("Arial", 12),pady=20).pack(pady=10)
    def choix_bis(action):
        """ fnc : ferme la fenetre ou recommence une partie en fonction du choix effectuer
            args : str
            return : none
        """
        if action == "Réessayer":
            reset_jeu()
            fenetre_choix.destroy()  # ferme la petite fenêtre après le choix
        elif action == "Quitter":
            fermer() #fermer la fenetre principal
    # Boutons de choix
    tk.Button(fenetre_choix, text="Réessayer", command=lambda: choix_bis("Réessayer")).pack(pady=5)
    tk.Button(fenetre_choix, text="Quitter", command=lambda: choix_bis("Quitter")).pack(pady=5)

def promotions(pion):
    """ fnc : reatribue au pion son type en fonction du choix de la personne
        args : dict()
        return : none
    """
    fenetre_promotions = tk.Toplevel(window)
    fenetre_promotions.title("Promotion du pion")
    fenetre_promotions.geometry("400x250")
    fenetre_promotions.grab_set()  # bloque les interactions avec la fenêtre principale
    tk.Label(fenetre_promotions, text="Choisissez une pièce :", font=("Arial", 12)).pack(pady=10)

    def choix(type_piece):
        pion["Type"] = type_piece
        dessiner_tout()
        fenetre_promotions.destroy()  # ferme la petite fenêtre après le choix

    # Boutons de choix
    tk.Button(fenetre_promotions, text="Dame", command=lambda: choix("dame")).pack(pady=5)
    tk.Button(fenetre_promotions, text="Tour", command=lambda: choix("tour")).pack(pady=5)
    tk.Button(fenetre_promotions, text="Fou", command=lambda: choix("fou")).pack(pady=5)
    tk.Button(fenetre_promotions, text="Cavalier", command=lambda: choix("cavalier")).pack(pady=5)
def En_passant(pion):
    coordoner = pion["pos"]
    listePion = []
    for i in Blancs :
        if (i["pos"] == [coordoner[0] + 1,coordoner[1]] or i["pos"] == [coordoner[0] -1,coordoner[1]]) and i["compteur"] == 1 :
            listePion.append(i)
    for i in Noirs :
        if (i["pos"] == [coordoner[0] + 1,coordoner[1]] or i["pos"] == [coordoner[0] -1,coordoner[1]]) and i["compteur"] == 1 :
            listePion.append(i)


def Le_roque(pion):
    """ fnc : cette fonction sert juste a verifier si l'option du rock est autoriser ou non pour le roi
        args : dict()
        return : bool() or list()
    """
    global Noirs,Blancs

    petit_roque = []
    grand_roque = []

    if pion["Type"] == "roi" :
        if pion["compteur"] == 0:
            if echec() == False :
                if pion["couleur"] == "Blancs" :
                    x = pion["pos"][0]
                    y = pion["pos"][1]
                    #il faut que les case soit libre et pas attaquer
                    for i in range(1,3):
                        petit_roque.append([x + i,y])
                    for i in range(1,4):
                        grand_roque.append([x - i,y])

                    for piece_blanche in Blancs :
                        if piece_blanche["pos"] in petit_roque :
                            petit_roque = False
                            break

                    for piece_blanche in Blancs :
                        if piece_blanche["pos"] in grand_roque :
                            grand_roque = False
                            break

                    if petit_roque != False :
                        stop = False
                        for piece_noir in Noirs :
                            if stop == True:
                                break
                            cases_interdites = []
                            if piece_noir["Type"] == "pions":
                                #Les pions noir attaquent en diagonales vers le bas (y + 1)
                                if x - 1 >= 0 and y + 1 < 8:
                                    cases_interdites.append([x - 1, y + 1])
                                if x + 1 < 8 and y + 1 < 8:
                                    cases_interdites.append([x + 1, y + 1])
                            else :
                                cases_interdites = case_autoriser(piece_noir)
                            for case in cases_interdites :
                                if case in petit_roque :
                                    stop = True
                                    petit_roque = False
                                    break

                    if grand_roque != False :
                        stop = False
                        for piece_noir in Noirs :
                            if stop == True :
                                break
                            cases_interditesBis = []
                            if piece_noir["Type"] == "pions":
                                #Les pions noir attaquent en diagonales vers le bas (y + 1)
                                if x - 1 >= 0 and y + 1 < 8:
                                    cases_interditesBis.append([x - 1, y + 1])
                                if x + 1 < 8 and y + 1 < 8:
                                    cases_interditesBis.append([x + 1, y + 1])
                            else :
                                cases_interditesBis = case_autoriser(piece_noir)
                            for case in cases_interditesBis :
                                if case in grand_roque :
                                    grand_roque = False
                                    stop = True
                                    break
                if pion["couleur"] == "Noirs" :
                    if echec() == False :
                            x = pion["pos"][0]
                            y = pion["pos"][1]
                            #il faut que les case soit libre et pas attaquer
                            for i in range(1,3):
                                petit_roque.append([x + i,y])
                            for i in range(1,4):
                                grand_roque.append([x - i,y])

                            for piece_noire in Noirs :
                                if piece_noire["pos"] in petit_roque :
                                    petit_roque = False
                                    break

                            for piece_noire in Noirs :
                                if piece_noire["pos"] in grand_roque :
                                    grand_roque = False
                                    break

                            if petit_roque != False :
                                stop = False
                                for piece_noir in Blancs :
                                    if stop == True:
                                        break
                                    cases_interdites = []
                                    if piece_noir["Type"] == "pions":
                                        #Les pions noir attaquent en diagonales vers le bas (y + 1)
                                        if x - 1 >= 0 and y + 1 < 8:
                                            cases_interdites.append([x - 1, y + 1])
                                        if x + 1 < 8 and y + 1 < 8:
                                            cases_interdites.append([x + 1, y + 1])
                                    else :
                                        cases_interdites = case_autoriser(piece_noir)
                                    for case in cases_interdites :
                                        if case in petit_roque :
                                            stop = True
                                            petit_roque = False
                                            break

                            if grand_roque != False :
                                stop = False
                                for piece_noir in Blancs :
                                    if stop == True :
                                        break
                                    cases_interditesBis = []
                                    if piece_noir["Type"] == "pions":
                                        #Les pions noir attaquent en diagonales vers le bas (y + 1)
                                        if x - 1 >= 0 and y + 1 < 8:
                                            cases_interditesBis.append([x - 1, y + 1])
                                        if x + 1 < 8 and y + 1 < 8:
                                            cases_interditesBis.append([x + 1, y + 1])
                                    else :
                                        cases_interditesBis = case_autoriser(piece_noir)
                                    for case in cases_interditesBis :
                                        if case in grand_roque :
                                            grand_roque = False
                                            stop = True
                                            break
            else :
                grand_roque = False
                petit_roque = False
        else :
            grand_roque = False
            petit_roque = False
        return grand_roque,petit_roque

def recommencer():
    '''fnc : ouvre un menu pour choisir de recommencer ou quitter
       args : None
       return : None
    '''
    fenetre_choix = tk.Toplevel(window)
    fenetre_choix.title("Partie terminée")
    fenetre_choix.geometry("400x200")
    fenetre_choix.grab_set()  # bloque les interactions avec la fenêtre principale
    tk.Label(fenetre_choix,text="Voulez-vous recommencez ?",font=("Arial", 12),pady=20).pack(pady=10)

    def choix_bis(action):
        """ fnc : ferme la fenetre ou recommence une partie en fonction du choix effectuer
            args : str
            return : none
        """
        if action == "Réessayer":
            reset_jeu()
            fenetre_choix.destroy()  # ferme la petite fenêtre après le choix
        elif action == "Quitter":
            fermer() #fermer la fenetre principal

    # Boutons de choix
    tk.Button(fenetre_choix, text="Réessayer", command=lambda: choix_bis("Réessayer")).pack(pady=5)
    tk.Button(fenetre_choix, text="Quitter", command=lambda: choix_bis("Quitter")).pack(pady=5)

def reset_jeu():
    """fnc : relance les variables global
       args : None
       return : None
    """
    global Blancs, Noirs, joueur
    # réinitialise les variables global
    joueur = "Blancs"
    Blancs =[{"Type": "pions", "pos": [0, 6]}, {"Type": "pions", "pos": [1, 6]}, {"Type": "pions", "pos": [2, 6]}, {"Type": "pions", "pos": [3, 6]},{"Type": "pions", "pos": [4, 6]}, {"Type": "pions", "pos": [5, 6]}, {"Type": "pions", "pos": [6, 6]}, {"Type": "pions", "pos": [7, 6]},{"Type": "tour", "pos": [0, 7]},{"Type": "cavalier", "pos": [1, 7]},{"Type": "fou", "pos": [2, 7]},{"Type": "dame", "pos": [3, 7]},{"Type": "roi", "pos": [4, 7]},{"Type": "fou", "pos": [5, 7]},{"Type": "cavalier", "pos": [6, 7]},{"Type": "tour", "pos": [7, 7]}]
    Noirs = [{"Type": "pions", "pos": [0, 1]}, {"Type": "pions", "pos": [1, 1]}, {"Type": "pions", "pos": [2, 1]}, {"Type": "pions", "pos": [3, 1]},{"Type": "pions", "pos": [4, 1]}, {"Type": "pions", "pos": [5, 1]}, {"Type": "pions", "pos": [6, 1],},{"Type": "pions", "pos": [7, 1]},{"Type": "tour", "pos": [0, 0]},{"Type": "cavalier", "pos": [1, 0]},{"Type": "fou", "pos": [2, 0]},{"Type": "dame", "pos": [3, 0]},{"Type": "roi", "pos": [4, 0]},{"Type": "fou", "pos": [5, 0]},{"Type": "cavalier", "pos": [6, 0]},{"Type": "tour", "pos": [7, 0]}]
    for element in Blancs:
        element["compteur"] =0
        element["vivant"]= True
        element["selection"]=False
        element["couleur"] = "Blancs"
    for element in Noirs:
        element["compteur"] =0
        element["vivant"]= True
        element["selection"]=False
        element["couleur"] = "Noirs"
    dessiner_tout()
    global temps_blanc, temps_noir

    temps_blanc = 600
    temps_noir = 600
    label_temps_blanc.config(text="Blancs : 10:00")
    label_temps_noir.config(text="Noirs : 10:00")
def attaque(pion):
    """ fnc : Elle ressemble tres pour tres a case autoriser mais cette fonction renvoie toute les case sur les quelle attauqe les pieces on l'appelle dans echec
        args : dict()
        return : list(list())
    """
    global Blancs, Noirs
    liste_attaque = []
    liste_obstacles = scanner(pion)
    x = pion["pos"][0]
    y = pion["pos"][1]

    # ------------------ TOUR ------------------ #
    if pion["Type"] == "tour":
        #les 4 direction de la tour
        # Droite
        i = 1
        bloque = False
        #on parcourt les obstacles et on s'arretera a celui qui est a la droite de la tour si celui ci est de la meme couleur alors
        #on ne le met pas dans la liste si il est de la couleur inverse alors on l'ajoute et on ne peux pas aller plus loin
        while bloque == False and x+i < 8: # x < 8 car c'est la limite de notre plateau
            pos = [x+i, y]
            trouve = False

            for obstacle in liste_obstacles: # cette sert a s'arreter, elle nous permet de savoir qu'elle obstacle est sur la ligne de droite
                if obstacle["pos"] == pos:
                    trouve = True #sa veut dire que l'obstacle est trouver
                    bloque = True #donc on s'arrete
                    liste_attaque.append(pos)
            if trouve == False: # si la case est vide on ajoute celle si a la liste
                liste_attaque.append(pos)
            i += 1

        #pour pas que sa fasse mal au yeux on suit se meme resonnement pour les autres direction, pour les diagonalde du fous et ducoup pour la reine qui est juste l'esemble de la tour et du fou

        # Gauche
        i = 1
        bloque = False
        while bloque == False and x-i >= 0:
            pos = [x-i, y]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    liste_attaque.append(pos)

            if trouve == False:
                liste_attaque.append(pos)
            i += 1
        # Bas
        i = 1
        bloque = False
        while bloque == False and y+i < 8:
            pos = [x, y+i]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    liste_attaque.append(pos)

            if trouve == False:
                liste_attaque.append(pos)
            i += 1
        # Haut
        i = 1
        bloque = False
        while bloque == False and y-i >= 0:
            pos = [x, y-i]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    liste_attaque.append(pos)

            if trouve == False:
                liste_attaque.append(pos)
            i += 1

    # ------------------ FOU ------------------ #
    if pion["Type"] == "fou":
        # Bas-droite
        i = 1
        bloque = False
        while bloque == False and x+i < 8 and y+i < 8:
            pos = [x+i, y+i]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    liste_attaque.append(pos)

            if trouve == False:
                liste_attaque.append(pos)
            i += 1
        # Bas-gauche
        i = 1
        bloque = False
        while bloque == False and x-i >= 0 and y+i < 8:
            pos = [x-i, y+i]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    liste_attaque.append(pos)

            if trouve == False:
                liste_attaque.append(pos)
            i += 1
        # Haut-droite
        i = 1
        bloque = False
        while bloque == False and x+i < 8 and y-i >= 0:
            pos = [x+i, y-i]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    liste_attaque.append(pos)

            if trouve == False:
                liste_attaque.append(pos)
            i += 1
        # Haut-gauche
        i = 1
        bloque = False
        while bloque == False and x-i >= 0 and y-i >= 0:
            pos = [x-i, y-i]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    liste_attaque.append(pos)

            if trouve == False:
                liste_attaque.append(pos)
            i += 1

    #------------------dame ------------------#
    if pion["Type"] == "dame":

        # Combine tour + fou
        #les 4 direction de la tour
        # Droite
        i = 1
        bloque = False
        while bloque == False and x+i < 8:
            pos = [x+i, y]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    liste_attaque.append(pos)

            if trouve == False:
                liste_attaque.append(pos)
            i += 1
        # Gauche
        i = 1
        bloque = False
        while bloque == False and x-i >= 0:
            pos = [x-i, y]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    liste_attaque.append(pos)

            if trouve == False:
                liste_attaque.append(pos)
            i += 1
        # Bas
        i = 1
        bloque = False
        while bloque == False and y+i < 8:
            pos = [x, y+i]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    liste_attaque.append(pos)

            if trouve == False:
                liste_attaque.append(pos)
            i += 1
        # Haut
        i = 1
        bloque = False
        while bloque == False and y-i >= 0:
            pos = [x, y-i]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    liste_attaque.append(pos)

            if trouve == False:
                liste_attaque.append(pos)
            i += 1

        #Les diagonale du fou dans les 4 directions
        #Bas-droite
        i = 1
        bloque = False
        while bloque == False and x+i < 8 and y+i < 8:
            pos = [x+i, y+i]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    liste_attaque.append(pos)

            if trouve == False:
                liste_attaque.append(pos)
            i += 1

        #Bas-gauche
        i = 1
        bloque = False
        while bloque == False and x-i >= 0 and y+i < 8:
            pos = [x-i, y+i]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    liste_attaque.append(pos)

            if trouve == False:
                liste_attaque.append(pos)
            i += 1

        # Haut-droite
        i = 1
        bloque = False
        while bloque == False and x+i < 8 and y-i >= 0:
            pos = [x+i, y-i]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    liste_attaque.append(pos)

            if trouve == False:
                liste_attaque.append(pos)
            i += 1

        #Haut-gauche
        i = 1
        bloque = False
        while bloque == False and x-i >= 0 and y-i >= 0:
            pos = [x-i, y-i]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    liste_attaque.append(pos)

            if trouve == False:
                liste_attaque.append(pos)
            i += 1

    #------------------ roi ------------------#
    elif pion["Type"] == "roi":
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    nx  = x + dx
                    ny = y + dy
                    if 0 <= nx < 8 and 0 <= ny < 8:
                        liste_attaque.append([nx, ny])


    # ------------------ CavaLier ------------------ #
    elif pion["Type"] == "cavalier":
        for coordonner in [[2,1],[1,2],[-1,2],[-2,1],[-2,-1],[-1,-2],[1,-2],[2,-1]]:
            ny = y + coordonner[1]
            nx = x + coordonner[0]
            if 0 <= nx < 8 and 0 <= ny < 8:
                liste_attaque.append([nx, ny])


    # ------------------ PIONS ------------------ #
    if pion["Type"] == "pions":
        if pion["couleur"] == "Blancs":
            # Diagonales pour capturer
            for dx in [-1,1]: #le pion au echec ne mange que en diagonaldes donc on ajoute bien au x du pion 1 ou -1
                nx = x + dx
                ny = y-1 # car le pion est blanc donc en bas de l'echequier donc quand il va allez de l'avant il fera y-1 et c'est donc aussi l'ordonner sur lequel les pieces qui peux manger se trouve
                if nx >= 0 and nx < 8 and ny >= 0 and ny < 8: #si la case est dans l'echequier
                    for pieces in Noirs :
                        if pieces["pos"] == [nx, ny] :
                            liste_attaque.append([nx, ny])
                    for pieces in Blancs :
                        if pieces["pos"] == [nx, ny] :
                            liste_attaque.append([nx, ny])

        #c'est pareil que pour les blanc mais au lieux de faire y-1  on fait plus car les pion noir son toute en haut de l'echequier
        if pion["couleur"] == "Noirs":
            # Diagonales pour capturer
            for dx in [-1,1]:
                nx = x + dx
                ny = y+1
                if nx >= 0 and nx < 8 and ny >= 0 and ny < 8:
                    for pieces in Noirs :
                        if pieces["pos"] == [nx, ny] :
                            liste_attaque.append([nx, ny])
                    for pieces in Blancs :
                        if pieces["pos"] == [nx, ny] :
                            liste_attaque.append([nx, ny])

    return liste_attaque
def case_autoriser(pion):
    """ fnc : Case_autoriser sert a avoir les limites/ les cases sur lesquelles notre pion peux allez
            Trouve nous sert a verifier si sur la case il y a une piece et si il y a pas on ajoute a la liste_autoriser et si il y a mais que c'est de la meme couleur on ajoute pas
            Bloque nous sert a savoir si on continue ou pas d'avancer, c'est notre condition d'arret
        args : dict()
        return : list(list())
    """
    global Blancs, Noirs
    liste_autoriser = []
    liste_obstacles = scanner(pion)
    x = pion["pos"][0]
    y = pion["pos"][1]

    # ------------------ TOUR ------------------ #
    if pion["Type"] == "tour":
        #les 4 direction de la tour
        # Droite
        i = 1
        bloque = False
        #on parcourt les obstacles et on s'arretera a celui qui est a la droite de la tour si celui ci est de la meme couleur alors
        #on ne le met pas dans la liste si il est de la couleur inverse alors on l'ajoute et on ne peux pas aller plus loin
        while bloque == False and x+i < 8: # x < 8 car c'est la limite de notre plateau
            pos = [x+i, y]
            trouve = False

            for obstacle in liste_obstacles: # cette sert a s'arreter, elle nous permet de savoir qu'elle obstacle est sur la ligne de droite
                if obstacle["pos"] == pos:
                    trouve = True #sa veut dire que l'obstacle est trouver
                    bloque = True #donc on s'arrete
                    if obstacle["couleur"] != pion["couleur"]: # est ce une pieces adverse ?
                        liste_autoriser.append(pos)
            if trouve == False: # si la case est vide on ajoute celle si a la liste
                liste_autoriser.append(pos)
            i += 1

        #pour pas que sa fasse mal au yeux on suit se meme resonnement pour les autres direction, pour les diagonalde du fous et ducoup pour la reine qui est juste l'esemble de la tour et du fou

        # Gauche
        i = 1
        bloque = False
        while bloque == False and x-i >= 0:
            pos = [x-i, y]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    if obstacle["couleur"] != pion["couleur"]:
                        liste_autoriser.append(pos)

            if trouve == False:
                liste_autoriser.append(pos)
            i += 1
        # Bas
        i = 1
        bloque = False
        while bloque == False and y+i < 8:
            pos = [x, y+i]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    if obstacle["couleur"] != pion["couleur"]:
                        liste_autoriser.append(pos)

            if trouve == False:
                liste_autoriser.append(pos)
            i += 1
        # Haut
        i = 1
        bloque = False
        while bloque == False and y-i >= 0:
            pos = [x, y-i]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    if obstacle["couleur"] != pion["couleur"]:
                        liste_autoriser.append(pos)

            if trouve == False:
                liste_autoriser.append(pos)
            i += 1

    # ------------------ FOU ------------------ #
    if pion["Type"] == "fou":
        # Bas-droite
        i = 1
        bloque = False
        while bloque == False and x+i < 8 and y+i < 8:
            pos = [x+i, y+i]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    if obstacle["couleur"] != pion["couleur"]:
                        liste_autoriser.append(pos)

            if trouve == False:
                liste_autoriser.append(pos)
            i += 1
        # Bas-gauche
        i = 1
        bloque = False
        while bloque == False and x-i >= 0 and y+i < 8:
            pos = [x-i, y+i]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    if obstacle["couleur"] != pion["couleur"]:
                        liste_autoriser.append(pos)

            if trouve == False:
                liste_autoriser.append(pos)
            i += 1
        # Haut-droite
        i = 1
        bloque = False
        while bloque == False and x+i < 8 and y-i >= 0:
            pos = [x+i, y-i]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    if obstacle["couleur"] != pion["couleur"]:
                        liste_autoriser.append(pos)

            if trouve == False:
                liste_autoriser.append(pos)
            i += 1
        # Haut-gauche
        i = 1
        bloque = False
        while bloque == False and x-i >= 0 and y-i >= 0:
            pos = [x-i, y-i]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    if obstacle["couleur"] != pion["couleur"]:
                        liste_autoriser.append(pos)

            if trouve == False:
                liste_autoriser.append(pos)
            i += 1

    #------------------dame ------------------#
    if pion["Type"] == "dame":

        # Combine tour + fou
        #les 4 direction de la tour
        # Droite
        i = 1
        bloque = False
        while bloque == False and x+i < 8:
            pos = [x+i, y]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    if obstacle["couleur"] != pion["couleur"]:
                        liste_autoriser.append(pos)

            if trouve == False:
                liste_autoriser.append(pos)
            i += 1
        # Gauche
        i = 1
        bloque = False
        while bloque == False and x-i >= 0:
            pos = [x-i, y]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    if obstacle["couleur"] != pion["couleur"]:
                        liste_autoriser.append(pos)

            if trouve == False:
                liste_autoriser.append(pos)
            i += 1
        # Bas
        i = 1
        bloque = False
        while bloque == False and y+i < 8:
            pos = [x, y+i]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    if obstacle["couleur"] != pion["couleur"]:
                        liste_autoriser.append(pos)

            if trouve == False:
                liste_autoriser.append(pos)
            i += 1
        # Haut
        i = 1
        bloque = False
        while bloque == False and y-i >= 0:
            pos = [x, y-i]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    if obstacle["couleur"] != pion["couleur"]:
                        liste_autoriser.append(pos)

            if trouve == False:
                liste_autoriser.append(pos)
            i += 1

        #Les diagonale du fou dans les 4 directions
        #Bas-droite
        i = 1
        bloque = False
        while bloque == False and x+i < 8 and y+i < 8:
            pos = [x+i, y+i]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    if obstacle["couleur"] != pion["couleur"]:
                        liste_autoriser.append(pos)

            if trouve == False:
                liste_autoriser.append(pos)
            i += 1

        #Bas-gauche
        i = 1
        bloque = False
        while bloque == False and x-i >= 0 and y+i < 8:
            pos = [x-i, y+i]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    if obstacle["couleur"] != pion["couleur"]:
                        liste_autoriser.append(pos)

            if trouve == False:
                liste_autoriser.append(pos)
            i += 1

        # Haut-droite
        i = 1
        bloque = False
        while bloque == False and x+i < 8 and y-i >= 0:
            pos = [x+i, y-i]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    if obstacle["couleur"] != pion["couleur"]:
                        liste_autoriser.append(pos)

            if trouve == False:
                liste_autoriser.append(pos)
            i += 1

        #Haut-gauche
        i = 1
        bloque = False
        while bloque == False and x-i >= 0 and y-i >= 0:
            pos = [x-i, y-i]
            trouve = False
            for obstacle in liste_obstacles:
                if obstacle["pos"] == pos:
                    trouve = True
                    bloque = True
                    if obstacle["couleur"] != pion["couleur"]:
                        liste_autoriser.append(pos)

            if trouve == False:
                liste_autoriser.append(pos)
            i += 1

    #------------------ roi ------------------#
    if pion["Type"] == "roi":
        for dx in [-1,0,1]:
            for dy in [-1,0,1]: #on fait le tour du roi
                if dx != 0 or dy != 0: # [0,0] c'est le roi
                    nx = x + dx
                    ny = y + dy
                    if nx >= 0 and nx < 8 and ny >= 0 and ny < 8:
                        bloque = False
                        for obstacle in liste_obstacles:
                            if obstacle["pos"] == [nx, ny] and obstacle["couleur"] == pion["couleur"]:
                                bloque = True
                        if bloque == False:
                            liste_autoriser.append([nx, ny])


    # ------------------ CAVALIER ------------------ #
    if pion["Type"] == "cavalier":
        logique_deplacement_constant = [[2,1],[1,2],[-1,2],[-2,1],[-2,-1],[-1,-2],[1,-2],[2,-1]] # c'est a dire qui se deplace en L on a chercher a généraliser sa faisait trop lourd dans le scanner
        for deplacement in logique_deplacement_constant:
            nx = x + deplacement[0] #on fera pour tout les deplacement en L et on obtiendra les 8 case sur les qu'elles il peut allez
            ny = y + deplacement[1]
            if nx >= 0 and nx < 8 and ny >= 0 and ny < 8: # verifier si la case est bien dans l'echéquier
                bloque = False
                for obstacle in liste_obstacles: #comme pour la tour on verfie si l'obstacle
                    if obstacle["pos"] == [nx, ny] and obstacle["couleur"] == pion["couleur"]:
                        bloque = True
                if bloque == False:
                    liste_autoriser.append([nx, ny])


    # ------------------ PIONS ------------------ #
    if pion["Type"] == "pions":
        if pion["couleur"] == "Blancs":
            if y-1 >= 0: #verifie la case devant lui seulement si il est pas deja au bord
                libre = True
                for obstacle in liste_obstacles:
                    if obstacle["pos"] == [x, y-1]:
                        libre = False
                if libre == True:
                    liste_autoriser.append([x, y-1])

            if pion["compteur"] == 0 and y-2 >= 0: #verfie deux case devant car au echec le pion, si il est a sa case de depart, c'est a dire quand il as pas bouger (d'ou le compteur de mouvement de piece) il peux avancer de deux
                libre = True
                for obstacle in liste_obstacles:
                    if obstacle["pos"] == [x, y-1] or obstacle["pos"] == [x, y-2]:
                        libre = False
                if libre == True:
                    liste_autoriser.append([x, y-2])

            # Diagonales pour capturer
            for dx in [-1,1]: #le pion au echec ne mange que en diagonaldes donc on ajoute bien au x du pion 1 ou -1
                nx = x + dx
                ny = y-1 # car le pion est blanc donc en bas de l'echequier donc quand il va allez de l'avant il fera y-1 et c'est donc aussi l'ordonner sur lequel les pieces qui peux manger se trouve
                if nx >= 0 and nx < 8 and ny >= 0 and ny < 8: #si la case est dans l'echequier
                    for pieces in Noirs :
                        if pieces["pos"] == [nx, ny] and pieces["couleur"] != pion["couleur"]:
                            liste_autoriser.append([nx, ny])
                    for pieces in Blancs :
                        if pieces["pos"] == [nx, ny] and pieces["couleur"] != pion["couleur"]:
                            liste_autoriser.append([nx, ny])

        #c'est pareil que pour les blanc mais au lieux de faire y-1 ou y-2 on fait plus car les pion noir son toute en haut de l'echequier
        if pion["couleur"] == "Noirs":
            if y+1 < 8:
                libre = True
                for obstacle in liste_obstacles:
                    if obstacle["pos"] == [x, y+1]:
                        libre = False
                if libre == True:
                    liste_autoriser.append([x, y+1])
            if pion["compteur"] == 0 and y+2 < 8:
                libre = True
                for obstacle in liste_obstacles:
                    if obstacle["pos"] == [x, y+1] or obstacle["pos"] == [x, y+2]:
                        libre = False
                if libre == True:
                    liste_autoriser.append([x, y+2])
            # Diagonales pour capturer
            for dx in [-1,1]:
                nx = x + dx
                ny = y+1
                if nx >= 0 and nx < 8 and ny >= 0 and ny < 8:
                    for pieces in Noirs :
                        if pieces["pos"] == [nx, ny] and pieces["couleur"] != pion["couleur"]:
                            liste_autoriser.append([nx, ny])
                    for pieces in Blancs :
                        if pieces["pos"] == [nx, ny] and pieces["couleur"] != pion["couleur"]:
                            liste_autoriser.append([nx, ny])
    return liste_autoriser

def case_autoriser_Echec(pion,liste_autoriser):
    """fnc : on teste tout les case possible et on les ajoutest dans une liste case_valide si elle ne nous mette pas en echec
       args : pion(dict), liste_autoriser(liste(liste))
       return : case_valide(liste(liste))
    """
    global Blancs,Noirs,joueur
    case_valide =list()             # nouvelle liste restreinte de tout les casses autorisé
    ancienne_coord = pion["pos"]    # garde les anciennes coordonées

    if pion["Type"] == "roi" :
        ancienne_coord_roi = pion["pos"]
        for case in liste_autoriser :
            if joueur == "Blancs" :
                for pieces in Noirs :
                    if pieces["pos"] == case :

                        pieces_manger_fictive = pieces
                        pion["pos"] = case
                        pieces_manger_fictive["pos"] = [100,100]
                        pieces_manger_fictive["vivant"] = False

                        if echec() == True :
                            pion["pos"] = ancienne_coord_roi
                            pieces_manger_fictive["vivant"] = True
                            pieces_manger_fictive["pos"] = case

                        else :
                            if case not in case_valide :
                                case_valide.append(case)
                            pion["pos"] = ancienne_coord_roi
                            pieces_manger_fictive["vivant"] = True
                            pieces_manger_fictive["pos"] = case
                    else :
                        pion["pos"] = case
                        if echec() != True and case not in case_valide:
                            case_valide.append(case)
                        pion["pos"] = ancienne_coord
            else :
                for pieces in Blancs :
                    if pieces["pos"] == case :

                        pion["pos"] = case
                        pieces["pos"] = [100,100]
                        pieces["vivant"] = False

                        if echec() == True :
                            pion["pos"] = ancienne_coord_roi
                            pieces["vivant"] = True
                            pieces["pos"] = case

                        elif echec() != True :
                            if case not in case_valide :
                                case_valide.append(case)
                            pion["pos"] = ancienne_coord_roi
                            pieces["vivant"] = True
                            pieces["pos"] = case
                    else :
                        pion["pos"] = case
                        if echec() != True and case not in case_valide:
                            case_valide.append(case)
                        pion["pos"] = ancienne_coord
        return case_valide

    elif pion["Type"] != "roi"  :
        for case in liste_autoriser:
            # Chercher si une pièce adverse est sur la case cible (capture fictive)
            piece_capturee = None
            if joueur == "Blancs":
                for pieces in Noirs:
                    if pieces["pos"] == case and pieces["vivant"]:
                        piece_capturee = pieces
                        break
            else:
                for pieces in Blancs:
                    if pieces["pos"] == case and pieces["vivant"]:
                        piece_capturee = pieces
                        break

            # Simuler le mouvement (et la capture éventuelle)
            pion["pos"] = case
            if piece_capturee is not None:
                piece_capturee["vivant"] = False
                piece_capturee["pos"] = [100, 100]

            if echec() != True:
                case_valide.append(case)

            # Annuler la simulation
            pion["pos"] = ancienne_coord
            if piece_capturee is not None:
                piece_capturee["vivant"] = True
                piece_capturee["pos"] = case

        return case_valide


def créer_pion():
    """ Dessine toutes les pièces sans recréer les images à chaque fois """
    global Blancs, Noirs, images

    def dessiner_piece(element, img_key):
        x_aff, y_aff = coord_affichage(element["pos"][0], element["pos"][1])
        x = x_aff * TAILLE_PIXEL + 5
        y = y_aff * TAILLE_PIXEL + 5
        photo = images[img_key]

        # Couleur de fond selon la case
        if (element["pos"][0] % 2 == 0 and element["pos"][1] % 2 == 0) or \
           (element["pos"][0] % 2 != 0 and element["pos"][1] % 2 != 0):
            bg = "#75954F"
        else:
            bg = "#F8EFD4"

        canva.create_image(x + 17, y + 20, image=photo, anchor="nw")

    # ----- Pièces blanches -----
    for element in Blancs:
        if element["vivant"]:
            t = element["Type"]
            clé = {
                "pions": "wp",
                "cavalier": "wn",
                "fou": "wb",
                "tour": "wr",
                "dame": "wq",
                "roi": "wk"
            }[t]
            dessiner_piece(element, clé)
        else:
            element["pos"] = [100, 100]

    # ----- Pièces noires -----
    for element in Noirs:
        if element["vivant"]:
            t = element["Type"]
            clé = {
                "pions": "bp",
                "cavalier": "bn",
                "fou": "bb",
                "tour": "br",
                "dame": "bq",
                "roi": "bk"
            }[t]
            dessiner_piece(element, clé)
        else:
            element["pos"] = [100, 100]




def scanner(pion):
    """ fnc : regarder toute les pieces en vis-à-vis avec la piece
        args : dict()
        return : list(list())
    """
    global Blancs, Noirs
    # pion={} <--- mon pion a bouger
    liste_obstacle = []

    #---------------------------Tour------------------------------------------------------------------------------------#
    if pion["Type"] == "tour" :

        """_____________Verifie si il y a des pieces Noires Horizontalement et verticalement_________"""
        for x in range(8):
            for element in Noirs :
                if element["pos"] == [x,pion["pos"][1]] and element["pos"] != pion["pos"]:
                    liste_obstacle.append(element)
        for y in range(8):
            for element in Noirs :
                if element["pos"] == [pion["pos"][0],y] and element["pos"] != pion["pos"]:
                    liste_obstacle.append(element)

        """_____________Verifie si il y a des pieces blanches Horizontalement et verticalement_______"""
        for x in range(8):
            for element in Blancs :
                if element["pos"] == [x,pion["pos"][1]] and element["pos"] != pion["pos"]:
                    liste_obstacle.append(element)
        for y in range(8):
            for element in Blancs :
                if element["pos"] == [pion["pos"][0],y] and element["pos"] != pion["pos"]:
                    liste_obstacle.append(element)

    #-------------------------------Fou---------------------------------------------------------------------------------#
    if pion["Type"] == "fou" :
        for i in range(8):
            """_________________On verifie les pieces dans les 4 digonaldes differentes______________"""
            #--------  Diagonalde Bas_Droit  -----------------#
            for element in Noirs:
                if element["pos"] == [pion["pos"][0]+i,pion["pos"][1]+i] and element["pos"] != pion["pos"]:
                    liste_obstacle.append(element)
            for element in Blancs:
                if element["pos"] == [pion["pos"][0]+i,pion["pos"][1]+i] and element["pos"] != pion["pos"]:
                    liste_obstacle.append(element)

            #--------  Diagonalde Bas_Droit  -----------------#
            for element in Noirs:
                if element["pos"] == [pion["pos"][0]+i,pion["pos"][1]-i] and element["pos"] != pion["pos"]:
                    liste_obstacle.append(element)
            for element in Blancs:
                if element["pos"] == [pion["pos"][0]+i,pion["pos"][1]-i] and element["pos"] != pion["pos"]:
                    liste_obstacle.append(element)

            #--------  Diagonalde Bas_Gauche  ----------------#
            for element in Noirs:
                if element["pos"] == [pion["pos"][0]-i,pion["pos"][1]+i] and element["pos"] != pion["pos"]:
                    liste_obstacle.append(element)
            for element in Blancs:
                if element["pos"] == [pion["pos"][0]-i,pion["pos"][1]+i] and element["pos"] != pion["pos"]:
                    liste_obstacle.append(element)

            #--------  Diagonalde Haut-Gauche  ---------------#
            for element in Noirs:
                if element["pos"] == [pion["pos"][0]-i,pion["pos"][1]-i] and element["pos"] != pion["pos"]:
                    liste_obstacle.append(element)
            for element in Blancs:
                if element["pos"] == [pion["pos"][0]-i,pion["pos"][1]-i] and element["pos"] != pion["pos"]:
                    liste_obstacle.append(element)


    #------------------------------Dame---------------------------------------------------------------------------------#
    if pion["Type"] == "dame":

        """_____________Verifie si il y a des pieces Noires Horizontalement et verticalement________"""
        for x in range(8):
            for element in Noirs :
                if element["pos"] == [x,pion["pos"][1]] and element["pos"] != pion["pos"]:
                    liste_obstacle.append(element)
        for y in range(8):
            for element in Noirs :
                if element["pos"] == [pion["pos"][0],y] and element["pos"] != pion["pos"]:
                    liste_obstacle.append(element)
        """_____________Verifie si il y a des pieces blanches Horizontalement et verticalement_______"""
        for x in range(8):
            for element in Blancs :
                if element["pos"] == [x,pion["pos"][1]] and element["pos"] != pion["pos"]:
                    liste_obstacle.append(element)
        for y in range(8):
            for element in Blancs :
                if element["pos"] == [pion["pos"][0],y] and element["pos"] != pion["pos"]:
                    liste_obstacle.append(element)
        for i in range(8):
            """_________________On verifie les pieces dans les 4 digonaldes differentes______________"""
            #--------  Diagonalde Bas_Droit  -------------------------#
            for element in Noirs:
                if element["pos"] == [pion["pos"][0]+i,pion["pos"][1]+i] and element["pos"] != pion["pos"]:
                    liste_obstacle.append(element)
            for element in Blancs:
                if element["pos"] == [pion["pos"][0]+i,pion["pos"][1]+i] and element["pos"] != pion["pos"]:
                    liste_obstacle.append(element)

            #--------  Diagonalde Bas_Droit  -------------------------#
            for element in Noirs:
                if element["pos"] == [pion["pos"][0]+i,pion["pos"][1]-i] and element["pos"] != pion["pos"]:
                    liste_obstacle.append(element)
            for element in Blancs:
                if element["pos"] == [pion["pos"][0]+i,pion["pos"][1]-i] and element["pos"] != pion["pos"]:
                    liste_obstacle.append(element)

            #--------  Diagonalde Bas_Gauche  ------------------------#
            for element in Noirs:
                if element["pos"] == [pion["pos"][0]-i,pion["pos"][1]+i] and element["pos"] != pion["pos"]:
                    liste_obstacle.append(element)
            for element in Blancs:
                if element["pos"] == [pion["pos"][0]-i,pion["pos"][1]+i] and element["pos"] != pion["pos"]:
                    liste_obstacle.append(element)

            #--------  Diagonalde Haut-Gauche  ----------------------#
            for element in Noirs:
                if element["pos"] == [pion["pos"][0]-i,pion["pos"][1]-i] and element["pos"] != pion["pos"]:
                    liste_obstacle.append(element)
            for element in Blancs:
                if element["pos"] == [pion["pos"][0]-i,pion["pos"][1]-i] and element["pos"] != pion["pos"]:
                    liste_obstacle.append(element)


    #--------------------Roi-----------------------------------------#
    if pion["Type"] == "roi" :
        #on fait le tour de la piece
        for element in Noirs:
            if [element["pos"][0],element["pos"][1]] == [pion["pos"][0],pion["pos"][1]+1] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0]+1,pion["pos"][1]+1] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0]+1,pion["pos"][1]] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0]+1,pion["pos"][1]-1] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0],pion["pos"][1]-1] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0]-1,pion["pos"][1]-1] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0]-1,pion["pos"][1]] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0]-1,pion["pos"][1]+1]:
                liste_obstacle.append(element)
        for element in Blancs:
            if [element["pos"][0],element["pos"][1]] == [pion["pos"][0],pion["pos"][1]+1] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0]+1,pion["pos"][1]+1] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0]+1,pion["pos"][1]] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0]+1,pion["pos"][1]-1] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0],pion["pos"][1]-1] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0]-1,pion["pos"][1]-1] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0]-1,pion["pos"][1]] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0]-1,pion["pos"][1]+1]:
                liste_obstacle.append(element)


    #----------------------Pion--------------------------------------#
    if pion["Type"] == "pions" :
        if pion["couleur"] == "Blancs" :
            for element in Noirs:
                if [element["pos"][0],element["pos"][1]] == [pion["pos"][0],pion["pos"][1]-1] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0],pion["pos"][1]-2] :
                    liste_obstacle.append(element)

            for element in Blancs:
                if [element["pos"][0],element["pos"][1]] == [pion["pos"][0],pion["pos"][1]-1] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0],pion["pos"][1]-2] :
                    liste_obstacle.append(element)

    if pion["Type"] == "pions" :
        if pion["couleur"] == "Noirs" :
            for element in Noirs:
                if [element["pos"][0],element["pos"][1]] == [pion["pos"][0],pion["pos"][1]+1] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0],pion["pos"][1]+2] :
                    liste_obstacle.append(element)

            for element in Blancs:
                if [element["pos"][0],element["pos"][1]] == [pion["pos"][0],pion["pos"][1]+1] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0],pion["pos"][1]+2] :
                    liste_obstacle.append(element)

    #--------------------Cavalier-------------------------------------#
    if pion["Type"] == "cavalier" :
        for element in Noirs :
            if [element["pos"][0],element["pos"][1]] == [pion["pos"][0]+2,pion["pos"][1]+1] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0]-2,pion["pos"][1]+1] or[element["pos"][0],element["pos"][1]] == [pion["pos"][0]+1,pion["pos"][1]+2] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0]-1,pion["pos"][1]+2] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0]+2,pion["pos"][1]-1] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0]-2,pion["pos"][1]-1] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0]+1,pion["pos"][1]-2] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0]-1,pion["pos"][1]-2]:
                liste_obstacle.append(element)
        for element in Blancs:
            if [element["pos"][0],element["pos"][1]] == [pion["pos"][0]+2,pion["pos"][1]+1] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0]-2,pion["pos"][1]+1] or[element["pos"][0],element["pos"][1]] == [pion["pos"][0]+1,pion["pos"][1]+2] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0]-1,pion["pos"][1]+2] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0]+2,pion["pos"][1]-1] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0]-2,pion["pos"][1]-1] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0]+1,pion["pos"][1]-2] or [element["pos"][0],element["pos"][1]] == [pion["pos"][0]-1,pion["pos"][1]-2]:
                liste_obstacle.append(element)

    liste_obstacle_trier = trie_scanner(liste_obstacle,pion)
    return liste_obstacle_trier

def trie_scanner(liste_obstacle,pion):
    """ fnc : Fait le trie du scan  qui a été fait sur la piece toucher pour garder seulement celle qui  entrave le chemin
        args : list(dict())
        return : list(dict())
    """
    liste_obstacle_trier = []
    #------------------------------Tour-----------------------------------#
    if pion["Type"] == "tour":

        distance_min_droite = 100
        distance_min_gauche = 100
        distance_min_haut = 100
        distance_min_bas = 100

        pion_plus_proche_droite = None
        pion_plus_proche_gauche = None
        pion_plus_proche_haut = None
        pion_plus_proche_bas = None

        for element in liste_obstacle:

            # même ligne soit la ligne des ordonnées Y gauche et droite
            if element["pos"][1] == pion["pos"][1]:
                distance = abs(element["pos"][0] - pion["pos"][0])
                if element["pos"][0] > pion["pos"][0] and distance < distance_min_droite:
                    distance_min_droite = distance
                    pion_plus_proche_droite = element
                elif element["pos"][0] < pion["pos"][0] and distance < distance_min_gauche:
                    distance_min_gauche = distance
                    pion_plus_proche_gauche = element

            # même colonne soit la ligne des abscisses haut et bas
            elif element["pos"][0] == pion["pos"][0]:
                distance = abs(element["pos"][1] - pion["pos"][1])
                if element["pos"][1] > pion["pos"][1] and distance < distance_min_bas:
                    distance_min_bas = distance
                    pion_plus_proche_bas = element
                elif element["pos"][1] < pion["pos"][1] and distance < distance_min_haut:
                    distance_min_haut = distance
                    pion_plus_proche_haut = element

        #On ajoute seulement les pieces existentes
        for pion_plus_proche in [pion_plus_proche_droite,pion_plus_proche_gauche,pion_plus_proche_haut,pion_plus_proche_bas]:
            if pion_plus_proche != None:
                liste_obstacle_trier.append(pion_plus_proche)
        return liste_obstacle_trier


    if pion["Type"] == "fou" :
        distance_diagonalde_haut_droite = 100
        distance_diagonalde_bas_droite = 100
        distance_diagonalde_haut_gauche = 100
        distance_diagonalde_bas_gauche = 100

        pion_plus_proche_diagonalde_haut_droite = None
        pion_plus_proche_diagonalde_bas_droite = None
        pion_plus_proche_diagonalde_haut_gauche = None
        pion_plus_proche_diagonalde_bas_gauche = None

        for element in liste_obstacle:
            if element["pos"][0] > pion["pos"][0] and element["pos"][1] > pion["pos"][1] :
                distance = abs(element["pos"][0] - pion["pos"][0]) + abs(element["pos"][1] - pion["pos"][1])
                if distance < distance_diagonalde_bas_droite :
                    distance_diagonalde_bas_droite = distance
                    pion_plus_proche_diagonalde_bas_droite = element

            elif element["pos"][0] < pion["pos"][0] and element["pos"][1] < pion["pos"][1] :
                distance = abs(element["pos"][0] - pion["pos"][0]) + abs(element["pos"][1] - pion["pos"][1])
                if distance < distance_diagonalde_haut_gauche :
                    distance_diagonalde_haut_gauche = distance
                    pion_plus_proche_diagonalde_haut_gauche = element

            elif element["pos"][0] > pion["pos"][0] and element["pos"][1] < pion["pos"][1] :
                distance = abs(element["pos"][0] - pion["pos"][0]) + abs(element["pos"][1] - pion["pos"][1])
                if distance < distance_diagonalde_haut_droite :
                    distance_diagonalde_haut_droite = distance
                    pion_plus_proche_diagonalde_haut_droite = element

            elif element["pos"][0] < pion["pos"][0] and element["pos"][1] > pion["pos"][1] :
                distance = abs(element["pos"][0] - pion["pos"][0]) + abs(element["pos"][1] - pion["pos"][1])
                if distance < distance_diagonalde_bas_gauche :
                    distance_diagonalde_bas_gauche = distance
                    pion_plus_proche_diagonalde_bas_gauche = element

        for pion_plus_proche in [pion_plus_proche_diagonalde_haut_droite,pion_plus_proche_diagonalde_bas_droite,pion_plus_proche_diagonalde_haut_gauche,pion_plus_proche_diagonalde_bas_gauche]:
            if pion_plus_proche != None:
                liste_obstacle_trier.append(pion_plus_proche)
        return liste_obstacle_trier


    if pion["Type"] == "cavalier" :
        for element in liste_obstacle :
            if element["couleur"] == pion["couleur"]:
                liste_obstacle_trier.append(element)
        return liste_obstacle_trier


    if pion["Type"] == "pions":
        distance_min = 100
        pion_plus_proche = None
        for element in liste_obstacle :
            distance = abs(pion["pos"][0] - element["pos"][0])
            if distance < distance_min :
                distance_min = distance
                pion_plus_proche = element
        if pion_plus_proche != None :
            liste_obstacle_trier.append(pion_plus_proche)
        return liste_obstacle_trier


    if pion["Type"] == "roi" :
        for element in liste_obstacle:
            if element["couleur"] == pion["couleur"]:
                liste_obstacle_trier.append(element)
        return liste_obstacle_trier


    if pion["Type"] == "dame" :

        distance_min_droite = 100
        distance_min_gauche = 100
        distance_min_haut = 100
        distance_min_bas = 100
        distance_diagonalde_haut_droite = 100
        distance_diagonalde_bas_droite = 100
        distance_diagonalde_haut_gauche = 100
        distance_diagonalde_bas_gauche = 100

        pion_plus_proche_diagonalde_haut_droite = None
        pion_plus_proche_diagonalde_bas_droite = None
        pion_plus_proche_diagonalde_haut_gauche = None
        pion_plus_proche_diagonalde_bas_gauche = None
        pion_plus_proche_droite = None
        pion_plus_proche_gauche = None
        pion_plus_proche_haut = None
        pion_plus_proche_bas = None

        for element in liste_obstacle:
            # même ligne soit la ligne des ordonnées Y gauche et droite
            if element["pos"][1] == pion["pos"][1]:
                distance = abs(element["pos"][0] - pion["pos"][0])
                if element["pos"][0] > pion["pos"][0] and distance < distance_min_droite:
                    distance_min_droite = distance
                    pion_plus_proche_droite = element
                elif element["pos"][0] < pion["pos"][0] and distance < distance_min_gauche:
                    distance_min_gauche = distance
                    pion_plus_proche_gauche = element

            # même colonne soit la ligne des abscisses haut et bas
            elif element["pos"][0] == pion["pos"][0]:
                distance = abs(element["pos"][1] - pion["pos"][1])
                if element["pos"][1] > pion["pos"][1] and distance < distance_min_bas:
                    distance_min_bas = distance
                    pion_plus_proche_bas = element
                elif element["pos"][1] < pion["pos"][1] and distance < distance_min_haut:
                    distance_min_haut = distance
                    pion_plus_proche_haut = element

        #On ajoute seulement les pieces existentes
        for pion_plus_proche in [pion_plus_proche_droite,pion_plus_proche_gauche,pion_plus_proche_haut,pion_plus_proche_bas]:
            if pion_plus_proche != None:
                liste_obstacle_trier.append(pion_plus_proche)


        for element in liste_obstacle:
            if element["pos"][0] > pion["pos"][0] and element["pos"][1] > pion["pos"][1] :
                distance = abs(element["pos"][0] - pion["pos"][0]) + abs(element["pos"][1] - pion["pos"][1])
                if distance < distance_diagonalde_bas_droite :
                    distance_diagonalde_bas_droite = distance
                    pion_plus_proche_diagonalde_bas_droite = element

            elif element["pos"][0] < pion["pos"][0] and element["pos"][1] < pion["pos"][1] :
                distance = abs(element["pos"][0] - pion["pos"][0]) + abs(element["pos"][1] - pion["pos"][1])
                if distance < distance_diagonalde_haut_gauche :
                    distance_diagonalde_haut_gauche = distance
                    pion_plus_proche_diagonalde_haut_gauche = element

            elif element["pos"][0] > pion["pos"][0] and element["pos"][1] < pion["pos"][1] :
                distance = abs(element["pos"][0] - pion["pos"][0]) + abs(element["pos"][1] - pion["pos"][1])
                if distance < distance_diagonalde_haut_droite :
                    distance_diagonalde_haut_droite = distance
                    pion_plus_proche_diagonalde_haut_droite = element

            elif element["pos"][0] < pion["pos"][0] and element["pos"][1] > pion["pos"][1] :
                distance = abs(element["pos"][0] - pion["pos"][0]) + abs(element["pos"][1] - pion["pos"][1])
                if distance < distance_diagonalde_bas_gauche :
                    distance_diagonalde_bas_gauche = distance
                    pion_plus_proche_diagonalde_bas_gauche = element

        for pion_plus_proche in [pion_plus_proche_diagonalde_haut_droite,pion_plus_proche_diagonalde_bas_droite,pion_plus_proche_diagonalde_haut_gauche,pion_plus_proche_diagonalde_bas_gauche]:
            if pion_plus_proche != None:
                liste_obstacle_trier.append(pion_plus_proche)
        return liste_obstacle_trier

def bouger_pion(x,y):
    """ fnc : Recherche d'abord la piece selectionné dans les pieces noirs et blanches, si les coordonnées sont les memes on determine son type et ainsi ces restriction de mouvement
        args : coordoner de la case selectionner en x et y
        return : none
    """
    global pion_selection, joueur
    pion = None
    if joueur == "Blancs":
        for piece in Blancs:
            if piece["pos"] == pion_selection:
                pion = piece
    else:
        for piece in Noirs:
            if piece["pos"] == pion_selection:
                pion = piece
    if pion != None:
        liste_case_autoriser = case_autoriser(pion)
        liste_case_autoriser = case_autoriser_Echec(pion, liste_case_autoriser)
        if pion["Type"] == "pions" :
            En_passant(pion)
        if pion["Type"] == "roi" :
            grand_roque,petit_roque = Le_roque(pion)
            if pion["couleur"] == "Blancs" :
                if [x,y] == [2,7] :
                    if grand_roque != False :
                        liste_case_autoriser.append([2,7])
                        for pieces in Blancs :
                            if pieces["pos"] == [0,7] :
                                pieces["pos"] = [3,7]
                if [x,y] == [6,7] :
                    if petit_roque != False :
                        liste_case_autoriser.append([6,7])

                        for pieces in Blancs :
                            if pieces["pos"] == [7,7] :
                                pieces["pos"] = [5,7]
            if pion["couleur"] == "Noirs" :
                if [x,y] == [2,0] :
                    grand_roque,petit_roque = Le_roque(pion)
                    if grand_roque != False :
                        liste_case_autoriser.append([2,0])
                        for pieces in Noirs :
                            if pieces["pos"] == [0,0] :
                                pieces["pos"] = [3,0]
                if [x,y] == [6,0] :
                    if petit_roque != False :
                        liste_case_autoriser.append([6,0])
                        for pieces in Noirs :
                            if pieces["pos"] == [7,0] :
                                pieces["pos"] = [5,0]

        pion_selection =False

        if [x,y] in liste_case_autoriser:
            pion["pos"] =[x,y]
            pion["compteur"] += 1
            manger(pion)

def formater_temps(t):
    minutes = t // 60
    secondes = t % 60
    return f"{minutes:02}:{secondes:02}"

def update_timer():
    global temps_blanc, temps_noir, timer_id

    if joueur == "Blancs":
        temps_blanc -= 1

    elif joueur == "Noirs":
        temps_noir -= 1

    # Mise à jour affichage
    label_temps_blanc.config(text=formater_temps(temps_blanc))

    label_temps_noir.config(text=formater_temps(temps_noir))

    # Vérification fin
    if temps_blanc <= 0:
        messagebox.showinfo(
            "Temps écoulé",
            "Les Noirs gagnent !"
        )
        return

    if temps_noir <= 0:
        messagebox.showinfo(
            "Temps écoulé",
            "Les Blancs gagnent !"
        )
        return

    # Relance du timer
    timer_id = window.after(1000, update_timer)

def afficher_case_dispo(pion):
    """fnc : permet d'afficher les cases dispo pour le pion selection avec un rond gris
       args : pion(dict)
       return : None
    """
    liste_case_autoriser = case_autoriser(pion)
    liste_case_autoriser = case_autoriser_Echec(pion, liste_case_autoriser)

#les cases du roi si il peux faire le roque ou pas
    if pion["Type"] == "roi" :
        grand_roque,petit_roque = Le_roque(pion)
        if grand_roque != False :
            if joueur == "Blancs":
                liste_case_autoriser.append([2,7])
            if joueur == "Noirs" :
                liste_case_autoriser.append([2,0])
        if petit_roque != False :
            if joueur == "Blancs" :
                liste_case_autoriser.append([6,7])
            if joueur == "Noirs" :
                liste_case_autoriser.append([6,0])



    # 1ere option afficher les cases sur lesquelle on peux jouer
    for case in liste_case_autoriser:
        x, y = coord_affichage(case[0], case[1])

        # Coordonnées du centre de la case
        x_centre = x * 90 + 90 / 2
        y_centre = y * 90 + 90 / 2
        # Rayon du rond
        r = 90 * 0.1
        canva.create_oval(x_centre - r, y_centre - r,x_centre + r, y_centre + r,fill="#A5A5A5")

def tour_joueur ():
    """fnv : change la couleur de fond de la fenetre en fonction de qui joue.
    arg : none
    return : none
    """
    global joueur
    if joueur =="Blancs":
        window.config(bg="beige")
    else :
        window.config(bg="black")

def lettre_chiffre():

    lettres = ["A","B","C","D","E","F","G","H"]
    chiffres = ["8","7","6","5","4","3","2","1"]

    if joueur == "Noirs":
        lettres.reverse()
        chiffres.reverse()

    for i in range(8):

        canva.create_text(
            i * TAILLE_PIXEL + TAILLE_PIXEL // 2,
            HAUTEUR - 10,
            text=lettres[i],
            font=("Arial", 14)
        )

        canva.create_text(
            10,
            i * TAILLE_PIXEL + TAILLE_PIXEL // 2,
            text=chiffres[i],
            font=("Arial", 14)
        )

def click(event):
    """ fnc : permet de connaitre quel pion est selectionner grace au coordonées de la souris en x,y
        args : float(),float()
        return : none
    """
    global pion_selection,x,y
    x = event.x // TAILLE_PIXEL
    y = event.y // TAILLE_PIXEL

    if joueur == "Noirs":
        x = 7 - x
        y = 7 - y
    selection = False         #on initialise la variable qui permet de prendre les coordonées d'un pion
    dessiner_tout()
    if pion_selection !=False:  # si on a deja cliqué avant et que c'était sur un pion on effectue bouger_pion

        bouger_pion(x,y)

    else :
        if joueur == "Blancs":
            for pion in Blancs:
                if pion["pos"] == [x,y]:
                    selection = pion["pos"]     # selection prend les coordonée du pion
                    afficher_case_dispo(pion)

        else :
            for pion in Noirs:
                if pion["pos"] == [x,y]:
                    selection = pion["pos"]     # selection prend les coordonée du pion
                    afficher_case_dispo(pion)

        if selection == pion_selection and selection != False:  # ?
            pion_selection = False

        else :
            pion_selection = selection      #pion_selection prend les coordonées selection


def coord_affichage(x, y):
    """Transforme les coordonnées selon le joueur."""
    global joueur

    if joueur == "Noirs":
        return 7 - x, 7 - y  # rotation du plateau
    return x, y
# ------ Programme principal ------

# On crée une fenêtre à l'aide de la bibliothèque tkinter et on lui donne un titre
window = tkinter.Tk()
window.state("zoomed")
label_temps_blanc = tk.Label(
    window,
    text="10:00",
    font=("Arial", 22, "bold"),
    width=8,
    bg="white",
    fg="black",
    relief="solid",
    bd=2
)

label_temps_blanc.place(x=20, y=100)

label_temps_noir = tk.Label(
    window,
    text="10:00",
    font=("Arial", 22, "bold"),
    width=8,
    bg="black",
    fg="white",
    relief="solid",
    bd=2
)

label_temps_noir.place(x=20, y=200)
window.title("Micro-Projet Echec")


# On crée un canevas dans la fenêtre aux bonnes dimensions
canva = tkinter.Canvas(window, width = LARGEUR, height = HAUTEUR) # Un caneva est une zone rectangulaire destinée à contenir des dessins ou d’autres figures complexes
canva.place(x=300, y=0) # On l'ajoute à la fenêtre
canva.focus_set() # On place le focus sur la fenêtre
label_temps_blanc.place(
    x=20,
    y=100
)

label_temps_noir.place(
    x=20,
    y=200
)
# On utilise la méthode bind pour lier un événement au canva
# Dès qu'un clic sera appuyé, la fonction click sera appelé avec en argument event qui est les coordonées de la souris quand on a cliquer
canva.bind("<Button-1>", click)

#c'est la croix en haut a droite de l'ecran
window.protocol("WM_DELETE_WINDOW", fermer)

# On crée la grille du jeu
creer_grille()



#on ajoute les lettres par rapport aux cases
lettre_chiffre()
images = {
    "wp": PhotoImage(file="wp.png"),
    "wn": PhotoImage(file="wn.png"),
    "wb": PhotoImage(file="wb.png"),
    "wr": PhotoImage(file="wr.png"),
    "wq": PhotoImage(file="wq.png"),
    "wk": PhotoImage(file="wk.png"),

    "bp": PhotoImage(file="bp.png"),
    "bn": PhotoImage(file="bn.png"),
    "bb": PhotoImage(file="bb.png"),
    "br": PhotoImage(file="br.png"),
    "bq": PhotoImage(file="bq.png"),
    "bk": PhotoImage(file="bk.png"),
}
# Après avoir dessiner la grille on dessine les pieces
créer_pion()
# On affiche la fenetre en boucle
update_timer()
window.mainloop()




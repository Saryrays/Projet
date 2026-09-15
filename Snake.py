import tkinter
from easygui import *
import random

# ------ Initialisation des constantes globales ------
TAILLE_PIXEL = 20 # C'est la taille d'1 pixel, ce qui nous permet de représenter les colonnes & lignes de la grille
RANGEE = 32
COLONNE = 32
HAUTEUR = RANGEE * TAILLE_PIXEL
LARGEUR = COLONNE * TAILLE_PIXEL

# ------ Initialisation des variables globales ------
nourriture_positionnee = False
nourriture_coordonnees = [0, 0]
serpent_direction = 2 # -1 en haut, 1 en bas, -2 à gauche et 2 à droite
serpent_coordonnees = [[4, 16], [3, 16], [2, 16]] # Position du serpent à l'origine (Tête en position 0)
score = 0

def creer_grille():
    """ fnc : créer la grille aux couleurs bleues et grises
        args :
        return : none
    """
    for x in range(COLONNE):
        for y in range(RANGEE):
            # Si COLONNE et RANGEE sont pairs ou COLONNE et RANGEE sont impairs, on attribue la couleur bleue
            if (x % 2 == 0 and y % 2 == 0) or (x % 2 != 0 and y % 2 != 0):
                couleur = '#8CDAF5'
            else:
                couleur = '#FFFFFF'
            # On dessine un rectangle sur le canva
            dessiner_objet(x, y, couleur)

def dessiner_objet(colonne, rangee, couleur):
    """ fnc : fonction qui permet de dessiner des cases dans le canva à une certaine position
        args : int, int, str
        return : none
    """
    x1 = colonne * TAILLE_PIXEL
    y1 = rangee * TAILLE_PIXEL
    x2 = (colonne + 1) * TAILLE_PIXEL
    y2 = (rangee + 1) * TAILLE_PIXEL
    # On dessine l'objet de (x1, y1) à (x2, y2) avec une couleur de fond et une couleur de bordure
    canva.create_rectangle(x1, y1, x2, y2, fill = couleur, outline = "grey")

def dessiner_serpent():
    """ fnc : fonction qui permet de dessiner le corps du serpent à l'aide de la fonction dessiner_objet(...)
        args :
        return : none
    """
    global serpent_coordonnees
	# On dessine le serpent sur la grille avec des cases bleues
    for coordonné in serpent_coordonnees:
        dessiner_objet(coordonné[0],coordonné[1],"blue")

def dessiner_nourriture():
    """ fnc : créer une nouriture dans la grille
        args : none
        return : list bool
    """
    global nourriture_positionnee, nourriture_coordonnees, serpent_coordonnees
    # Si il y a déjà de la nourriture sur la grille on quitte la fonction.
    if nourriture_positionnee == True:
        return
	# On détermine une position aléatoirement
    else:
        x = random.randint(0, RANGEE-1)
        y = random.randint(0, COLONNE-1)
    # Cependant si la nourriture est sur le serpent on la change de place
        while serpent_coordonnees == nourriture_coordonnees:
            x = random.randint(0, RANGEE-1)
            y = random.randint(0, COLONNE-1)

    # On dessine la nourriture sur la grille avec une case rouge
    dessiner_objet(x, y, "red")
    # On n'oubli pas de mettre à jour la variable nourriture_positionnee
    nourriture_coordonnees = [x, y]
    nourriture_positionnee = True

def boucle_jeu():
    """ fnc : la boucle du jeu qui tourne en continue tant que le joueur n'a pas perdu, met a jour la fenêtre, les mouvements du serpent, l'affichage de nourriture... heberge une condition de fin.
        args : none
        return :
    """
    global score
    window.update()
    # On récupère la position de la tête et les positions du corps
    tete = serpent_coordonnees[0]
    corps = serpent_coordonnees[1:]
    # Si la position de la tête est déjà contenu dans la liste (cela signifie qu'on chevauche le corps du serpent) et que le score est > 0
    # On affiche une boolbox avec le score et 2 boutons : soit on ferme la fenêtre soit on relance la fonction recommencer_partie()
    if tete in corps and score > 0:
        choix = boolbox(msg="Ton score actuel est de " + str(score), title="Fin du jeu", choices=("Quitter","Réessayer"))
        if choix == True:
            window.destroy()
        else:
            recommencer_partie()
            score = 0
            text.set("Ton score actuel est de "+ str(score))
        return

    dessiner_nourriture() # On redessine une nourriture si besoin
    snake = bouger_serpent()
    window.after(200, boucle_jeu) # rafraichissement de la fenetre
    return

def bouger_serpent():
    """ fnc : permet de bouger, indique les coordonées et héberge une des conditions de défaite + écran de fin
        args : none
        return : none
    """
    global score, nourriture_positionnee, serpent_coordonnees, serpent_direction, window

    # On ajoute une case devant le serpent pour le faire avancer
    # On déclare des nouvelles coordonnées qu'on va réellement calculer juste après en fonction des coordonnées actuelles et de la direction
    nouvelles_coordonnees = [0, 0]
    tete = serpent_coordonnees[0]
    # Si la direction n'est pas pair (verticale)
    if serpent_direction % 2 == 1:
        # x = les coordonnées actuel de la tête du serpent en x (elle ne bouge pas car on se déplace verticalement)
        x = serpent_coordonnees[0][0]
        # y = les coordonnées actuels de la tête du serpent en y + la direction
        y = serpent_coordonnees[0][1] + serpent_direction

    # Sinon, si elle est pair (horizontale)
    else:
        # x = les coordonnés actuels de la tête du serpend en x plus la direction qu'il faut diviser par 2 car sinon ils sont espacés d'un carreau
        x = serpent_coordonnees[0][0] + serpent_direction/2
        # y = les coordonnées acutels du serpent en y (elle ne bouge pas car on se déplace horizontalement)
        y = serpent_coordonnees[0][1]
    # On insère les nouvelles coordonnées au début de la liste des coordonnées du serpent
    nouvelles_coordonnees = [x,y]
    serpent_coordonnees.insert(0, nouvelles_coordonnees)

    # Si cette novelle case nous fait taper contre un mur on a perdu
    for coordonnes in serpent_coordonnees:
        if coordonnes[0] not in range(COLONNE) or coordonnes[1] not in range(RANGEE):
            # On affiche une boolbox avec le score et 2 boutons : soit on ferme la fenêtre soit on relance la fonction recommencer_partie()
            choix = boolbox(msg="Ton score actuel est de " + str(score), title="Fin du jeu", choices=("Quitter","Réessayer"))
            if choix == True:
                window.destroy()
            else:
                recommencer_partie()
                score = 0
                text.set("Ton score actuel est de "+ str(score))
            return

    # Pour effacer la queue du serpent, on reprend le principe de la fonction pour dessiner la grille, si x est pair ET y est pair OU x est impair ET y est impair alors le carré est bleu.
    if (serpent_coordonnees[-1][0] % 2 == 0 and serpent_coordonnees[-1][1] % 2 == 0) or (serpent_coordonnees[-1][0] % 2 != 0 and serpent_coordonnees[-1][1] % 2 != 0):
        couleur = '#8CDAF5'
        dessiner_objet(serpent_coordonnees[len(serpent_coordonnees) - 1][0], serpent_coordonnees[len(serpent_coordonnees) - 1][1], couleur)
    else:
        couleur = '#FFFFFF'
        dessiner_objet(serpent_coordonnees[len(serpent_coordonnees) - 1][0], serpent_coordonnees[len(serpent_coordonnees) - 1][1], couleur)

    # Si on mange la nourriture on redessine un carré bleu aux coordonnées de la tête du serpent calculée au-dessus, on réinitialise la variable nourriture_positionnee et on met à jour le score et son affichage
    if nourriture_coordonnees[0] == serpent_coordonnees[0][0] and nourriture_coordonnees[1] == serpent_coordonnees[0][1]:
        dessiner_objet(serpent_coordonnees[0][0], serpent_coordonnees[0][1], "blue")
        score += 1
        text.set("Ton score actuel est de "+ str(score))
        nourriture_positionnee = False
    else:
        # Sinon on redessine un carré bleu aux coordonnées de la tête du serpent calculée au-dessus
        dessiner_objet(nouvelles_coordonnees[0], nouvelles_coordonnees[1], "blue")
        # On supprime le dernier élément de la liste des coordonnées du serpent
        del serpent_coordonnees[len(serpent_coordonnees) - 1]

    return serpent_coordonnees

def deplacer(event):
    """ fnc : permet au serpent de bouger via les 4 flèches directionneles, utilise les canva.bind de la fonction 'creer grilles'
              Attention : le serpent ne peut pas revenir sur ses "pas"
        args : event
        return : none
    """
    global serpent_direction, serpent_coordonnees
    # On récupère le nom de la touche qui a créée l'évènement
    touche = event.keysym
    # Si la touche 'Up' est active et que le sens de direction n'est pas égal à 1 on met le sens de direction à -1
    if touche == 'Up' or touche == "z" and serpent_direction != 1:
        serpent_direction = -1
    # Sinon si, on fait de même pour chacune des touches
    elif touche == 'Down' or touche == "s" and serpent_direction != -1:
        serpent_direction = 1
    elif touche == 'Right' or touche == "d" and serpent_direction != -2:
        serpent_direction = 2
    elif touche == 'Left' or touche == "q" and serpent_direction != 2:
        serpent_direction = -2

def recommencer_partie():
    """ fnc : permet de recommencer la partie
        args :
        return : none
    """
    # réinitialisation de toutes les variables globales liées au jeu.
    global nourriture_positionnee, nourriture_coordonnees, serpent_direction, serpent_coordonnees, score
    nourriture_positionnee = False
    nourriture_coordonnees = [0, 0]
    serpent_direction = 2 # -1 en haut, 1 en bas, -2 à gauche et 2 à droite
    serpent_coordonnees = [[4, 16], [3, 16], [2, 16]] # Position du serpent à l'origine (Tête en position 0)
    score = 0


    for x in range(COLONNE):
        for y in range(RANGEE):
            # Si COLONNE et RANGEE sont pairs ou COLONNE et RANGEE sont impairs, on attribue la couleur bleue
            if (x % 2 == 0 and y % 2 == 0) or (x % 2 != 0 and y % 2 != 0):
                couleur = '#8CDAF5'
            else:
                couleur = '#FFFFFF'
            # On dessine un rectangle sur le canva
            dessiner_objet(x, y, couleur)

    text = tkinter.StringVar()
    score = 0
    text.set("Ton score actuel est de "+ str(score))

    # On crée la grille du jeu
    creer_grille()
    # Après avoir dessiner la grille on dessine le serpent
    dessiner_serpent()
    # Et on dessine la nourriture
    dessiner_nourriture()
    # On lance la boucle du jeu
    boucle_jeu()

# ------ Programme principal ------

# On crée une fenêtre à l'aide de la bibliothèque tkinter et on lui donne un titre
window = tkinter.Tk()
window.title("Micro-Projet Snake")

# On crée une variables de contrôle pour afficher le score et qui sera partagée entre plusieurs widgets tkinter
score = 0
text = tkinter.StringVar()
text.set("Ton score actuel est de "+ str(score)) # tous les widgets reliés à cette variable de contrôle sont automatiquement mis à jour sur l’écran.

# On crée un label pour afficher le contenu de la variable de controle en haut de la fenêtre
label = tkinter.Label(textvariable = text)
label.pack() # On l'ajoute à la fenêtre

# On crée un canevas dans la fenêtre aux bonnes dimensions
canva = tkinter.Canvas(window, width = LARGEUR, height = HAUTEUR) # Un caneva est une zone rectangulaire destinée à contenir des dessins ou d’autres figures complexes
canva.pack() # On l'ajoute à la fenêtre
canva.focus_set() # On place le focus sur la fenêtre

# On utilise la méthode bind pour lier un événement au canva
# Dès qu'une des touches directionnels sera appuyé, la fonction deplacer sera appelé avec l'argument event prédéfini par la méthode "bind"
canva.bind("<KeyPress-Left>", deplacer)
canva.bind("<KeyPress-Right>", deplacer)
canva.bind("<KeyPress-Up>", deplacer)
canva.bind("<KeyPress-Down>", deplacer)

canva.bind("<KeyPress-q>", deplacer)
canva.bind("<KeyPress-d>", deplacer)
canva.bind("<KeyPress-z>", deplacer)
canva.bind("<KeyPress-s>", deplacer)

# On crée la grille du jeu
creer_grille()
# Après avoir dessiner la grille on dessine le serpent
dessiner_serpent()
# Et on dessine la nourriture
dessiner_nourriture()
# On lance la boucle du jeu
boucle_jeu()
# On affiche la fenetre en boucle
window.mainloop()

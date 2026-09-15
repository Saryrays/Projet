# Bibliothèques utilisées

from PIL import Image # PIL est la bibliothèque spécialisée dans le traitement de l'image
from io import BytesIO # module pour transformer en bytes
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import cv2
import os
import random
from matplotlib.widgets import Button
import pprint

# Affiche côte-à-côte l'image originale et l'image transformée

def affichage(img_modif, nom) :
    """
    prend en paramètre l'image modifier ainsi que son nom pour afficher dans une fenètre l'image original et celle modifier
    """
    plt.subplot(1,2,1)
    plt.imshow(image_simul, cmap='gray')
    plt.title("Image originale")
    plt.subplot(1,2,2)
    plt.imshow(img_modif, cmap='gray')
    plt.title(nom)
    plt.show()



def protanopie(img_origine):
    """
    renvoie l'image modifiée pour la vue d'une personne atteinte de protanopie
    """
    img_copie = np.copy(img_origine) # On fait une copie de l'original
    for i in range(hauteur):
        for j in range(largeur):
            r, v, b, a = img_copie[i, j]
##            Transformation des pixels

            r = 0



##            Reconstitution de l'image
            img_copie[i, j] = (r, v, b, a)
    return img_copie

def protanomalie(img_origine):
    """
    renvoie l'image modifiée pour la vue d'une personne atteinte de protanomalie
    """
    img_copie = np.copy(img_origine) # On fait une copie de l'original
    for i in range(hauteur):
        for j in range(largeur):
            r, v, b, a = img_copie[i, j]

##            Transformation des pixels

            r = r//2

##            Reconstitution de l'image
            img_copie[i, j] = (r, v, b, a)
    return img_copie

def deutéranopie(img_origine):
    """
    renvoie l'image modifiée pour la vue d'une personne atteinte de deutéranopie
    """
    img_copie = np.copy(img_origine) # On fait une copie de l'original
    for i in range(hauteur):
        for j in range(largeur):
            r, v, b, a = img_copie[i, j]

##            Transformation des pixels

            v = 0


##            Reconstitution de l'image
            img_copie[i, j] = (r, v, b, a)
    return img_copie

def deutéranomalie(img_origine):
    """
    renvoie l'image modifiée pour la vue d'une personne atteinte de deutéranomalie
    """
    img_copie = np.copy(img_origine) # On fait une copie de l'original
    for i in range(hauteur):
        for j in range(largeur):
            r, v, b, a = img_copie[i, j]

##            Transformation des pixels

            v = v//2

##            Reconstitution de l'image
            img_copie[i, j] = (r, v, b, a)
    return img_copie

def tritanopie(img_origine):
    """
    renvoie l'image modifiée pour la vue d'une personne atteinte de tritanopie
    """
    img_copie = np.copy(img_origine) # On fait une copie de l'original
    for i in range(hauteur):
        for j in range(largeur):
            r, v, b, a = img_copie[i, j]

##            Transformation des pixels

            b = 0


##            Reconstitution de l'image
            img_copie[i, j] = (r, v, b, a)
    return img_copie

def tritanomalie(img_origine):
    """
    renvoie l'image modifiée pour la vue d'une personne atteinte de tritanomalie
    """
    img_copie = np.copy(img_origine) # On fait une copie de l'original
    for i in range(hauteur):
        for j in range(largeur):
            r, v, b, a = img_copie[i, j]

##            Transformation des pixels

            b = b//2

##            Reconstitution de l'image

            img_copie[i, j] = (r, v, b, a)

    return img_copie

def achromatopsie(img_origine):
    """
    renvoie l'image modifiée pour la vue d'une personne atteinte de achromatopsie
    """
    img_copie = np.copy(img_origine) # On fait une copie de l'original
    for i in range(hauteur):
        for j in range(largeur):
            r, v, b, a = img_copie[i, j]
            Luminance = 0.2126*r+0.7152*v+0.0722*b

##            Transformation des pixels

            r = Luminance

            v = Luminance

            b = Luminance


##            Reconstitution de l'image
            img_copie[i, j] = (r, v, b, a)

    return img_copie


class TestDaltonisme:

    def __init__(self, dico_images):
        self.data = list(dico_images.items())
        random.shuffle(self.data)
        self.index = 0
        # score obtenu
        self.scores = {
            "Normal": 0,
            "Protanopie": 0,
            "Deuteranopie": 0,
            "Tritanopie": 0
        }
        # nombre total de questions correspondant à chaque profil
        self.total_questions = len(self.data)
        self.reponse_utilisateur = []
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        plt.subplots_adjust(bottom=0.25)
        self.choix = ["0", "1", "2", "3", "4",
                       "5", "6", "7", "8", "9", "Rien"]
        self.boutons = []
        for i, val in enumerate(self.choix):
            ax_btn = plt.axes([0.02 + i * 0.085, 0.05, 0.07, 0.07])
            btn = Button(ax_btn, val)
            btn.on_clicked(self.make_callback(val))
            self.boutons.append(btn)
        self.afficher_image()

    def make_callback(self, val):
        def callback(event):
            self.choisir_valeur(val)
        return callback

    def choisir_valeur(self, val):
        """
        enregistre les réponses choisies par l'utilisateur
        """
        # pour avoir 2 réponses
        if len(self.reponse_utilisateur) < 2:
            self.reponse_utilisateur.append(val)
        # 2 réponses = validation
        if len(self.reponse_utilisateur) == 2:
            self.verifier_reponse()
            self.reponse_utilisateur = []


    def afficher_image(self):
        """
        affiche l'image du test Ishihara
        """
        self.ax.clear()
        # affiche le résultat
        if self.index >= len(self.data):
            self.afficher_resultats()
            return
        chemin, _ = self.data[self.index]
        img = cv2.imread(chemin)
        if img is None:
            print(f"Erreur chargement : {chemin}")
            self.index += 1
            self.afficher_image()
            return
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.ax.imshow(img)
        self.ax.set_title(
            f"Image {self.index + 1}/{len(self.data)}\n"
            "Choisis 2 réponses"
        )
        self.ax.axis('off')
        plt.draw()


    def verifier_reponse(self):
        """
        vérifie les réponse donné grâce à la liste des solutions
        """
        _, bonnes_reponses = self.data[self.index]
        reponse = sorted(self.reponse_utilisateur)
        # Vérifie chaque profil
        for profil, bonne_rep in bonnes_reponses.items():
            if reponse == sorted(bonne_rep) and profil == "Normal":
                self.scores[profil] += 1
                break
            elif reponse == sorted(bonne_rep):
                self.scores[profil] += 1
        self.index += 1
        self.afficher_image()

    def afficher_resultats(self):
        """
        Affiche votre résultat obtenue au test à la fin de celui-ci
        """
        self.ax.clear()
        resultats = {}
        for profil, score in self.scores.items():
            pourcentage = round((score / self.total_questions) * 100,1)
            resultats[profil] = pourcentage

        type_probable = max(resultats, key=resultats.get)
        texte = "TEST TERMINÉ\n\n"
        for profil, pourcentage in resultats.items():
            texte += f"{profil} : {pourcentage}%\n"
        texte += f"\nType probable : {type_probable}"
        self.ax.text(
            0.5,
            0.5,
            texte,
            ha='center',
            va='center',
            fontsize=12
        )
        self.ax.axis('off')

        self.btn_restart_ax = plt.axes([0.20, 0.2, 0.3, 0.05])

        self.btn_restart = Button(
            self.btn_restart_ax,
            "Recommencer",
            color='lime'
        )

        self.btn_restart.on_clicked(self.recommencer_test)

        self.btn_quit_ax = plt.axes([0.50, 0.2, 0.3, 0.05])

        self.btn_quit = Button(
            self.btn_quit_ax,
            "Quitter",
            color='salmon'
        )

        self.btn_quit.on_clicked(lambda event: plt.close(self.fig))
        plt.draw()

    def recommencer_test(self, event=None):
        """
        fonction permettant de recommencer le test si choisi
        """
        # Remet tout à 0
        self.scores = {
            "Normal": 0,
            "Protanopie": 0,
            "Deuteranopie": 0,
            "Tritanopie": 0
        }
        self.index = 0
        self.reponse_utilisateur = []
        random.shuffle(self.data)
        if hasattr(self, 'btn_restart_ax'):
            self.btn_restart_ax.remove()
            self.btn_quit_ax.remove()
        self.afficher_image()


def menu():
    """
    appel des fonctions correspondantes choisies par l'utilisateur
    """
    # choix des modes
    if(combobox.get() == "Protanopie"):
        image_protanopie = protanopie(image_simul)
        affichage(image_protanopie, "Protanopie")
    if(combobox.get() == "Protanomalie"):
        image_protanomalie = protanomalie(image_simul)
        affichage(image_protanomalie, "Protanomalie")
    if(combobox.get() == "Deutéranopie"):
        image_deutéranopie = deutéranopie(image_simul)
        affichage(image_deutéranopie,"Deutéranopie" )
    if(combobox.get() == "Deutéranomalie"):
        image_deutéranomalie = deutéranomalie(image_simul)
        affichage(image_deutéranomalie,"Deutéranomalie" )
    if(combobox.get() == "Tritanopie"):
        image_tritanopie = tritanopie(image_simul)
        affichage(image_tritanopie, "Tritanopie")
    if(combobox.get() == "Tritanomalie"):
        image_tritanomalie = tritanomalie(image_simul)
        affichage(image_tritanomalie, "Tritanomalie")
    if(combobox.get() == "Achromatopsie"):
        image_achromatopsie = achromatopsie(image_simul)
        affichage(image_achromatopsie,"Achromatopsie" )
    if(combobox.get() == "Jeu de test"):
        TestDaltonisme(dico_images)
        plt.show()
    elif(combobox.get() == "Quitter"):
        fenetre.destroy()

image_simul = Image.open("imagedetest.png") # donner le chemin complet si pas dans le même répertoire
# image contient un tableau de quadruplets donnant les valeurs RVBA de chaque pixel
largeur, hauteur = image_simul.size # récupère les dimensions de l'image
dossier = "images"



dico_images = {}
normal = [["1","2"], ["5","Rien"], ["7","Rien"], ["6","7"], ["7","3"],["Rien","Rien"], ["Rien", "Rien"], ["2","6"], ["4","2"], ["8", "Rien"], ["2","9"],["5","Rien"], ["3","Rien"],["1","5"], ["7","4"], ["6","Rien"], ["4","5"]]
protanopie_dic = [["1","2"], ["Rien","Rien"], ["7","Rien"], ["6","7"], ["Rien","Rien"],["5","Rien"], ["4", "5"], ["6","Rien"], ["2","Rien"], ["3", "Rien"], ["7","0"],["2","Rien"], ["5","Rien"],["1","7"], ["2","1"], ["Rien","Rien"], ["Rien","Rien"]]
deuteranopie_dic = [["1","2"], ["Rien","Rien"], ["7","Rien"], ["6","7"], ["Rien","Rien"],["5","Rien"], ["4", "5"], ["2","Rien"], ["4","Rien"], ["3", "Rien"], ["7","0"],["2","Rien"], ["5","Rien"],["1","7"], ["2","1"], ["Rien","Rien"], ["Rien","Rien"]]
tritanopie_dic =[["1","2"], ["5","Rien"], ["Rien","Rien"], ["Rien","Rien"], ["7","3"],["Rien","Rien"], ["Rien", "Rien"], ["2","6"], ["4","2"], ["8", "Rien"], ["2","9"],["5","Rien"], ["3","Rien"],["1","5"], ["7","4"], ["6","Rien"], ["4","5"]]
i = 0

## Permet de créer les listes des réponses attendues
for f in sorted(os.listdir("images")):
    if f.endswith(".png"):
        chemin = os.path.join("images", f)
        dico_images[chemin] = {
            "Normal": normal[i],
            "Protanopie": protanopie_dic[i],
            "Deuteranopie": deuteranopie_dic[i],
            "Tritanopie": tritanopie_dic[i],

        }
    i = i+1



fenetre = tk.Tk()
fenetre.title("Micro-projet Images")
fenetre.geometry("%dx%d%+d%+d" % (250,100,(fenetre.winfo_screenwidth()-250)//2,(fenetre.winfo_screenheight()-100)//2)) # Taille et position de la fenetre
label = tk.Label(fenetre,text = "Choisir une action")
label.pack()
combobox = ttk.Combobox(fenetre, values=["Choisir une action","Protanopie","Protanomalie", "Deutéranopie","Deutéranomalie", "Tritanopie","Tritanomalie", "Achromatopsie","Jeu de test", "Quitter"])
combobox.current(0)
combobox.pack()
bouton_ok = tk.Button(fenetre, text='OK', command=menu)
bouton_ok.pack()
fenetre.mainloop()



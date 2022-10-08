"""Ce fichier définit des fonctions utiles pour le programme pendu.
On utilise les données du programme contenues dans donnees.py"""
import os
import pickle
from random import choice, randrange
from donnees import *

# Gestion des scores

def recup_scores():

    """Cette fonction récupère les scores enregistrés si le fichier existe.
    Dans tous les cas, on renvoie un dictionnaire, soit l'objet dépicklé, soit un dictionnaire vide.
    On s'appuie sur nom_fichier_scores défini dans donnees.py"""

    if os.path.exists(nom_fichier_scores): # Le fichier existe
    # On le récupère
        fichier_scores = open(nom_fichier_scores, "rb")
        mon_depickler = pickle.Unpickler(fichier_scores)
        scores = mon_depickler.load()
        fichier_scores.close()
    else: # Le fichier n'existe pas
        scores = {}
    return scores

def enregistrer_scores(scores):

    """Cette fonction se charge d'enregistrer les scores dans le fichier nom_fichier_scores.
    Elle reçoit en paramètre le dictionnaire des scores à enregistrer"""

    fichier_scores = open(nom_fichier_scores, "wb") # On écrase les anciens scores
    mon_pickler = pickle.Pickler(fichier_scores)
    mon_pickler.dump(scores)
    fichier_scores.close()

#
# Fonctions gérant les éléments saisis par l'utilisateur
#

def recup_nom_utilisateur():
    """Fonction chargée de récupérer le nom de l'utilisateur.
    Le nom de l'utilisateur doit être composé de 4 caractères minimum, chiffres et lettres exclusivement.
    Si ce nom n'est pas valide, on appelle récursivement la fonction pour en obtenir un nouveau"""
    
    nom_utilisateur = input("Tapez votre nom: ")

    # On met la première lettre en majuscule et les autres en minuscules
    nom_utilisateur = nom_utilisateur.capitalize()

    if not nom_utilisateur.isalnum() or len(nom_utilisateur)<4:
        print("Ce nom est invalide.")
        
        # On appelle de nouveau la fonction pour avoir un autre nom
        return recup_nom_utilisateur()
    else:
        return nom_utilisateur

def recup_lettre():

    """Cette fonction récupère une lettre saisie par l'utilisateur. Si la chaîne récupérée n'est pas une lettre,
    on appelle récursivement la fonction jusqu'à obtenir une lettre"""

    lettre = input("Tapez une lettre: ")
    lettre = lettre.lower()
    if len(lettre)>1 or not lettre.isalpha():
        print("Vous n'avez pas saisi une lettre valide.")
        return recup_lettre()
    else:
        return lettre

# Fonctions du jeu de pendu

def choisir_mot(): 
    """Cette fonction renvoie le mot choisi dans la liste des mots liste_mots.
    On utilise la fonction choice du module random (voir l'aide)."""
    word = randrange(len(liste_mots))
    return liste_mots[word]

def recup_mot_masque(mot_complet, lettres_trouvees):

    """Cette fonction renvoie un mot masqué tout ou en partie, en fonction :
    - du mot d'origine (type str)
    - des lettres déjà trouvées (type list)
    On renvoie le mot d'origine avec des * remplaçant les lettres que l'on n'a pas encore trouvées."""

    mot_masque = ""
    for lettre in mot_complet:
        if lettre in lettres_trouvees:
            mot_masque += lettre
        else:
            mot_masque += "*"
    return mot_masque

def ajouter_mot(liste_mots):
    #Cette foction permet aux gagnant d'aujouter de nouveaux mots

    nouveau_mot = input("Souhaitez vous enrichir notre dictionnaire? (o/n) ")
    if nouveau_mot == 'o':
        nouveau_mot = input("Tapez votre mot: ")
        if nouveau_mot in liste_mots:
            print("Merci mais votre mot fait déjà partir de notre jeu")
        else:
            liste_mots.append(nouveau_mot)
            print("Votre mot a été ajouté avec succès")

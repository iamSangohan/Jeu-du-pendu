"""Ce fichier définit des fonctions utiles pour le programme pendu.
On utilise les données du programme contenues dans donnees.py"""
import os
import pickle
from random import randrange
import time
from donnees import *
import Pyro4


class Client():
    username = ""
    score = 0
    
    def enregistrement_joueur(self, nom, jeu):
        """Fonction chargée de récupérer le nom de l'utilisateur.
        Le nom de l'utilisateur doit être composé de 4 caractères minimum, chiffres et lettres exclusivement.
        Si ce nom n'est pas valide, on appelle récursivement la fonction pour en obtenir un nouveau"""
        
        # On met la première lettre en majuscule et les autres en minuscules
        username = nom.capitalize()

        if not username.isalnum() or len(username)<4:
            print("Ce nom est invalide.")
            
            # On appelle de nouveau la fonction pour avoir un autre nom
            return self.recup_nom_utilisateur()
        else:
            jeu.inscription_au_jeu()
            jeu.attente_joueur()
            return username
        
    
    
    
    

@Pyro4.expose
class Server():
    
    joueurs = []
    scores = []
    gagne = []
    
    def start(self):
        ok = False
        nbjoueurs = self.joueurs.count()
        if nbjoueurs == 3:
            ok = True
        return ok
    
    def attente_joueur(self):
        nbjoueurs = self.joueurs.count()
        while nbjoueurs != 3:
            print('En attente des joueurs ({}/3)...'.format(nbjoueurs),end='\r')
            time.sleep(1)
        #print('Joueur {} connecté !'.format(gm.player()['name']))
        print("Le match va commencer !")
        
    
    def afficher_scores(self):
        for joueur, score in self.joueurs, self.scores :
            print("Joueur {0}: {1} point(s)".format(joueur, score))
        print("--------------------------------------------------------------------------")
    
    
    # def gagnant(self):
    #     for joueur in self.joueurs :
    
    # Gestion des scores

    def recup_scores(self):

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

    def enregistrer_scores(self, scores):

        """Cette fonction se charge d'enregistrer les scores dans le fichier nom_fichier_scores.
        Elle reçoit en paramètre le dictionnaire des scores à enregistrer"""

        fichier_scores = open(nom_fichier_scores, "wb") # On écrase les anciens scores
        mon_pickler = pickle.Pickler(fichier_scores)
        mon_pickler.dump(scores)
        fichier_scores.close()

    # Fonctions gérant les éléments saisis par l'utilisateur

    def inscription_au_jeu(self, username):
        """Fonction chargée de récupérer le nom de l'utilisateur.
        Le nom de l'utilisateur doit être composé de 4 caractères minimum, chiffres et lettres exclusivement.
        Si ce nom n'est pas valide, on appelle récursivement la fonction pour en obtenir un nouveau"""
        
        # On met la première lettre en majuscule et les autres en minuscules
        self.joueurs.append(username)
        self.scores.append(0)
        self.gagne.append(False)

    def recup_lettre(self, saisi):

        """Cette fonction récupère une lettre saisie par l'utilisateur. Si la chaîne récupérée n'est pas une lettre,
        on appelle récursivement la fonction jusqu'à obtenir une lettre"""

        lettre = saisi.lower()
        if len(lettre)>1 or not lettre.isalpha():
            print("Vous n'avez pas saisi une lettre valide.")
            return self.recup_lettre()
        else:
            return lettre

    # Fonctions du jeu de pendu

    def choisir_mot(self, user): 
        """Cette fonction renvoie le mot choisi dans la liste des mots liste_mots.
        On utilise la fonction choice du module random (voir l'aide)."""
        word = randrange(len(liste_mots))
        return liste_mots[word]

    def recup_mot_masque(self, mot_complet, lettres_trouvees):

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

    def ajouter_mot(self, liste_mots):
        #Cette foction permet aux gagnant d'aujouter de nouveaux mots

        nouveau_mot = input("Souhaitez vous enrichir notre dictionnaire? (o/n) ")
        if nouveau_mot == 'o':
            nouveau_mot = input("Tapez votre mot: ")
            if nouveau_mot in liste_mots:
                print("Merci mais votre mot fait déjà partir de notre jeu")
            else:
                liste_mots.append(nouveau_mot)
                

def main():
    dmn=Pyro4.Daemon(host="0.0.0.0", port=9091)
    game = Server()
    Pyro4.Daemon.serveSimple(
        {game : 'example.pendu'}, 
        daemon=dmn,
        ns=False, 
    )
    Pyro4.Daemon.serveSimple(
        {Client : 'example.joueur'}, 
        daemon=dmn,
        ns=False, 
    )

if __name__=="__main__":
    main()

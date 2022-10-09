import sys
from donnees import *
from fonctions import *
import Pyro4
import Pyro4.util

sys.excepthook = Pyro4.util.excepthook

jeu = Pyro4.Proxy("PYRONAME:example.pendu")

# On récupère les scores de la partie
scores = jeu.recup_scores()

# On récupère un nom d'utilisateur
utilisateur = jeu.recup_nom_utilisateur()

# Si l'utilisateur n'a pas encore de score, on l'ajoute
if utilisateur not in scores.keys():
    scores[utilisateur] = 0 # 0 point pour commencer

# Notre variable pour savoir quand arrêter la partie
continuer_partie = 'o'
while continuer_partie != 'n':
    print("Joueur {0}: {1} point(s)".format(utilisateur, scores[utilisateur]))
    print("--------------------------------------------------------------------------")
    mot_a_trouver = jeu.choisir_mot()
    lettres_trouvees = []
    mot_trouve = jeu.recup_mot_masque(mot_a_trouver, lettres_trouvees)
    nb_chances = nb_coups
    while mot_a_trouver!=mot_trouve and nb_chances>0:
        print("Mot à trouver {0} (encore {1} chances)".format(mot_trouve, nb_chances))
        lettre = jeu.recup_lettre()
        if lettre in lettres_trouvees: # La lettre a déjà été choisie
            print("Vous avez déjà choisi cette lettre.")
        elif lettre in mot_a_trouver: # La lettre est dans le mot à trouver
            lettres_trouvees.append(lettre)
            print("Bien joué.")
            nb_chances = nb_coups
        else:
            nb_chances -= 1
            print("... non, cette lettre ne se trouve pas dans le")
        mot_trouve = jeu.recup_mot_masque(mot_a_trouver, lettres_trouvees)

        # A-t-on trouvé le mot ou nos chances sont-elles épuisées ?
        if mot_a_trouver==mot_trouve:
            print("Félicitations ! Vous avez trouvé le mot {0}.".format(mot_a_trouver))
        if mot_a_trouver != mot_trouve and nb_chances == 0:
            print("PENDU !!! Vous avez perdu.")
            print("\n Le mot était: {0}.".format(mot_a_trouver))

        # On met à jour le score de l'utilisateur
        scores[utilisateur] += nb_chances
    print("--------------------------------------------------------------------------")
    continuer_partie = input("Souhaitez-vous continuer la partie (O/N) ?")
    continuer_partie = continuer_partie.lower()

jeu.ajouter_mot(liste_mots)

# La partie est finie, on enregistre les scores
jeu.enregistrer_scores(scores)

# On affiche les scores de l'utilisateur
print("Vous finissez la partie avec {0} points.".format(scores[utilisateur]))
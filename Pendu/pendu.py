import pygame
import random

# Listes de mots selon les niveaux de difficulté
Mots_facile = ("kiwi", "acte", "agar", "eros", "yeti", "zeub")
Mots_moyen = ("ecoduc", "abacot", "atroce", "baille", "zyclon", "yukata")
Mots_difficile = ("aalénien", "azraqite", "badigeon", "calamite", "zoulette", "xanthium")

# Fonction pour choisir un mot selon le niveau de difficulté
def choisir_mot():
    niveau = input("Choisissez un niveau de difficulté (facile, moyen, difficile) : ").strip().lower()
    if niveau == "facile":
        mot = random.choice(Mots_facile)
    elif niveau == "moyen":
        mot = random.choice(Mots_moyen)
    elif niveau == "difficile":
        mot = random.choice(Mots_difficile)
    else:
        print("Niveau invalide. Veuillez choisir entre facile, moyen ou difficile.")
        return choisir_mot()
    
    return mot

# Fonction de jeu du pendu
def pendu():
    mot_choisi = choisir_mot()  # Choisir un mot
    lettres_trouvees = ["_"] * len(mot_choisi)  # Masquer les lettres
    essais_restants = 6  # Nombre d'essais

    print("Bienvenue dans le jeu du pendu !")
    print("Pour chaque tentative incorrecte, vous perdez 1 essai.")
    print("Si vous devinez le mot entier et que c'est incorrect, vous perdez 2 essais.")
    print(" ".join(lettres_trouvees))
    
    # Boucle de jeu
    while essais_restants > 0 and "_" in lettres_trouvees:
        choix = input("Devinez une lettre ou essayez de deviner le mot entier : ").strip().lower()

        # Vérifier si l'utilisateur a deviné le mot entier
        if len(choix) > 1:  # Si l'utilisateur entre plus d'une lettre, c'est une supposition de mot
            if choix == mot_choisi:
                lettres_trouvees = list(mot_choisi)  # Révéler toutes les lettres
                print("Félicitations ! Vous avez deviné le mot entier :", mot_choisi)
                break
            else:
                essais_restants -= 2  # Perte de 2 essais pour une supposition incorrecte
                print(f"Ce n'est pas le bon mot. Vous perdez 2 essais. Il vous reste {essais_restants} essais.")
        else:
            # Deviner une seule lettre
            lettre = choix
            if lettre in mot_choisi:
                for index, char in enumerate(mot_choisi):
                    if char == lettre:
                        lettres_trouvees[index] = lettre
                print("Bonne lettre !")
            else:
                essais_restants -= 1  # Perte de 1 essai pour une lettre incorrecte
                print(f"Lettre incorrecte. Il vous reste {essais_restants} essais.")

        # Afficher l'état actuel des lettres trouvées
        print(" ".join(lettres_trouvees))

    # Fin de la partie
    if "_" not in lettres_trouvees:
        print("Félicitations ! Vous avez trouvé le mot :", mot_choisi)
    else:
        print("Dommage, vous avez perdu. Le mot était :", mot_choisi)

# Lancer le jeu
pendu()

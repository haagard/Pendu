import pygame
import random

# Initialisation de Pygame
pygame.init()

# Taille de la fenêtre (plein écran)
WIDTH, HEIGHT = 1080, 720
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Jeu du Pendu")

# Couleurs et polices
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
font = pygame.font.Font(None, 36)

Mots_facile = ("kiwi", "acte", "agar", "eros", "yeti", "zeub", "abat", "fuir", "funs", "fume")
Mots_moyen = ("ecoduc", "abacot", "atroce", "baille", "zyclon", "yukata")
Mots_difficile = ("aalénien", "azraqite", "badigeon", "calamite", "zoulette", "xanthium")

# Variables de jeu
lettres_trouvees = []
essais_restants = 10
lettres_essayees = []
mot_choisi = ""
choix_difficulte = False  # Drapeau pour vérifier si la difficulté a été choisie

# Contrôle de la fréquence de rafraîchissement
clock = pygame.time.Clock()
FPS = 30

# Fonction pour afficher des boutons pour la sélection de la difficulté
def affichage_difficulte():
    win.fill(WHITE)
    texte = font.render("Choisissez un niveau de difficulté :", True, BLACK)
    win.blit(texte, (WIDTH // 2 - texte.get_width() // 2, HEIGHT // 4))

    # Boutons de difficulté
    bouton_facile = pygame.Rect(WIDTH // 4 - 50, HEIGHT // 2, 100, 50)
    bouton_moyen = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2, 100, 50)
    bouton_difficile = pygame.Rect(3 * WIDTH // 4 - 50, HEIGHT // 2, 100, 50)

    pygame.draw.rect(win, BLUE, bouton_facile)
    pygame.draw.rect(win, BLUE, bouton_moyen)
    pygame.draw.rect(win, BLUE, bouton_difficile)

    texte_facile = font.render("Facile", True, WHITE)
    texte_moyen = font.render("Moyen", True, WHITE)
    texte_difficile = font.render("Difficile", True, WHITE)

    win.blit(texte_facile, (bouton_facile.x + 10, bouton_facile.y + 10))
    win.blit(texte_moyen, (bouton_moyen.x + 10, bouton_moyen.y + 10))
    win.blit(texte_difficile, (bouton_difficile.x + 10, bouton_difficile.y + 10))

    pygame.display.flip()
    
    return bouton_facile, bouton_moyen, bouton_difficile

def choisir_mot(niveau):
    global mot_choisi, lettres_trouvees, essais_restants, lettres_essayees
    if niveau == "facile":
        mot_choisi = random.choice(Mots_facile)
    elif niveau == "moyen":
        mot_choisi = random.choice(Mots_moyen)
    elif niveau == "difficile":
        mot_choisi = random.choice(Mots_difficile)

    lettres_trouvees = ["_"] * len(mot_choisi)
    essais_restants = 10  # Réinitialiser les essais
    lettres_essayees = []  # Réinitialiser les lettres essayées

# Affichage des essais restants (Potence + Pendu)
def dessiner_pendu(essais):
    # Potence
    if essais <= 9:
        pygame.draw.line(win, BLACK, (150, 400), (250, 400), 5)  # Base de la potence
    if essais <= 8:
        pygame.draw.line(win, BLACK, (200, 400), (200, 150), 5)  # Poteau vertical
    if essais <= 7:
        pygame.draw.line(win, BLACK, (200, 150), (300, 150), 5)  # Poteau horizontal
    if essais <= 6:
        pygame.draw.line(win, BLACK, (300, 150), (300, 200), 5)  # Corde

    # Corps du pendu
    if essais <= 5:
        pygame.draw.circle(win, BLACK, (300, 220), 20, 2)  # Tête
    if essais <= 4:
        pygame.draw.line(win, BLACK, (300, 240), (300, 300), 2)  # Corps
    if essais <= 3:
        pygame.draw.line(win, BLACK, (300, 260), (280, 280), 2)  # Bras gauche
    if essais <= 2:
        pygame.draw.line(win, BLACK, (300, 260), (320, 280), 2)  # Bras droit
    if essais <= 1:
        pygame.draw.line(win, BLACK, (300, 300), (280, 340), 2)  # Jambe gauche
    if essais == 0:
        pygame.draw.line(win, BLACK, (300, 300), (320, 340), 2)  # Jambe droite

# Affichage principal
def affichage_principal():
    win.fill(WHITE)

    # Affichage du mot
    mot_affiche = " ".join(lettres_trouvees)
    texte_mot = font.render(mot_affiche, True, BLACK)
    win.blit(texte_mot, (450, 200))

    # Affichage des essais restants
    texte_essais = font.render(f"Essais restants : {essais_restants}", True, RED)
    win.blit(texte_essais, (450, 50))

    # Affichage des lettres essayées
    texte_lettres = "Lettres essayées : " + ", ".join(lettres_essayees)
    texte_lettres_rendu = font.render(texte_lettres, True, BLACK)
    if texte_lettres_rendu.get_width() > WIDTH - 100:  # Ajuster pour plusieurs lignes
        lignes = [texte_lettres[i:i + 35] for i in range(0, len(texte_lettres), 35)]
        for i, ligne in enumerate(lignes):
            ligne_rendu = font.render(ligne, True, BLACK)
            win.blit(ligne_rendu, (450, 300 + i * 40))
    else:
        win.blit(texte_lettres_rendu, (450, 300))

    # Dessiner le pendu
    dessiner_pendu(essais_restants)

    pygame.display.flip()

# Fonction de gestion des événements
def gerer_entrées():
    global essais_restants
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and choix_difficulte:
            if event.key == pygame.K_ESCAPE:  # Touche Échap
                return False  # Indique que l'on veut quitter le menu
            lettre = event.unicode.lower()
            if len(lettre) == 1 and lettre.isalpha():
                if lettre not in lettres_essayees:
                    lettres_essayees.append(lettre)
                    if lettre in mot_choisi:
                        for i, char in enumerate(mot_choisi):
                            if char == lettre:
                                lettres_trouvees[i] = lettre
                    else:
                        essais_restants -= 1
    return True  # Indique que le jeu continue

# Fonction pour afficher un message de fin de jeu
def afficher_message_fin(gagné):
    win.fill(WHITE)
    if gagné:
        message = font.render("Vous avez gagné !", True, BLACK)
    else:
        message = font.render("Vous avez perdu !", True, BLACK)
    win.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 4))
    mot_complet = font.render(f"Le mot était : {mot_choisi}", True, BLACK)
    win.blit(mot_complet, (WIDTH // 2 - mot_complet.get_width() // 2, HEIGHT // 4 + 40))
    pygame.display.flip()
    pygame.time.delay(2000)  # Attendre 2 secondes avant de réinitialiser

def reset_game():
    global lettres_trouvees, essais_restants, lettres_essayees, mot_choisi, choix_difficulte
    lettres_trouvees = []
    essais_restants = 10
    lettres_essayees = []
    mot_choisi = ""
    choix_difficulte = False  # Réinitialiser le drapeau de difficulté

gagné = False
while True:
    if not choix_difficulte:
        bouton_facile, bouton_moyen, bouton_difficile = affichage_difficulte()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Touche Échap pour quitter le menu
                    pygame.quit()
                    exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_facile.collidepoint(event.pos):
                    choisir_mot("facile")
                    choix_difficulte = True
                elif bouton_moyen.collidepoint(event.pos):
                    choisir_mot("moyen")
                    choix_difficulte = True
                elif bouton_difficile.collidepoint(event.pos):
                    choisir_mot("difficile")
                    choix_difficulte = True
    else:
        if not gerer_entrées():  # Quitte si Échap est pressé
            choix_difficulte = False  # Retourne au menu
            continue
        
        affichage_principal()

        # Vérifier l'état du jeu
        if "_" not in lettres_trouvees:
            gagné = True
            afficher_message_fin(gagné)
            reset_game()  # Réinitialiser le jeu après la victoire
            continue  # Revenir au début de la boucle pour choisir la difficulté
        elif essais_restants <= 0:
            gagné = False
            afficher_message_fin(gagné)
            reset_game()  # Réinitialiser le jeu après la défaite
            continue  # Revenir au début de la boucle pour choisir la difficulté

    clock.tick(FPS)

pygame.quit()

from os import system
system('cls')

def afficher_grille(grille):
    for i, ligne in enumerate(grille):
        print(" | ".join(ligne))
        if i < 2:
            print("-" * 9)

# Grille vide (3x3)
grille = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]
]

afficher_grille(grille)
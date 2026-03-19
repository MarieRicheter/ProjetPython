from os import system
system('cls')

from morpion import afficher_grille


def jouer_humain_vs_humain():
    grille = [[" "] * 3 for _ in range(3)]
    joueurs = ["X", "O"]
    tour = 0

    while True:
        afficher_grille(grille)
        joueur = joueurs[tour % 2]
        print(f"\nTour du joueur {joueur}")

        try:
            ligne = int(input("Ligne (0-2) : "))
            col  = int(input("Colonne (0-2) : "))
        except ValueError:
            print("Entree invalide, réessaie.")
            continue

        if not (0 <= ligne <= 2 and 0 <= col <= 2):
            print("Position hors grille, reessaie.")
            continue

        if grille[ligne][col] != " ":
            print("Case deja occupee, reessaie.")
            continue

        grille[ligne][col] = joueur
        tour += 1

        gagnant = verifier_gagnant(grille)
        if gagnant:
            afficher_grille(grille)
            print(f"\nLe joueur {gagnant} a gagne !")
            return

        if tour == 9:
            afficher_grille(grille)
            print("\nMatch nul !")
            return


def jouer_humain_vs_ia():
    print("\nMode Humain vs IA — en cours de developpement...")

def verifier_gagnant(grille):
    # Lignes et colonnes
    for i in range(3):
        if grille[i][0] == grille[i][1] == grille[i][2] != " ":
            return grille[i][0]
        if grille[0][i] == grille[1][i] == grille[2][i] != " ":
            return grille[0][i]
    # Diagonales
    if grille[0][0] == grille[1][1] == grille[2][2] != " ":
        return grille[0][0]
    if grille[0][2] == grille[1][1] == grille[2][0] != " ":
        return grille[0][2]
    return None


def afficher_menu():
    print("\n╔══════════════════════════╗")
    print("║        MORPION           ║")
    print("╠══════════════════════════╣")
    print("║  1. Humain vs Humain     ║")
    print("║  2. Humain vs IA         ║")
    print("║  0. Quitter              ║")
    print("╚══════════════════════════╝")


def main():
    while True:
        afficher_menu()
        choix = input("\nVotre choix : ").strip()

        if choix == "1":
            jouer_humain_vs_humain()
        elif choix == "2":
            jouer_humain_vs_ia()
        elif choix == "0":
            print("A bientôt !")
            break
        else:
            print("Choix invalide, réessaie.")


if __name__ == "__main__":
    main()
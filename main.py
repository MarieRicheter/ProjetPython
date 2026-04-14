from morpion import Morpion
from minMax import coup_ia_minmax


def afficher_titre():
    """Affiche le titre du programme."""
    print("=" * 45)
    print("        BIENVENUE DANS LE MORPION")
    print("=" * 45)
    print("1. Joueur vs Joueur (classique)")
    print("2. Joueur vs Joueur (cases bloquées)")
    print("3. Joueur vs IA (MinMax)")
    print("4. Joueur vs IA (minMax avec cases bloquées)")
    print("5. Joueur vs IA (Qlearning) - à venir")
    print("=" * 45)


def choisir_mode():
    """Permet de choisir le mode de jeu."""
    afficher_titre()
    choix = input("Choisissez un mode : ")

    if choix == "1":
        return 0, False

    elif choix == "2":
        while True:
            try:
                nb = int(input("Combien de cases bloquées ? (1 à 3 conseillé) : "))
                if 0 <= nb <= 3:
                    return nb, False
                else:
                    print("Veuillez entrer un nombre entre 0 et 3.")
            except ValueError:
                print("Erreur : vous devez entrer un nombre valide.")

    elif choix == "3":
        return 0, True

    elif choix == "4":
        while True:
            try:
                nb = int(input("Combien de cases bloquées ? (1 à 3 conseillé) : "))
                if 0 <= nb <= 3:
                    return nb, True
                else:
                    print("Veuillez entrer un nombre entre 0 et 3.")
            except ValueError:
                print("Erreur : vous devez entrer un nombre valide.")

    else:
        print("Choix invalide. Le mode classique sera lancé.")
        return 0, False


def demander_coordonnees():
    """Demande la ligne et la colonne au joueur."""
    while True:
        try:
            ligne = int(input("Entrez la ligne : "))
            colonne = int(input("Entrez la colonne : "))
            return ligne, colonne
        except ValueError:
            print("Erreur : vous devez entrer des nombres entiers.")


def jouer_partie():
    """Lance une partie complète."""
    nb_cases_bloquees, ia_active = choisir_mode()
    jeu = Morpion(nb_cases_bloquees=nb_cases_bloquees)

    while True:
        jeu.afficher_grille()

        if ia_active and jeu.joueur_actuel == "O":
            print("Tour de l'IA (O)...")
            coup = coup_ia_minmax(jeu)
            if coup is not None:
                ligne, colonne = coup
                jeu.jouer_coup(ligne, colonne)
            else:
                print("Aucun coup possible pour l'IA.")
        else:
            ligne, colonne = demander_coordonnees()
            if not jeu.jouer_coup(ligne, colonne):
                print("Coup invalide : case occupée, bloquée ou hors de la grille.")
                continue

        if jeu.verifier_victoire(jeu.joueur_actuel):
            jeu.afficher_grille()
            print(f"\nVictoire du joueur {jeu.joueur_actuel} !")
            break

        if jeu.verifier_match_nul():
            jeu.afficher_grille()
            print("\nMatch nul !")
            break

        jeu.changer_joueur()


if __name__ == "__main__":
    jouer_partie()
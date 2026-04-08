from morpion import Morpion


def afficher_titre():
    """Affiche le titre du programme."""
    print("=" * 45)
    print("        BIENVENUE DANS LE MORPION")
    print("=" * 45)
    print("1. Mode classique")
    print("2. Mode avec cases bloquées")
    print("=" * 45)


def choisir_mode():
    """Permet de choisir le mode de jeu."""
    afficher_titre()
    choix = input("Choisissez un mode (1 ou 2) : ")

    if choix == "1":
        return 0

    elif choix == "2":
        while True:
            try:
                nb = int(input("Combien de cases bloquées ? (1 à 3 conseillé) : "))
                if 0 <= nb <= 3:
                    return nb
                else:
                    print("Veuillez entrer un nombre entre 0 et 3.")
            except ValueError:
                print("Erreur : vous devez entrer un nombre valide.")

    else:
        print("Choix invalide. Le mode classique sera lancé.")
        return 0


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
    nb_cases_bloquees = choisir_mode()
    jeu = Morpion(nb_cases_bloquees=nb_cases_bloquees)

    while True:
        jeu.afficher_grille()

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
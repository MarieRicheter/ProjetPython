from morpion import Morpion
from qlearning import QLearningAgent


def afficher_titre():
    print("=" * 50)
    print("              MORPION AVEC IA")
    print("=" * 50)
    print("1. Humain vs Humain")
    print("2. Humain vs IA (Q-learning)")
    print("=" * 50)


def choisir_mode():
    while True:
        afficher_titre()
        choix = input("Choisissez un mode (1 ou 2) : ")

        if choix in ["1", "2"]:
            return choix

        print("Choix invalide. Réessayez.\n")


def choisir_nb_cases_bloquees():
    while True:
        try:
            nb = int(input("Combien de cases bloquées ? (0 à 3 conseillé) : "))
            if 0 <= nb <= 3:
                return nb
            print("Veuillez entrer un nombre entre 0 et 3.")
        except ValueError:
            print("Erreur : vous devez entrer un nombre entier.")


def demander_coordonnees():
    while True:
        try:
            ligne = int(input("Entrez la ligne : "))
            colonne = int(input("Entrez la colonne : "))
            return ligne, colonne
        except ValueError:
            print("Erreur : vous devez entrer des nombres entiers.")


def jouer_humain_vs_humain():
    nb_cases_bloquees = choisir_nb_cases_bloquees()
    jeu = Morpion(nb_cases_bloquees=nb_cases_bloquees)

    while True:
        jeu.afficher_grille()
        print(f"\nTour du joueur {jeu.joueur_actuel}")

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


def jouer_humain_vs_ia():
    nb_cases_bloquees = choisir_nb_cases_bloquees()
    jeu = Morpion(nb_cases_bloquees=nb_cases_bloquees)

    agent = QLearningAgent(symbole="X")

    try:
        agent.charger("q_table.pkl")
    except FileNotFoundError:
        print("\nErreur : le fichier q_table.pkl est introuvable.")
        print("Vous devez d'abord lancer l'entraînement avec : python entrainement.py")
        return

    print("\nL'IA joue avec X et commence la partie.")
    print("Vous jouez avec O.\n")

    while True:
        jeu.afficher_grille()

        # Tour de l'IA
        if jeu.joueur_actuel == "X":
            print("\nTour de l'IA...")
            action = agent.choisir_action(jeu, entrainement=False)

            if action is None:
                print("Aucune action possible pour l'IA.")
                break

            jeu.jouer_symbole(action[0], action[1], "X")
            print(f"L'IA a joué : ligne {action[0]}, colonne {action[1]}")

            if jeu.verifier_victoire("X"):
                jeu.afficher_grille()
                print("\nL'IA a gagné !")
                break

            if jeu.verifier_match_nul():
                jeu.afficher_grille()
                print("\nMatch nul !")
                break

            jeu.changer_joueur()

        # Tour du joueur humain
        else:
            print("\nVotre tour (vous jouez avec O)")
            ligne, colonne = demander_coordonnees()

            if not jeu.jouer_coup(ligne, colonne):
                print("Coup invalide : case occupée, bloquée ou hors de la grille.")
                continue

            if jeu.verifier_victoire("O"):
                jeu.afficher_grille()
                print("\nBravo, vous avez gagné contre l'IA !")
                break

            if jeu.verifier_match_nul():
                jeu.afficher_grille()
                print("\nMatch nul !")
                break

            jeu.changer_joueur()


def main():
    mode = choisir_mode()

    if mode == "1":
        jouer_humain_vs_humain()
    else:
        jouer_humain_vs_ia()


if __name__ == "__main__":
    main()
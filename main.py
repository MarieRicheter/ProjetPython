from morpion import Morpion
from qlearning import QLearningAgent
from minMax import coup_ia_minmax
from evaluation import Evaluation


def choisir_taille_grille(nb_cases_bloquees):
    """Adapte la taille selon le blocage."""
    if nb_cases_bloquees <= 1:
        return 3
    elif nb_cases_bloquees <= 3:
        return 4
    else:
        return 5


def afficher_titre():
    print("=" * 60)
    print("         MORPION AVEC CASES BLOQUÉES ET IA")
    print("=" * 60)
    print("0. Quitter")
    print("1. Humain vs Humain")
    print("2. Humain vs Q-learning")
    print("3. Humain vs MinMax")
    print("4. Comparer Q-learning et MinMax")
    print("5. Entraîner le Q-learning (10000 episodes)")
    print("=" * 60)


def choisir_mode():
    """Choix du mode."""
    while True:
        afficher_titre()
        choix = input("Choisissez un mode (0 à 5) : ")

        if choix in ["0", "1", "2", "3", "4", "5"]:
            return choix

        print("Choix invalide.\n")


def choisir_nb_cases_bloquees():
    """Choix du nombre de cases bloquées."""
    while True:
        try:
            nb = int(input("Combien de cases bloquées ? : "))
            if nb >= 0:
                return nb
            print("Entrez un nombre positif.")
        except ValueError:
            print("Entrez un nombre entier.")


def demander_coordonnees():
    """Lecture simple des coordonnées."""
    while True:
        try:
            ligne = int(input("Entrez la ligne : "))
            colonne = int(input("Entrez la colonne : "))
            return ligne, colonne
        except ValueError:
            print("Entrez des nombres valides.")


def demander_blocage_manuel(jeu):
    """Permet de fixer les cases bloquées à la main."""
    if jeu.nb_cases_bloquees == 0:
        return

    choix = input("Voulez-vous placer les cases bloquées manuellement ? (o/n) : ").lower()

    if choix != "o":
        return

    positions = []
    print(f"Entrez {jeu.nb_cases_bloquees} positions.")

    while len(positions) < jeu.nb_cases_bloquees:
        try:
            ligne = int(input("Ligne bloquée : "))
            colonne = int(input("Colonne bloquée : "))
            pos = (ligne, colonne)

            if pos in positions:
                print("Case déjà choisie.")
                continue

            if not (0 <= ligne < jeu.taille and 0 <= colonne < jeu.taille):
                print("Case hors grille.")
                continue

            positions.append(pos)
        except ValueError:
            print("Coordonnées invalides.")

    if not jeu.definir_cases_bloquees_manuellement(positions):
        print("Configuration trop fermée. Retour au blocage automatique.")
        jeu.reinitialiser()


def creer_jeu():
    """Crée un jeu cohérent avec le nombre de cases bloquées."""
    nb_cases_bloquees = choisir_nb_cases_bloquees()
    taille = choisir_taille_grille(nb_cases_bloquees)

    print(f"\nTaille choisie automatiquement : {taille}x{taille}")
    jeu = Morpion(taille=taille, nb_cases_bloquees=nb_cases_bloquees)

    demander_blocage_manuel(jeu)
    return jeu


def jouer_humain_vs_humain():
    """Mode humain contre humain."""
    jeu = creer_jeu()

    while True:
        jeu.afficher_grille()
        print(f"\nTour du joueur {jeu.joueur_actuel}")

        ligne, colonne = demander_coordonnees()

        if not jeu.jouer_coup(ligne, colonne):
            print("Coup invalide.")
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


def jouer_humain_vs_qlearning():
    """Mode humain contre Q-learning."""
    jeu = creer_jeu()
    agent = QLearningAgent(symbole="X")

    try:
        agent.charger("q_table.pkl")
    except FileNotFoundError:
        print("\nLe fichier q_table.pkl est introuvable.")
        print("Lancez d'abord : python entrainement.py")
        return

    print("\nLe Q-learning joue avec X.")
    print("Vous jouez avec O.\n")

    while True:
        jeu.afficher_grille()

        if jeu.joueur_actuel == "X":
            print("\nTour du Q-learning...")
            action = agent.choisir_action(jeu, entrainement=False)

            if action is None:
                break

            jeu.jouer_symbole(action[0], action[1], "X")
            print(f"L'IA joue : ({action[0]}, {action[1]})")

            if jeu.verifier_victoire("X"):
                jeu.afficher_grille()
                print("\nLe Q-learning a gagné !")
                break

            if jeu.verifier_match_nul():
                jeu.afficher_grille()
                print("\nMatch nul !")
                break

            jeu.changer_joueur()

        else:
            print("\nVotre tour.")
            ligne, colonne = demander_coordonnees()

            if not jeu.jouer_coup(ligne, colonne):
                print("Coup invalide.")
                continue

            if jeu.verifier_victoire("O"):
                jeu.afficher_grille()
                print("\nBravo, vous avez gagné !")
                break

            if jeu.verifier_match_nul():
                jeu.afficher_grille()
                print("\nMatch nul !")
                break

            jeu.changer_joueur()


def jouer_humain_vs_minmax():
    """Mode humain contre MinMax."""
    jeu = creer_jeu()

    print("\nMinMax joue avec O.")
    print("Vous jouez avec X.\n")

    while True:
        jeu.afficher_grille()

        if jeu.joueur_actuel == "X":
            print("\nVotre tour.")
            ligne, colonne = demander_coordonnees()

            if not jeu.jouer_coup(ligne, colonne):
                print("Coup invalide.")
                continue

            if jeu.verifier_victoire("X"):
                jeu.afficher_grille()
                print("\nBravo, vous avez gagné !")
                break

            if jeu.verifier_match_nul():
                jeu.afficher_grille()
                print("\nMatch nul !")
                break

            jeu.changer_joueur()

        else:
            print("\nTour de MinMax...")
            action = coup_ia_minmax(jeu, symbole_ia="O", symbole_humain="X")

            if action is None:
                break

            jeu.jouer_symbole(action[0], action[1], "O")
            print(f"MinMax joue : ({action[0]}, {action[1]})")

            if jeu.verifier_victoire("O"):
                jeu.afficher_grille()
                print("\nMinMax a gagné !")
                break

            if jeu.verifier_match_nul():
                jeu.afficher_grille()
                print("\nMatch nul !")
                break

            jeu.changer_joueur()


def comparer_les_ia():
    """Compare les deux agents."""
    nb_cases_bloquees = choisir_nb_cases_bloquees()
    taille = choisir_taille_grille(nb_cases_bloquees)

    print(f"\nComparaison sur une grille {taille}x{taille}")

    agent = QLearningAgent(symbole="X")

    try:
        agent.charger("q_table.pkl")
    except FileNotFoundError:
        print("\nLe fichier q_table.pkl est introuvable.")
        print("Lancez d'abord : python entrainement.py")
        return

    evaluation = Evaluation(
        agent_qlearning=agent,
        num_parties=100,
        nb_cases_bloquees=nb_cases_bloquees
    )

    resultats = evaluation.evaluer_qlearning_vs_minmax()

    print("\n=== COMPARAISON DES IA ===")
    print(f"Q-learning : {resultats['qlearning']}")
    print(f"MinMax     : {resultats['minmax']}")
    print(f"Égalités   : {resultats['egalite']}")


def main():
    """Point d'entrée."""
    mode = choisir_mode()

    if mode == "0":
        print("Au revoir !")
        return
    elif mode == "1":
        jouer_humain_vs_humain()
    elif mode == "2":
        jouer_humain_vs_qlearning()
    elif mode == "3":
        jouer_humain_vs_minmax()
    elif mode == "4":
        comparer_les_ia()
    elif mode == "5":
        # Entrainement du Q-learning (10000 episodes)
        from entrainement import entrainer_agent
        nb_cases_bloquees = choisir_nb_cases_bloquees()
        print("\nEntrainement du Q-learning en cours...")
        agent, stats = entrainer_agent(nb_episodes=10000, nb_cases_bloquees=nb_cases_bloquees)
        print("\n=== ENTRAINEMENT TERMINÉ ===")
        print(f"Victoires : {stats['victoires']}")
        print(f"Défaites  : {stats['defaites']}")
        print(f"Nuls      : {stats['nuls']}")
        agent.sauvegarder("q_table.pkl")
        print("\nTable Q sauvegardée dans q_table.pkl")


if __name__ == "__main__":
    main()
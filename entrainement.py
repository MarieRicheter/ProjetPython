import random
from morpion import Morpion
from qlearning import QLearningAgent


def action_aleatoire(jeu):
    """Choisit un coup aléatoire parmi les coups possibles."""
    actions = jeu.coups_possibles()

    if not actions:
        return None

    return random.choice(actions)


def entrainer_agent(nb_episodes=10000, nb_cases_bloquees=1):
    """
    Entraîne l'agent Q-learning.
    X = agent Q-learning
    O = joueur aléatoire
    """
    agent = QLearningAgent(symbole="X")
    statistiques = {
        "victoires": 0,
        "defaites": 0,
        "nuls": 0
    }

    for episode in range(nb_episodes):
        jeu = Morpion(nb_cases_bloquees=nb_cases_bloquees)

        while not jeu.est_termine():
            # -----------------------------
            # Tour de l'agent Q-learning
            # -----------------------------
            etat = jeu.obtenir_etat()
            action = agent.choisir_action(jeu, entrainement=True)

            if action is None:
                break

            jeu.jouer_symbole(action[0], action[1], "X")

            # Si l'agent gagne
            if jeu.verifier_victoire("X"):
                agent.mettre_a_jour(
                    etat,
                    action,
                    1,
                    jeu.obtenir_etat(),
                    []
                )
                statistiques["victoires"] += 1
                break

            # Si match nul après le coup de X
            if jeu.verifier_match_nul():
                agent.mettre_a_jour(
                    etat,
                    action,
                    0.3,
                    jeu.obtenir_etat(),
                    []
                )
                statistiques["nuls"] += 1
                break

            # -----------------------------
            # Tour du joueur aléatoire O
            # -----------------------------
            action_ennemi = action_aleatoire(jeu)

            if action_ennemi is not None:
                jeu.jouer_symbole(action_ennemi[0], action_ennemi[1], "O")

            # Si l'ennemi gagne
            if jeu.verifier_victoire("O"):
                agent.mettre_a_jour(
                    etat,
                    action,
                    -1,
                    jeu.obtenir_etat(),
                    []
                )
                statistiques["defaites"] += 1
                break

            # Si match nul après le coup de O
            if jeu.verifier_match_nul():
                agent.mettre_a_jour(
                    etat,
                    action,
                    0.3,
                    jeu.obtenir_etat(),
                    []
                )
                statistiques["nuls"] += 1
                break

            # -----------------------------
            # Partie continue
            # -----------------------------
            etat_suivant = jeu.obtenir_etat()
            actions_suivantes = jeu.coups_possibles()

            agent.mettre_a_jour(
                etat,
                action,
                0,
                etat_suivant,
                actions_suivantes
            )

        agent.reduire_epsilon()

        if (episode + 1) % 1000 == 0:
            print(f"Épisode {episode + 1}/{nb_episodes} terminé.")

    return agent, statistiques


if __name__ == "__main__":
    agent, stats = entrainer_agent(nb_episodes=10000, nb_cases_bloquees=1)

    print("\n=== ENTRAÎNEMENT TERMINÉ ===")
    print(f"Victoires : {stats['victoires']}")
    print(f"Défaites  : {stats['defaites']}")
    print(f"Nuls      : {stats['nuls']}")

    agent.sauvegarder("q_table.pkl")
    print("\nTable Q sauvegardée dans q_table.pkl")
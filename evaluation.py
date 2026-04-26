from morpion import Morpion
from minMax import coup_ia_minmax
from qlearning import QLearningAgent


def choisir_taille_grille(nb_cases_bloquees):
    """Même logique que dans main."""
    if nb_cases_bloquees <= 1:
        return 3
    elif nb_cases_bloquees <= 3:
        return 4
    else:
        return 5


class Evaluation:
    def __init__(self, agent_qlearning, num_parties=100, nb_cases_bloquees=0):
        self.agent_qlearning = agent_qlearning
        self.num_parties = num_parties
        self.nb_cases_bloquees = nb_cases_bloquees

    def evaluer_qlearning_vs_minmax(self):
        """Compare les deux IA."""
        resultats = {
            "qlearning": 0,
            "minmax": 0,
            "egalite": 0
        }

        taille = choisir_taille_grille(self.nb_cases_bloquees)

        for _ in range(self.num_parties):
            jeu = Morpion(taille=taille, nb_cases_bloquees=self.nb_cases_bloquees)

            while not jeu.est_termine():
                if jeu.joueur_actuel == "X":
                    action = self.agent_qlearning.choisir_action(jeu, entrainement=False)
                    if action is not None:
                        jeu.jouer_symbole(action[0], action[1], "X")
                else:
                    action = coup_ia_minmax(jeu, symbole_ia="O", symbole_humain="X")
                    if action is not None:
                        jeu.jouer_symbole(action[0], action[1], "O")

                if not jeu.est_termine():
                    jeu.changer_joueur()

            gagnant = jeu.obtenir_gagnant()

            if gagnant == "X":
                resultats["qlearning"] += 1
            elif gagnant == "O":
                resultats["minmax"] += 1
            else:
                resultats["egalite"] += 1

        return resultats


if __name__ == "__main__":
    agent = QLearningAgent(symbole="X")
    agent.charger("q_table.pkl")

    evaluation = Evaluation(agent_qlearning=agent, num_parties=100, nb_cases_bloquees=2)
    resultats = evaluation.evaluer_qlearning_vs_minmax()

    print("\n=== RÉSULTATS DE LA COMPARAISON ===")
    print(f"Q-learning : {resultats['qlearning']}")
    print(f"MinMax     : {resultats['minmax']}")
    print(f"Égalités   : {resultats['egalite']}")
from morpion import Morpion
from minMax import coup_ia_minmax
from entrainement import entrainer_agent
from qlearning import QLearningAgent

class evaluation:
    def __init__(self, agent1, agent2, num_parties):
        self.agent1 = agent1
        self.agent2 = agent2
        self.num_parties = num_parties

    def evaluer(self):
        resultats = {"qlearning": 0, "minMax": 0, "egalite": 0}
        for _ in range(self.num_parties):
            jeu = Morpion()
            while not jeu.est_termine():
                if jeu.joueur_actuel == 1:
                    ligne, colonne = self.agent1.choisir_coup(jeu)
                else:
                    ligne, colonne = self.agent2.choisir_coup(jeu)
                jeu.jouer_coup(ligne, colonne)
            if jeu.gagnant == 1:
                resultats["qlearning"] += 1
            elif jeu.gagnant == 2:
                resultats["minMax"] += 1
            else:
                resultats["egalite"] += 1
        return resultats
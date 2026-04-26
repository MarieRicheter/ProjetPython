import random
import pickle


class QLearningAgent:
    def __init__(self, symbole="X", alpha=0.1, gamma=0.9, epsilon=0.2):
        self.symbole = symbole
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}

    def get_q_value(self, etat, action):
        """Valeur Q d'un état-action."""
        return self.q_table.get((etat, action), 0.0)

    def choisir_action(self, jeu, entrainement=True):
        """Choisit un coup."""
        actions = jeu.coups_possibles()

        if not actions:
            return None

        # Un peu de hasard pendant l'apprentissage
        if entrainement and random.random() < self.epsilon:
            return random.choice(actions)

        etat = jeu.obtenir_etat()
        meilleure_valeur = float("-inf")
        meilleures_actions = []

        for action in actions:
            valeur = self.get_q_value(etat, action)

            if valeur > meilleure_valeur:
                meilleure_valeur = valeur
                meilleures_actions = [action]
            elif valeur == meilleure_valeur:
                meilleures_actions.append(action)

        return random.choice(meilleures_actions)

    def mettre_a_jour(self, etat, action, recompense, etat_suivant, actions_suivantes):
        """Formule du Q-learning."""
        ancienne_valeur = self.get_q_value(etat, action)

        if actions_suivantes:
            future_max = max(self.get_q_value(etat_suivant, a) for a in actions_suivantes)
        else:
            future_max = 0.0

        nouvelle_valeur = ancienne_valeur + self.alpha * (
            recompense + self.gamma * future_max - ancienne_valeur
        )

        self.q_table[(etat, action)] = nouvelle_valeur

    def reduire_epsilon(self, facteur=0.995, minimum=0.05):
        """Moins de hasard avec le temps."""
        self.epsilon = max(minimum, self.epsilon * facteur)

    def sauvegarder(self, nom_fichier="q_table.pkl"):
        """Sauvegarde la mémoire de l'agent."""
        with open(nom_fichier, "wb") as f:
            pickle.dump(self.q_table, f)

    def charger(self, nom_fichier="q_table.pkl"):
        """Recharge la mémoire."""
        with open(nom_fichier, "rb") as f:
            self.q_table = pickle.load(f)
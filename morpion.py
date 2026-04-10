import random


class Morpion:
    def __init__(self, taille=3, nb_cases_bloquees=0):
        self.taille = taille
        self.nb_cases_bloquees = nb_cases_bloquees
        self.grille = [[" " for _ in range(taille)] for _ in range(taille)]
        self.cases_bloquees = set()
        self.joueur_actuel = "X"

        if nb_cases_bloquees > 0:
            self.generer_cases_bloquees()

    def generer_cases_bloquees(self):
        """Choisit aléatoirement les cases bloquées."""
        toutes_les_cases = [(i, j) for i in range(self.taille) for j in range(self.taille)]
        cases_choisies = random.sample(toutes_les_cases, self.nb_cases_bloquees)

        for case in cases_choisies:
            self.cases_bloquees.add(case)
            i, j = case
            self.grille[i][j] = "#"

    def afficher_grille(self):
        """Affiche une grille propre dans le terminal."""
        print("\n" + "=" * 35)
        print("           MORPION")
        print("=" * 35)
        print(f"Joueur actuel : {self.joueur_actuel}")
        print("Légende : X = joueur 1 | O = joueur 2 | # = bloquée | . = vide")
        print("-" * 35)

        print("    " + "   ".join(str(i) for i in range(self.taille)))
        print("   +" + "---+" * self.taille)

        for i in range(self.taille):
            ligne_affichee = []
            for j in range(self.taille):
                case = self.grille[i][j]
                if case == " ":
                    ligne_affichee.append(".")
                else:
                    ligne_affichee.append(case)

            print(f" {i} | " + " | ".join(ligne_affichee) + " |")
            print("   +" + "---+" * self.taille)

    def coup_valide(self, ligne, colonne):
        """Vérifie si un coup est autorisé."""
        if ligne < 0 or ligne >= self.taille or colonne < 0 or colonne >= self.taille:
            return False

        if (ligne, colonne) in self.cases_bloquees:
            return False

        if self.grille[ligne][colonne] != " ":
            return False

        return True

    def jouer_coup(self, ligne, colonne):
        """Place le symbole du joueur actuel si le coup est valide."""
        if self.coup_valide(ligne, colonne):
            self.grille[ligne][colonne] = self.joueur_actuel
            return True
        return False

    def jouer_symbole(self, ligne, colonne, symbole):
        """Permet à l'IA de jouer directement avec X ou O."""
        if self.coup_valide(ligne, colonne):
            self.grille[ligne][colonne] = symbole
            return True
        return False

    def changer_joueur(self):
        """Passe de X à O ou de O à X."""
        if self.joueur_actuel == "X":
            self.joueur_actuel = "O"
        else:
            self.joueur_actuel = "X"

    def coups_possibles(self):
        """Retourne toutes les cases encore jouables."""
        coups = []
        for i in range(self.taille):
            for j in range(self.taille):
                if self.grille[i][j] == " ":
                    coups.append((i, j))
        return coups

    def obtenir_etat(self):
        """Transforme la grille en chaîne exploitable par l'IA."""
        etat = []
        for ligne in self.grille:
            for case in ligne:
                if case == " ":
                    etat.append("_")
                else:
                    etat.append(case)
        return "".join(etat)

    def verifier_victoire(self, symbole):
        """Vérifie si le symbole a gagné."""
        for ligne in self.grille:
            if all(case == symbole for case in ligne):
                return True

        for col in range(self.taille):
            if all(self.grille[ligne][col] == symbole for ligne in range(self.taille)):
                return True

        if all(self.grille[i][i] == symbole for i in range(self.taille)):
            return True

        if all(self.grille[i][self.taille - 1 - i] == symbole for i in range(self.taille)):
            return True

        return False

    def verifier_match_nul(self):
        """Vérifie s'il n'y a plus de cases libres."""
        for i in range(self.taille):
            for j in range(self.taille):
                if self.grille[i][j] == " ":
                    return False
        return True

    def obtenir_gagnant(self):
        """Retourne X, O ou None."""
        if self.verifier_victoire("X"):
            return "X"
        if self.verifier_victoire("O"):
            return "O"
        return None

    def est_termine(self):
        """Retourne True si la partie est finie."""
        return self.obtenir_gagnant() is not None or self.verifier_match_nul()
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

    def lignes_gagnantes(self):
        """Toutes les lignes de victoire."""
        lignes = []

        # Lignes
        for i in range(self.taille):
            lignes.append([(i, j) for j in range(self.taille)])

        # Colonnes
        for j in range(self.taille):
            lignes.append([(i, j) for i in range(self.taille)])

        # Diagonale principale
        lignes.append([(i, i) for i in range(self.taille)])

        # Diagonale secondaire
        lignes.append([(i, self.taille - 1 - i) for i in range(self.taille)])

        return lignes

    def compter_lignes_ouvertes(self):
        """Compte les lignes encore jouables."""
        compteur = 0
        for ligne in self.lignes_gagnantes():
            if all((i, j) not in self.cases_bloquees for i, j in ligne):
                compteur += 1
        return compteur

    def configuration_bloquage_valide(self, minimum_lignes_ouvertes=2):
        """Évite les plateaux trop fermés."""
        return self.compter_lignes_ouvertes() >= minimum_lignes_ouvertes

    def generer_cases_bloquees(self):
        """Place les cases bloquées de façon plus intelligente."""
        toutes_les_cases = [(i, j) for i in range(self.taille) for j in range(self.taille)]
        essais_max = 100

        for _ in range(essais_max):
            self.cases_bloquees = set(random.sample(toutes_les_cases, self.nb_cases_bloquees))
            self.grille = [[" " for _ in range(self.taille)] for _ in range(self.taille)]

            for i, j in self.cases_bloquees:
                self.grille[i][j] = "#"

            minimum = 2 if self.taille == 3 else 3
            if self.configuration_bloquage_valide(minimum_lignes_ouvertes=minimum):
                return

    def definir_cases_bloquees_manuellement(self, positions):
        """Permet de tester un scénario précis."""
        self.cases_bloquees = set()
        self.grille = [[" " for _ in range(self.taille)] for _ in range(self.taille)]

        for i, j in positions:
            if 0 <= i < self.taille and 0 <= j < self.taille:
                self.cases_bloquees.add((i, j))
                self.grille[i][j] = "#"

        minimum = 2 if self.taille == 3 else 3
        return self.configuration_bloquage_valide(minimum_lignes_ouvertes=minimum)

    def reinitialiser(self):
        """Remet la partie à zéro."""
        self.grille = [[" " for _ in range(self.taille)] for _ in range(self.taille)]
        self.cases_bloquees = set()
        self.joueur_actuel = "X"

        if self.nb_cases_bloquees > 0:
            self.generer_cases_bloquees()

    def afficher_grille(self):
        """Affichage propre."""
        print("\n" + "=" * 45)
        print(f"       MORPION {self.taille}x{self.taille}")
        print("=" * 45)
        print(f"Joueur actuel : {self.joueur_actuel}")
        print("Légende : X = joueur 1 | O = joueur 2 | # = bloquée | . = vide")
        print("-" * 45)

        print("    " + "   ".join(str(i) for i in range(self.taille)))
        print("   +" + "---+" * self.taille)

        for i in range(self.taille):
            ligne_affichee = []
            for j in range(self.taille):
                case = self.grille[i][j]
                ligne_affichee.append("." if case == " " else case)

            print(f" {i} | " + " | ".join(ligne_affichee) + " |")
            print("   +" + "---+" * self.taille)

    def coup_valide(self, ligne, colonne):
        """Vérifie si la case est jouable."""
        if ligne < 0 or ligne >= self.taille or colonne < 0 or colonne >= self.taille:
            return False

        if (ligne, colonne) in self.cases_bloquees:
            return False

        if self.grille[ligne][colonne] != " ":
            return False

        return True

    def jouer_coup(self, ligne, colonne):
        """Joue avec le joueur actuel."""
        if self.coup_valide(ligne, colonne):
            self.grille[ligne][colonne] = self.joueur_actuel
            return True
        return False

    def jouer_symbole(self, ligne, colonne, symbole):
        """Utile pour les IA."""
        if self.coup_valide(ligne, colonne):
            self.grille[ligne][colonne] = symbole
            return True
        return False

    def changer_joueur(self):
        """Change de joueur."""
        self.joueur_actuel = "O" if self.joueur_actuel == "X" else "X"

    def coups_possibles(self):
        """Liste des cases libres."""
        coups = []
        for i in range(self.taille):
            for j in range(self.taille):
                if self.grille[i][j] == " ":
                    coups.append((i, j))
        return coups

    def obtenir_etat(self):
        """État lisible par l'IA."""
        etat = []
        for ligne in self.grille:
            for case in ligne:
                etat.append("_" if case == " " else case)
        return "".join(etat)

    def verifier_victoire(self, symbole):
        """Teste si un joueur remplit une ligne complète."""
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
        """S'il n'y a plus de case libre."""
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
        """Fin de partie."""
        return self.obtenir_gagnant() is not None or self.verifier_match_nul()
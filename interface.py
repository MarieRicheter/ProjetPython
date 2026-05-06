import tkinter as tk
from tkinter import messagebox, simpledialog
import threading

from morpion import Morpion
from qlearning import QLearningAgent
from minMax import coup_ia_minmax
from entrainement import entrainer_agent
from evaluation import Evaluation


class InterfaceMorpion:
    def __init__(self, root):
        self.root = root
        self.root.title("Projet IA - Morpion à cases bloquées")
        self.root.geometry("1000x700")
        self.root.configure(bg="#0f172a")

        self.jeu = None
        self.mode = None
        self.agent_q = None

        self.creer_interface_accueil()

    def nettoyer_fenetre(self):
        """Efface tous les widgets de la fenêtre."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def creer_titre(self, texte):
        """Affiche un titre principal."""
        label = tk.Label(
            self.root,
            text=texte,
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#0f172a"
        )
        label.pack(pady=20)

    def creer_bouton(self, texte, commande, couleur="#1d4ed8"):
        """Crée un bouton uniforme."""
        bouton = tk.Button(
            self.root,
            text=texte,
            command=commande,
            font=("Arial", 13, "bold"),
            bg=couleur,
            fg="white",
            width=30,
            height=2,
            relief="flat",
            cursor="hand2"
        )
        bouton.pack(pady=8)
        return bouton

    def creer_interface_accueil(self):
        """Page d'accueil principale."""
        self.nettoyer_fenetre()
        self.creer_titre("MORPION AVEC CASES BLOQUÉES ET IA")

        sous_titre = tk.Label(
            self.root,
            text="MinMax - Q-learning - Entraînement - Comparaison",
            font=("Arial", 12),
            fg="#cbd5e1",
            bg="#0f172a"
        )
        sous_titre.pack(pady=5)

        self.creer_bouton("Humain vs Humain", self.lancer_humain_vs_humain)
        self.creer_bouton("Humain vs Q-learning", self.lancer_humain_vs_qlearning)
        self.creer_bouton("Humain vs MinMax", self.lancer_humain_vs_minmax)
        self.creer_bouton("Comparer Q-learning et MinMax", self.comparer_ia, "#7c3aed")
        self.creer_bouton("Entraîner le Q-learning", self.lancer_entrainement, "#059669")

        quitter = tk.Button(
            self.root,
            text="Quitter",
            command=self.root.quit,
            font=("Arial", 12, "bold"),
            bg="#dc2626",
            fg="white",
            width=20,
            height=2,
            relief="flat",
            cursor="hand2"
        )
        quitter.pack(pady=20)

    def demander_parametres(self):
        """Demande les paramètres du jeu."""
        nb_cases = simpledialog.askinteger(
            "Cases bloquées",
            "Combien de cases bloquées ?",
            minvalue=0,
            maxvalue=6
        )

        if nb_cases is None:
            return None, None

        if nb_cases <= 1:
            taille = 3
        elif nb_cases <= 3:
            taille = 4
        else:
            taille = 5

        return taille, nb_cases

    def dessiner_grille(self):
        """Affiche la grille sous forme de boutons."""
        self.nettoyer_fenetre()
        self.creer_titre(f"Mode : {self.mode}")

        info = tk.Label(
            self.root,
            text=f"Joueur actuel : {self.jeu.joueur_actuel}",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#0f172a"
        )
        info.pack(pady=10)

        self.info_label = info

        cadre = tk.Frame(self.root, bg="#0f172a")
        cadre.pack(pady=20)

        self.boutons_grille = []

        for i in range(self.jeu.taille):
            ligne_boutons = []
            for j in range(self.jeu.taille):
                valeur = self.jeu.grille[i][j]

                texte = valeur if valeur != " " else ""
                couleur = "#1e293b"

                if valeur == "#":
                    couleur = "#475569"
                    texte = "#"
                elif valeur == "X":
                    couleur = "#2563eb"
                elif valeur == "O":
                    couleur = "#ea580c"

                btn = tk.Button(
                    cadre,
                    text=texte,
                    font=("Arial", 20, "bold"),
                    width=4,
                    height=2,
                    bg=couleur,
                    fg="white",
                    command=lambda x=i, y=j: self.jouer_case(x, y)
                )
                btn.grid(row=i, column=j, padx=5, pady=5)
                ligne_boutons.append(btn)

            self.boutons_grille.append(ligne_boutons)

        bas = tk.Frame(self.root, bg="#0f172a")
        bas.pack(pady=20)

        tk.Button(
            bas,
            text="Retour accueil",
            command=self.creer_interface_accueil,
            font=("Arial", 12, "bold"),
            bg="#dc2626",
            fg="white",
            width=18
        ).grid(row=0, column=0, padx=10)

    def maj_grille(self):
        """Met à jour les boutons de la grille."""
        for i in range(self.jeu.taille):
            for j in range(self.jeu.taille):
                valeur = self.jeu.grille[i][j]
                btn = self.boutons_grille[i][j]

                if valeur == " ":
                    btn.config(text="", bg="#1e293b")
                elif valeur == "#":
                    btn.config(text="#", bg="#475569")
                elif valeur == "X":
                    btn.config(text="X", bg="#2563eb")
                elif valeur == "O":
                    btn.config(text="O", bg="#ea580c")

        self.info_label.config(text=f"Joueur actuel : {self.jeu.joueur_actuel}")

    def verifier_fin(self):
        """Teste si la partie est finie."""
        gagnant = self.jeu.obtenir_gagnant()

        if gagnant is not None:
            messagebox.showinfo("Fin", f"Le joueur {gagnant} a gagné !")
            self.creer_interface_accueil()
            return True

        if self.jeu.verifier_match_nul():
            messagebox.showinfo("Fin", "Match nul !")
            self.creer_interface_accueil()
            return True

        return False

    def jouer_case(self, i, j):
        """Gère le clic sur une case."""
        if self.mode == "Humain vs Humain":
            if self.jeu.jouer_coup(i, j):
                self.maj_grille()
                if self.verifier_fin():
                    return
                self.jeu.changer_joueur()
                self.maj_grille()

        elif self.mode == "Humain vs Q-learning":
            if self.jeu.joueur_actuel == "O":
                if self.jeu.jouer_coup(i, j):
                    self.maj_grille()
                    if self.verifier_fin():
                        return
                    self.jeu.changer_joueur()
                    self.maj_grille()
                    self.root.after(400, self.tour_qlearning)

        elif self.mode == "Humain vs MinMax":
            if self.jeu.joueur_actuel == "X":
                if self.jeu.jouer_coup(i, j):
                    self.maj_grille()
                    if self.verifier_fin():
                        return
                    self.jeu.changer_joueur()
                    self.maj_grille()
                    self.root.after(400, self.tour_minmax)

    def tour_qlearning(self):
        """Fait jouer le Q-learning."""
        action = self.agent_q.choisir_action(self.jeu, entrainement=False)

        if action is not None:
            self.jeu.jouer_symbole(action[0], action[1], "X")
            self.maj_grille()

            if self.verifier_fin():
                return

            self.jeu.changer_joueur()
            self.maj_grille()

    def tour_minmax(self):
        """Fait jouer MinMax."""
        action = coup_ia_minmax(self.jeu, symbole_ia="O", symbole_humain="X")

        if action is not None:
            self.jeu.jouer_symbole(action[0], action[1], "O")
            self.maj_grille()

            if self.verifier_fin():
                return

            self.jeu.changer_joueur()
            self.maj_grille()

    def lancer_humain_vs_humain(self):
        """Lance le mode humain vs humain."""
        taille, nb_cases = self.demander_parametres()
        if taille is None:
            return

        self.jeu = Morpion(taille=taille, nb_cases_bloquees=nb_cases)
        self.mode = "Humain vs Humain"
        self.dessiner_grille()

    def lancer_humain_vs_qlearning(self):
        """Lance le mode humain vs Q-learning."""
        taille, nb_cases = self.demander_parametres()
        if taille is None:
            return

        self.jeu = Morpion(taille=taille, nb_cases_bloquees=nb_cases)
        self.mode = "Humain vs Q-learning"
        self.agent_q = QLearningAgent(symbole="X")

        try:
            self.agent_q.charger("q_table.pkl")
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Le fichier q_table.pkl est introuvable.\nLancez d'abord l'entraînement.")
            return

        self.dessiner_grille()

        if self.jeu.joueur_actuel == "X":
            self.root.after(400, self.tour_qlearning)

    def lancer_humain_vs_minmax(self):
        """Lance le mode humain vs MinMax."""
        taille, nb_cases = self.demander_parametres()
        if taille is None:
            return

        self.jeu = Morpion(taille=taille, nb_cases_bloquees=nb_cases)
        self.mode = "Humain vs MinMax"
        self.dessiner_grille()

    def lancer_entrainement(self):
        """Lance l'entraînement depuis l'accueil."""
        nb_episodes = simpledialog.askinteger(
            "Entraînement",
            "Nombre d'épisodes ?",
            minvalue=100,
            maxvalue=50000
        )

        if nb_episodes is None:
            return

        nb_cases = simpledialog.askinteger(
            "Cases bloquées",
            "Nombre de cases bloquées pour l'entraînement ?",
            minvalue=0,
            maxvalue=3
        )

        if nb_cases is None:
            return

        self.nettoyer_fenetre()
        self.creer_titre("ENTRAÎNEMENT EN COURS")

        self.zone_resultat = tk.Text(
            self.root,
            width=80,
            height=20,
            font=("Consolas", 11),
            bg="#111827",
            fg="white"
        )
        self.zone_resultat.pack(pady=20)

        tk.Button(
            self.root,
            text="Retour accueil",
            command=self.creer_interface_accueil,
            font=("Arial", 12, "bold"),
            bg="#dc2626",
            fg="white",
            width=18
        ).pack(pady=10)

        def entrainer():
            agent, stats = entrainer_agent(nb_episodes=nb_episodes, nb_cases_bloquees=nb_cases)
            agent.sauvegarder("q_table.pkl")

            texte = (
                f"Entraînement terminé\n\n"
                f"Épisodes : {nb_episodes}\n"
                f"Cases bloquées : {nb_cases}\n\n"
                f"Victoires : {stats['victoires']}\n"
                f"Défaites  : {stats['defaites']}\n"
                f"Nuls      : {stats['nuls']}\n\n"
                f"Table Q sauvegardée dans q_table.pkl"
            )

            self.zone_resultat.insert("1.0", texte)

        threading.Thread(target=entrainer).start()

    def comparer_ia(self):
        """Compare les deux IA depuis l'accueil."""
        nb_cases = simpledialog.askinteger(
            "Comparaison",
            "Combien de cases bloquées ?",
            minvalue=0,
            maxvalue=3
        )

        if nb_cases is None:
            return

        self.nettoyer_fenetre()
        self.creer_titre("COMPARAISON DES IA")

        zone = tk.Text(
            self.root,
            width=70,
            height=15,
            font=("Consolas", 12),
            bg="#111827",
            fg="white"
        )
        zone.pack(pady=20)

        tk.Button(
            self.root,
            text="Retour accueil",
            command=self.creer_interface_accueil,
            font=("Arial", 12, "bold"),
            bg="#dc2626",
            fg="white",
            width=18
        ).pack(pady=10)

        agent = QLearningAgent(symbole="X")

        try:
            agent.charger("q_table.pkl")
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Le fichier q_table.pkl est introuvable.\nLancez d'abord l'entraînement.")
            self.creer_interface_accueil()
            return

        evaluation = Evaluation(agent_qlearning=agent, num_parties=100, nb_cases_bloquees=nb_cases)
        resultats = evaluation.evaluer_qlearning_vs_minmax()

        texte = (
            "=== RÉSULTATS DE LA COMPARAISON ===\n\n"
            f"Q-learning : {resultats['qlearning']}\n"
            f"MinMax     : {resultats['minmax']}\n"
            f"Égalités   : {resultats['egalite']}\n"
        )
        zone.insert("1.0", texte)


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceMorpion(root)
    root.mainloop()
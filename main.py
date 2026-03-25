from os import system
system('cls')
import tkinter as tk
from tkinter import messagebox

from morpion import afficher_grille

def verifier_gagnant(grille):
    for i in range(3):
        if grille[i][0] == grille[i][1] == grille[i][2] != " ":
            return grille[i][0], [(i, 0), (i, 1), (i, 2)]
        if grille[0][i] == grille[1][i] == grille[2][i] != " ":
            return grille[0][i], [(0, i), (1, i), (2, i)]
    if grille[0][0] == grille[1][1] == grille[2][2] != " ":
        return grille[0][0], [(0, 0), (1, 1), (2, 2)]
    if grille[0][2] == grille[1][1] == grille[2][0] != " ":
        return grille[0][2], [(0, 2), (1, 1), (2, 0)]
    return None, []

BG         = "#1e1e2e"
CELL_BG    = "#2a2a3e"
CELL_HOVER = "#33334d"
WIN_COL    = "#a6e3a1"
X_COL      = "#f38ba8"
O_COL      = "#89dceb"
TEXT_COL   = "#cdd6f4"
MUTED_COL  = "#6c7086"
BTN_BG     = "#313244"
BTN_ACT    = "#45475a"

FONT_TITLE  = ("Segoe UI", 26, "bold")
FONT_STATUS = ("Segoe UI", 13)
FONT_CELL   = ("Segoe UI", 42, "bold")
FONT_BTN    = ("Segoe UI", 11)
FONT_MENU   = ("Segoe UI", 14)

CELL_SIZE = 130
GAP       = 8

class MenuWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Morpion")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self._center(360, 320)
        self._build()

    def _center(self, w, h):
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _build(self):
        tk.Label(self.root, text="MORPION", font=FONT_TITLE,
                 bg=BG, fg=TEXT_COL).pack(pady=(36, 6))
        tk.Label(self.root, text="Choisissez un mode de jeu",
                 font=FONT_STATUS, bg=BG, fg=MUTED_COL).pack(pady=(0, 28))

        self._btn("Humain  vs  Humain", lambda: self._launch("hvh"))
        self._btn("Humain  vs  IA", lambda: self._launch("hvia"))

        tk.Label(self.root, text="", bg=BG).pack(expand=True)
        tk.Label(self.root, text="Morpion 2025", font=("Segoe UI", 9),
                 bg=BG, fg=MUTED_COL).pack(pady=10)

    def _btn(self, label, cmd):
        b = tk.Button(self.root, text=label, font=FONT_MENU,
                      bg=BTN_BG, fg=TEXT_COL, activebackground=BTN_ACT,
                      activeforeground=TEXT_COL, relief="flat", cursor="hand2",
                      padx=20, pady=12, command=cmd)
        b.pack(fill="x", padx=48, pady=6)

    def _launch(self, mode):
        if mode == "hvia":
            messagebox.showinfo("En cours", "Mode Humain vs IA - en cours de développement !")
            return
        self.root.withdraw()
        game_win = tk.Toplevel(self.root)
        game_win.protocol("WM_DELETE_WINDOW", lambda: self.root.destroy())
        GameWindow(game_win, mode, on_back=self._on_back)

    def _on_back(self, game_win):
        game_win.destroy()
        self.root.deiconify()

class GameWindow:
    def __init__(self, root, mode, on_back):
        self.root    = root
        self.mode    = mode
        self.on_back = on_back
        self.grille  = [[" "] * 3 for _ in range(3)]
        self.joueurs = ["X", "O"]
        self.tour    = 0
        self.fini    = False

        self.root.title("Morpion — Humain vs Humain")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self._center()
        self._build()

    def _center(self):
        w = CELL_SIZE * 3 + GAP * 4 + 40
        h = w + 130
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _build(self):
        # En-tete
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=20, pady=(18, 4))

        tk.Button(header, text="← Menu", font=FONT_BTN,
                  bg=BTN_BG, fg=TEXT_COL, activebackground=BTN_ACT,
                  activeforeground=TEXT_COL, relief="flat", cursor="hand2",
                  padx=10, pady=5,
                  command=lambda: self.on_back(self.root)).pack(side="left")

        tk.Label(header, text="Morpion", font=("Segoe UI", 15, "bold"),
                 bg=BG, fg=TEXT_COL).pack(side="left", expand=True)

        # Statut
        self.status_var = tk.StringVar()
        self._set_status()
        tk.Label(self.root, textvariable=self.status_var,
                 font=FONT_STATUS, bg=BG, fg=TEXT_COL).pack(pady=(6, 12))

        # Grille (Canvas)
        canvas_size = CELL_SIZE * 3 + GAP * 4
        self.canvas = tk.Canvas(self.root, width=canvas_size, height=canvas_size,
                                bg=BG, highlightthickness=0)
        self.canvas.pack(padx=20)
        self._draw_grid()

        # Bouton rejouer
        tk.Button(self.root, text="Rejouer", font=FONT_BTN,
                  bg=BTN_BG, fg=TEXT_COL, activebackground=BTN_ACT,
                  activeforeground=TEXT_COL, relief="flat", cursor="hand2",
                  padx=16, pady=8, command=self._reset).pack(pady=14)

    def _draw_grid(self):
        self.canvas.delete("all")
        self.rects = {}
        self.texts = {}

        for r in range(3):
            for c in range(3):
                x1 = GAP + c * (CELL_SIZE + GAP)
                y1 = GAP + r * (CELL_SIZE + GAP)
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                rect = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=CELL_BG, outline="", tags=f"cell_{r}_{c}"
                )
                text = self.canvas.create_text(
                    (x1+x2)//2, (y1+y2)//2,
                    text="", font=FONT_CELL, fill=TEXT_COL,
                    tags=f"txt_{r}_{c}"
                )
                self.rects[(r, c)] = rect
                self.texts[(r, c)] = text

                for tag in (f"cell_{r}_{c}", f"txt_{r}_{c}"):
                    self.canvas.tag_bind(tag, "<Enter>",
                                         lambda e, rr=r, cc=c: self._hover(rr, cc, True))
                    self.canvas.tag_bind(tag, "<Leave>",
                                         lambda e, rr=r, cc=c: self._hover(rr, cc, False))
                    self.canvas.tag_bind(tag, "<Button-1>",
                                         lambda e, rr=r, cc=c: self._clic(rr, cc))

    def _hover(self, r, c, enter):
        if self.fini or self.grille[r][c] != " ":
            return
        self.canvas.itemconfig(self.rects[(r, c)],
                               fill=CELL_HOVER if enter else CELL_BG)

    def _clic(self, r, c):
        if self.fini or self.grille[r][c] != " ":
            return
        joueur = self.joueurs[self.tour % 2]
        self.grille[r][c] = joueur
        color = X_COL if joueur == "X" else O_COL
        self.canvas.itemconfig(self.texts[(r, c)], text=joueur, fill=color)
        self.canvas.itemconfig(self.rects[(r, c)], fill=CELL_BG)
        self.tour += 1

        gagnant, cases = verifier_gagnant(self.grille)
        if gagnant:
            self.fini = True
            for (rr, cc) in cases:
                self.canvas.itemconfig(self.rects[(rr, cc)], fill=WIN_COL)
                self.canvas.itemconfig(self.texts[(rr, cc)], fill=BG)
            self.status_var.set(f"Joueur {gagnant} a gagne !")
            return

        if self.tour == 9:
            self.fini = True
            self.status_var.set("Match nul !")
            return

        self._set_status()

    def _set_status(self):
        joueur = self.joueurs[self.tour % 2]
        self.status_var.set(f"Tour du joueur  {joueur}")

    def _reset(self):
        self.grille = [[" "] * 3 for _ in range(3)]
        self.tour   = 0
        self.fini   = False
        self._draw_grid()
        self._set_status()

if __name__ == "__main__":
    root = tk.Tk()
    MenuWindow(root)
    root.mainloop()
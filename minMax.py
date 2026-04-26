import math
import copy


def coups_possibles(grille, cases_bloquees):
    """Retourne les cases encore jouables."""
    taille = len(grille)
    return [
        (i, j)
        for i in range(taille)
        for j in range(taille)
        if grille[i][j] == " " and (i, j) not in cases_bloquees
    ]


def lignes_gagnantes(taille):
    """Construit toutes les lignes utiles."""
    lignes = []

    # Lignes horizontales
    for i in range(taille):
        lignes.append([(i, j) for j in range(taille)])

    # Lignes verticales
    for j in range(taille):
        lignes.append([(i, j) for i in range(taille)])

    # Grande diagonale
    lignes.append([(i, i) for i in range(taille)])

    # Diagonale inverse
    lignes.append([(i, taille - 1 - i) for i in range(taille)])

    return lignes


def evaluer_ligne(contenu_ligne, symbole_ia, symbole_humain):
    """Donne un score simple à une ligne."""
    nb_ia = contenu_ligne.count(symbole_ia)
    nb_humain = contenu_ligne.count(symbole_humain)
    nb_vides = contenu_ligne.count(" ")

    # Ligne bloquée des deux côtés
    if nb_ia > 0 and nb_humain > 0:
        return 0

    # Lignes favorables à l'IA
    if nb_ia > 0 and nb_humain == 0:
        if nb_ia == 1:
            return 1
        elif nb_ia == 2:
            return 5
        elif nb_ia == 3:
            return 20
        else:
            return 100

    # Lignes favorables à l'humain
    if nb_humain > 0 and nb_ia == 0:
        if nb_humain == 1:
            return -1
        elif nb_humain == 2:
            return -5
        elif nb_humain == 3:
            return -20
        else:
            return -100

    # Ligne vide
    if nb_vides == len(contenu_ligne):
        return 0

    return 0


def evaluer_plateau(morpion, symbole_ia="O", symbole_humain="X"):
    """Évalue rapidement la position sans finir tout l'arbre."""
    gagnant = morpion.obtenir_gagnant()

    if gagnant == symbole_ia:
        return 1000
    if gagnant == symbole_humain:
        return -1000
    if morpion.verifier_match_nul():
        return 0

    score = 0
    for ligne in lignes_gagnantes(morpion.taille):
        contenu = [morpion.grille[i][j] for i, j in ligne]

        # On ignore les lignes cassées par une case bloquée
        if "#" in contenu:
            continue

        score += evaluer_ligne(contenu, symbole_ia, symbole_humain)

    return score


def minmax_alpha_beta(
    morpion,
    profondeur,
    profondeur_max,
    alpha,
    beta,
    maximisant,
    symbole_ia="O",
    symbole_humain="X",
):
    """MinMax optimisé avec coupe alpha-bêta."""
    gagnant = morpion.obtenir_gagnant()

    # Fin naturelle
    if gagnant == symbole_ia:
        return 1000 - profondeur, None
    if gagnant == symbole_humain:
        return -1000 + profondeur, None
    if morpion.verifier_match_nul():
        return 0, None

    # Limite de profondeur
    if profondeur >= profondeur_max:
        return evaluer_plateau(morpion, symbole_ia, symbole_humain), None

    actions = coups_possibles(morpion.grille, morpion.cases_bloquees)

    if not actions:
        return evaluer_plateau(morpion, symbole_ia, symbole_humain), None

    if maximisant:
        meilleur_score = -math.inf
        meilleur_coup = None

        for i, j in actions:
            copie = copy.deepcopy(morpion)
            copie.jouer_symbole(i, j, symbole_ia)

            score, _ = minmax_alpha_beta(
                copie,
                profondeur + 1,
                profondeur_max,
                alpha,
                beta,
                False,
                symbole_ia,
                symbole_humain,
            )

            if score > meilleur_score:
                meilleur_score = score
                meilleur_coup = (i, j)

            alpha = max(alpha, meilleur_score)

            # Coupe alpha-bêta
            if beta <= alpha:
                break

        return meilleur_score, meilleur_coup

    else:
        meilleur_score = math.inf
        meilleur_coup = None

        for i, j in actions:
            copie = copy.deepcopy(morpion)
            copie.jouer_symbole(i, j, symbole_humain)

            score, _ = minmax_alpha_beta(
                copie,
                profondeur + 1,
                profondeur_max,
                alpha,
                beta,
                True,
                symbole_ia,
                symbole_humain,
            )

            if score < meilleur_score:
                meilleur_score = score
                meilleur_coup = (i, j)

            beta = min(beta, meilleur_score)

            # Coupe alpha-bêta
            if beta <= alpha:
                break

        return meilleur_score, meilleur_coup


def coup_ia_minmax(morpion, symbole_ia="O", symbole_humain="X"):
    """Choisit automatiquement une profondeur raisonnable."""
    if morpion.taille == 3:
        profondeur_max = 9
    elif morpion.taille == 4:
        profondeur_max = 4
    else:
        profondeur_max = 3

    _, coup = minmax_alpha_beta(
        morpion=morpion,
        profondeur=0,
        profondeur_max=profondeur_max,
        alpha=-math.inf,
        beta=math.inf,
        maximisant=True,
        symbole_ia=symbole_ia,
        symbole_humain=symbole_humain,
    )

    return coup
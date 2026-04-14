# from morpion import Morpion
# Algorithme MinMax pour le morpion
import copy

def coups_possibles(grille, cases_bloquees):
	taille = len(grille)
	return [
		(i, j)
		for i in range(taille)
		for j in range(taille)
		if grille[i][j] == " " and (i, j) not in cases_bloquees
	]

def minmax(morpion, profondeur, maximisant):
	# Verifie si la partie est terminee
	if morpion.verifier_victoire("X"):
		return -1, None  # X gagne
	if morpion.verifier_victoire("O"):
		return 1, None   # O gagne
	if morpion.verifier_match_nul():
		return 0, None  # Match nul

	if maximisant:
		meilleur_score = -float('inf')
		meilleur_coup = None
		for (i, j) in coups_possibles(morpion.grille, morpion.cases_bloquees):
			copie = copy.deepcopy(morpion)
			copie.grille[i][j] = "O"
			score, _ = minmax(copie, profondeur + 1, False)
			if score > meilleur_score:
				meilleur_score = score
				meilleur_coup = (i, j)
		return meilleur_score, meilleur_coup
	else:
		meilleur_score = float('inf')
		meilleur_coup = None
		for (i, j) in coups_possibles(morpion.grille, morpion.cases_bloquees):
			copie = copy.deepcopy(morpion)
			copie.grille[i][j] = "X"
			score, _ = minmax(copie, profondeur + 1, True)
			if score < meilleur_score:
				meilleur_score = score
				meilleur_coup = (i, j)
		return meilleur_score, meilleur_coup

def coup_ia_minmax(morpion):
	"""Renvoie le meilleur coup pour l'IA (O) avec MinMax."""
	_, coup = minmax(morpion, 0, True)
	return coup

#! python3

import sys

JoueurBlanc = 0
JoueurNoir = 1
GainPerdu = -1
GainGagne = 1

RetraitMaximum = 3

# Flip-flop sur le joueur
def autreJoueur(joueur):
	return JoueurNoir if joueur == JoueurBlanc else JoueurBlanc

# Résultat du meilleur coup
def meilleurCoup(nombreAllumettes, joueur):
	valeurCoupMax = GainPerdu
	meilleurRetrait = 1
	# Pour chaque coup possible
	for retrait in range(1, min(RetraitMaximum, nombreAllumettes)+1):
		valeurDuCoupJoue = valeurDuCoup(nombreAllumettes-retrait, joueur)
		# Mise à jour possible du meilleur coup
		if valeurDuCoupJoue > valeurCoupMax:
			valeurCoupMax = valeurDuCoupJoue
			meilleurRetrait = retrait
	return meilleurRetrait

# Évaluation la plus pessimiste
def valeurDuCoup(nombreAllumettes, joueur):
	valeurCoupMax = GainGagne
	if nombreAllumettes == 0:	# Plus rien à prendre : on perd
		valeurCoupMax = GainPerdu
	else:
		# Pour chaque coup possible
		for retrait in range(1, min(RetraitMaximum, nombreAllumettes)+1):
			valeurDuCoupJoue = valeurDuCoupAdverse(nombreAllumettes-retrait, autreJoueur(joueur))
			# Mise à jour possible du pire coup
			if valeurDuCoupJoue < valeurCoupMax:
				valeurCoupMax = valeurDuCoupJoue
	return valeurCoupMax

# Évaluation la plus optimiste (de l'adversaire)
def valeurDuCoupAdverse(nombreAllumettes, joueurAdverse):
	valeurCoupMax = GainPerdu
	if nombreAllumettes == 0:	# Plus rien à prendre : on gagne
		valeurCoupMax = GainGagne
	else:
		# Pour chaque coup possible
		for retrait in range(1, min(RetraitMaximum, nombreAllumettes)+1):
			valeurDuCoupJoue = valeurDuCoup(nombreAllumettes-retrait, autreJoueur(joueurAdverse))
			# Mise à jour possible du meilleur coup
			if valeurDuCoupJoue > valeurCoupMax:
				valeurCoupMax = valeurDuCoupJoue
	return valeurCoupMax

def allumettesDuJeu(chaine):
	try:
		nombreAllumettes = int(chaine)
	except:
		nombreAllumettes = 6
	return nombreAllumettes

def programmePrincipal():
	nombreAllumettes = allumettesDuJeu(sys.argv[1] if len(sys.argv) > 1 else  "")
	joueur = JoueurBlanc
	
	while nombreAllumettes != 0:
		resultat = meilleurCoup(nombreAllumettes, joueur)
		nombreAllumettes -= resultat
		print("Joueur {} retire {} alumette{} :\treste{} {}".format(
			"JoueurBlanc" if joueur == JoueurBlanc else "JoueurNoir",
			resultat,
			"s" if resultat >= 2 else "",
			"nt" if nombreAllumettes >= 2 else "",
			nombreAllumettes))
		joueur = autreJoueur(joueur)
	
	print(f"Joueur {'JoueurBlanc' if joueur == JoueurBlanc else 'JoueurNoir'} gagne")

if __name__ == "__main__":
	programmePrincipal()

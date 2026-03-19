#on definit une constante pour representer une case vide 

VIDE=" "

# fonction cree une grille vide 3x3
def initialiser_grille():
    return[[VIDE] *3 for _ in range(3)]

#fonction affiche la grille dans le terminal
def afficher_grille(grille):
    print()
    for i, ligne in enumerate(grille):
        print(" | ".join(ligne)) #la ligne est comme : X|O|X
        if i<2:
            print("_" *9)  # separation entre les lignes
        print()
        
        #cette fonction retourne la liste des coups possibles
        #un coup possible = une case encore vide
        # on renvoit sous formwe de lignes et de colonnes
    def coup_possibles(grille):
        actions =[]
        
        for i in range(3):
            for j in range(3):
                if grille[i][j] == VIDE:
                    actions.append((i,j))
        return actions
    # cette fonction joue un coup si la case et valide
    def jouer_coup(grille,ligne,col,joueur):
        if 0 <= ligne <=2 and 0 <= col <= 2 and grille[ligne][col]== VIDE:
            grille[ligne][col]= joueur
            return True
        return False
    
    #cette fonction verifie s'il y'a un gagnant
    def verifier_gagnant(grille):
        #verification de la colonnes 
        for i in range(3):
            #verification de la ligne i
            if grille[i][0]==grille[i][1] == grille[i][2]!= VIDE:
                return grille[i][0]
            
            #verification de la colonne i
            if grille[0][i] == grille[1][i] == grille[2][i] != VIDE:
                return grille[0][i]
            #verifie la diagonale principale
            if grille[0][0] == grille[1][1] == grille[2][0] != VIDE:
                return[0][0]
            #Verifie la deuxieme diagonale
            if grille[0][2] == grille[1][1] == grille[2][0] != VIDE:
                return[0][2]
            
            #AUCUN GAGNANT
            return None
        
        #cette fonction verifie si la grille est pleine
        def grille_pleine(grille):
            for ligne in grille:
                for case in ligne:
                    if case == VIDE:
                        return false
            return True
        
        #cette fonction dit si la parti est terminee
        def etat_terminal(grille):
            return verifier_gagnant(grille) is not None or grille_pleine(grille)
        
        #cette fonction transforme la grille en tuple
        #cette representation est utile pour l'IA car les tuples peuvent servir de cle dan un dictionnaire python
        def etat_grille(grille):
            return tuple(case for ligne in grille for case in ligne)
        
            
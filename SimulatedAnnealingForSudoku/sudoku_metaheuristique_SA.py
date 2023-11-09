import random
import numpy as np
import math 
from random import choice
import statistics 


#? Prend en entrée un tableau à deux dimensions de 9x9 (c'est-à-dire une liste de listes) et l'imprime dans un format qui représente une grille de Sudoku
def  afficher_sudoku(sudoku):
    print("\n")
    for i in range(len(sudoku)):
        ligne = ""
        if i == 3 or i == 6:
            print("---------------------")
        for j in range(len(sudoku[i])):
            if j == 3 or j == 6:
                ligne += "| "
            ligne += str(sudoku[i,j])+" "
        print(ligne)

#? La fonction convertit toutes les valeurs remplies en 1, laissant les cellules vides comme des 0
def ValSudokuFixe(sudoku_fixe):
    for i in range (0,9):
        for j in range (0,9):
            if sudoku_fixe[i,j] != 0:
                sudoku_fixe[i,j] = 1
    
    return(sudoku_fixe)

#? Cette fonction prend en entrée trois arguments et retourne le nombre d'erreurs dans une ligne et une colonne données d'une grille de Sudoku
def CalculerNbrErreursLigneColonne(ligne, colonne, sudoku):
    Nbr_erreurs = (9 - len(np.unique(sudoku[:,colonne]))) + (9 - len(np.unique(sudoku[ligne,:])))
    return(Nbr_erreurs)

#? une fonction qui calcule le nombre total d'erreurs dans une grille de Sudoku donnée
def CalculerNbrErreurs(sudoku):
    Nbr_erreurs = 0 
    for i in range (0,9):
        Nbr_erreurs += CalculerNbrErreursLigneColonne(i ,i ,sudoku)
    return(Nbr_erreurs)

#? crée une liste de listes où chaque liste interne contient les indices de ligne et de colonne d'un bloc 3x3 dans une grille de Sudoku
def CreerListe3x3Blocs ():
    ListeDeBlocsFinal = []
    for r in range (0,9):
        tmpListe = []
        block1 = [i + 3*((r)%3) for i in range(0,3)]
        block2 = [i + 3*math.trunc((r)/3) for i in range(0,3)]
        for x in block1:
            for y in block2:
                tmpListe.append([x,y])
        ListeDeBlocsFinal.append(tmpListe)
    return(ListeDeBlocsFinal)

#? remplir les cases vide avec une valeur aléatoire choisie parmi les chiffres de 1 à 9 qui ne sont pas déjà présents dans le bloc 3x3 en question, grâce à la fonction "choice" de la bibliothèque random
def RemplissageAleatoire3x3blocs(sudoku, listDeBlocs):
    for block in listDeBlocs:
        for box in block:
            if sudoku[box[0],box[1]] == 0:
                BlocCourant = sudoku[block[0][0]:(block[-1][0]+1),block[0][1]:(block[-1][1]+1)]
                sudoku[box[0],box[1]] = choice([i for i in range(1,10) if i not in BlocCourant])
    return sudoku

#? La fonction parcourt chaque coordonnée dans la liste et ajoute la valeur de la case correspondante à une somme finale
def SommeDUnBloc (sudoku, UnBloc):
    SommeFinal = 0
    for box in UnBloc:
        SommeFinal += sudoku[box[0], box[1]]
    return(SommeFinal)

#? la fonction vérifie que les deux cases sélectionnées ne sont pas déjà remplies avec une valeur fixe de la grille,Si les deux cases sélectionnées ne sont pas déjà remplies, la fonction retourne un tuple contenant ces deux cases
def DeuxCasesAleatoireDansUnBloc(SudokuFixe, block):
    while (1):
        PremierBox = random.choice(block)
        DeuxiemeBox = choice([box for box in block if box is not PremierBox ])

        if SudokuFixe[PremierBox[0], PremierBox[1]] != 1 and SudokuFixe[DeuxiemeBox[0], DeuxiemeBox[1]] != 1:
            return([PremierBox, DeuxiemeBox])

#? La fonction prend en entrée un sudoku et deux coordonnées correspondant à deux cases qui seront échangées
def RetournerBoxes(sudoku, boxesARetourner):
    SudokuPropose = np.copy(sudoku)
    PlaceReserve = SudokuPropose[boxesARetourner[0][0], boxesARetourner[0][1]]
    SudokuPropose[boxesARetourner[0][0], boxesARetourner[0][1]] = SudokuPropose[boxesARetourner[1][0], boxesARetourner[1][1]]
    SudokuPropose[boxesARetourner[1][0], boxesARetourner[1][1]] = PlaceReserve
    return (SudokuPropose)

#? génère une proposition d'état pour le sudoku en entrée en effectuant des changements aléatoires à deux cases d'un bloc choisi au hasard
def EtatPropose (sudoku, SudokuFixe, listDeBlocs):
    BlocAleatoire = random.choice(listDeBlocs)

    if SommeDUnBloc(SudokuFixe, BlocAleatoire) > 6:  
        return(sudoku, 1, 1)
    boxesARetourner = DeuxCasesAleatoireDansUnBloc(SudokuFixe, BlocAleatoire)
    SudokuPropose = RetournerBoxes(sudoku,  boxesARetourner)
    return([SudokuPropose, boxesARetourner])

#?
def ChoisirNouveauEtat (SudokuCourant, SudokuFixe, listDeBlocs, temperature):
    proposition = EtatPropose(SudokuCourant, SudokuFixe, listDeBlocs)
    nouveauSudoku = proposition[0]
    boxesAVerifier = proposition[1]
    #CoutCourant = CalculerNbrErreursLigneColonne(boxesAVerifier[0][0], boxesAVerifier[0][1], SudokuCourant) + CalculerNbrErreursLigneColonne(boxesAVerifier[1][0], boxesAVerifier[1][1], SudokuCourant)
    #nouvelCout = CalculerNbrErreursLigneColonne(boxesAVerifier[0][0], boxesAVerifier[0][1], nouveauSudoku) + CalculerNbrErreursLigneColonne(boxesAVerifier[1][0], boxesAVerifier[1][1], nouveauSudoku)
    CoutCourant = CalculerNbrErreurs(SudokuCourant)
    nouvelCout = CalculerNbrErreurs(nouveauSudoku)
    DifferenceDeCout = nouvelCout - CoutCourant
    rho = math.exp(-DifferenceDeCout/temperature)
    if(np.random.uniform(1,0,1) < rho):
        return([nouveauSudoku, DifferenceDeCout])
    return([SudokuCourant, 0])

#?cette fonction calcule le nombre de cases non vides dans la grille de sudoku, ce qui correspond également au nombre d'itérations nécessaires pour remplir complètement la grille
def ChoisirNombreDIterations(sudoku_fixe):
    nombreDItterations = 0
    for i in range (0,9):
        for j in range (0,9):
            if sudoku_fixe[i,j] != 0:
                nombreDItterations += 1
    return nombreDItterations

#?
def CalculerTemperatureInitiale (sudoku, SudokuFixe, listDeBlocs):
    listDeDifferences = []
    tmpSudoku = sudoku
    for i in range(1,10):
        tmpSudoku = EtatPropose(tmpSudoku, SudokuFixe, listDeBlocs)[0]
        listDeDifferences.append(CalculerNbrErreurs(tmpSudoku))
    return (statistics.pstdev(listDeDifferences))

#?
def ResoudreSudoku (sudoku):
    f = open("scores.txt", "a")
    solutionTrouve = 0
    while (solutionTrouve == 0):
        FacteurDeDecroissance = 0.99
        decompteBloque = 0
        SudokuFixe = np.copy(sudoku)
        afficher_sudoku(sudoku)
        ValSudokuFixe(SudokuFixe)
        listDeBlocs = CreerListe3x3Blocs()  
        tmpSudoku = RemplissageAleatoire3x3blocs(sudoku, listDeBlocs)
        temperature = CalculerTemperatureInitiale(sudoku, SudokuFixe, listDeBlocs)
        score = CalculerNbrErreurs(tmpSudoku)
        iterations = ChoisirNombreDIterations(SudokuFixe)
        if score <= 0:
            solutionTrouve = 1

        while solutionTrouve == 0:
            ScorePrecedent = score
            for i in range (0, iterations):
                nouveauEtat = ChoisirNouveauEtat(tmpSudoku, SudokuFixe, listDeBlocs, temperature)
                tmpSudoku = nouveauEtat[0]
                DifferenceScore = nouveauEtat[1]
                score += DifferenceScore
                print(score)
                f.write(str(score) + '\n')
                if score <= 0:
                    solutionTrouve = 1
                    break

            temperature *= FacteurDeDecroissance
            if score <= 0:
                solutionTrouve = 1
                break
            if score >= ScorePrecedent:
                decompteBloque += 1
            else:
                decompteBloque = 0
            if (decompteBloque > 80):
                temperature += 2
            if(CalculerNbrErreurs(tmpSudoku)==0):
                afficher_sudoku(tmpSudoku)
                break
    f.close()
    return(tmpSudoku)

sudokuDeDepart = """
                    207010605
                    095600423
                    800004000
                    700000260
                    000726018
                    020090030
                    050000307
                    604530000
                    012079000
                """
#? crée un tableau numpy sudoku à partir d'une chaîne de caractères sudokuDeDepart qui représente l'état initial d'une grille de Sudoku
sudoku = np.array([[int(i) for i in ligne] for ligne in sudokuDeDepart.split()])


solution = ResoudreSudoku(sudoku)
print(CalculerNbrErreurs(solution))
afficher_sudoku(solution)

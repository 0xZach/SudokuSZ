import numpy as np
import random as r


# renvois les coordonnées à utiliser pour regarder autour du chiffre
def getPos_around(nbr):
    check = nbr%3
    if check == 0:
        return [0,1,2]
    elif check == 1:
        return [-1,0,1]
    else:
        return [-2,-1,0]




def check_pos_Horizontal(sudoku, position, number):
    for i in range(0,9):
        if i != position[1]:
            if sudoku[position[0]][i] == number:
                return False
    return True




def check_pos_Vertical(sudoku, position, number):
    for i in range(0,9):
        if i != position[0]:
            if sudoku[i][position[1]] == number:
                return False
    return True




def check_pos_around(sudoku, position, number):
    compareX = getPos_around(position[0])
    compareY = getPos_around(position[1])


    for X in compareX: # in test: [0,1,2]
        for Y in compareY: # in test: [-2,-1,0]
            if X != 0 and Y != 0:
                if sudoku[ position[0] + X ][ position[1] + Y ] == number:
                    return False
    
    return True




# on prent en paramètre le sudoku ainsi que les coordonnées ou l'on souhaite placer le chiffre
# 
# on retourne vrai si la position est bonne, faux dans le cas contraire
def check_pos(sudoku, position, number):

    # check horizontal
    if check_pos_Horizontal(sudoku, position, number) == True:

        # check vertical
        if check_pos_Vertical(sudoku, position, number) == True:

            # check around
            if check_pos_around(sudoku, position, number) == True:
                return True
    
    return False




# cette partie créée le premier bloc sur lequel se basera l'algorithme RD3
def first_bloc(sudoku):
    
    oneToNine = [i for i in range(1,10)]
    r.shuffle(oneToNine)
    boolUseful = False
    i = 0
    

    while(i < 9):
        
        if i == 0 or i%3 == 0:
            rowPlacing = r.randrange(0,3)
            if i > 0 and sudoku[rowPlacing][0] != 0:
                while sudoku[rowPlacing][0] != 0:
                    rowPlacing = r.randrange(0,3)
            
        
        
        
        columPlacing = r.randrange(0,3)
        if sudoku[rowPlacing][columPlacing] == 0:
            sudoku[rowPlacing][columPlacing] = oneToNine[i]
            i+=1
    


    
    return sudoku




# cet algorithme place les chiffres en fonction de la première boite: 
# si on a un 1 en 0,0 il sera là en 1,3 puis 2,6 
# 
#
# si tu vois ça, bah j'ai merdé car ça veut dire que tu connais la strat
def algo_RD3():
    # on créé la structure du sudoku et on y ajoute directement la première boite
    sudoku = first_bloc(np.array([[0 for i in range(9)] for j in range(9)]))
    
    # décalage entre chaque nombre
    decalageVert = 3
    decalageHori = 1

    # décalage entre chaque bloc
    column = 0
    decalageBloc = 0
    
    # on fait colonne par colonne
    while(column <= 6):

        # puis bloc par bloc
        while(decalageBloc < 6):
            for i in range(decalageBloc,decalageBloc+3):
                for j in range(column,column+3):
                    
                    # si on est à la fin de la ligne ET de la colonne
                    if (decalageHori+j)%3 == 0 and (decalageVert+i)%3 == 2:
                        sudoku[(decalageVert+i)-2][(decalageHori+j)-3] = sudoku[i][j]

                    # si on est à la fin de la ligne mais pas à la fin de la colonne
                    elif (decalageHori+j)%3 == 0:
                        sudoku[i+decalageVert+1][(decalageHori+j)-3] = sudoku[i][j]

                    # cas normal
                    else:
                        sudoku[i+decalageVert][j+decalageHori] = sudoku[i][j]
            
            # on passe au bloc du dessous
            decalageBloc += 3
        
        # on passe à la colonne suivante
        column +=3
        
        # on ajoute le premier bloc de la prochaine colonne séparemment
        if column <= 6:

            for i in range(decalageBloc,decalageBloc+3):
                for j in range(3):

                    if (j)%3 == 2 and (i)%3 == 2:
                        sudoku[i-decalageBloc-2][(decalageHori+j)%3+column] = sudoku[i][j+column-3]

                    elif (j)%3 == 2:
                        sudoku[i-decalageBloc+1][(decalageHori+j)%3+column] = sudoku[i][j+column-3]

                    else:
                        sudoku[i-decalageBloc][j+decalageHori+column] = sudoku[i][j+column-3]
        
        decalageBloc = 0 # on remet à 0 le decalage Bloc pour la nouvelle ligne




    
    return sudoku



# sert à vérifier si la grille de sudoku fonctionne
def is_sudoku_perfect(sudoku):
    

    for i in range(0,9):
        for j in range(0,9):
            if check_pos(sudoku, [i,j], sudoku[i][j]) == False:
                return False
    return True



# finds instances of the argument toSearch and returns an array of it's position(s)
def findInstances(array2D,toSearch):
    positions = []
    for i in range(len(array2D)):
        for j in range(len(array2D[i])):
            if array2D[i][j] == toSearch:
                positions.append([i,j])

    return positions



def get_sudoku(sudoku_filled):
    final_sudoku = np.array(np.array([[0 for i in range(9)] for j in range(9)]))
    OneToNine = [i for i in range(1,10)]
    r.shuffle(OneToNine)
    howManyShown = [2,3,3,4,4,4,5,5,6]

    for i in range(9):
        instances = findInstances(sudoku_filled, OneToNine[i])

        for j in range(howManyShown[i]):
            whichShown = r.randrange(0,len(instances))
            
            final_sudoku[ instances[whichShown][0] ][ instances[whichShown][1] ] = OneToNine[i]
            instances.remove(instances[whichShown])

    return final_sudoku



def affichage(sudoku):
        
        affichage =  ["     A   B   C   D   E   F   G   H   I  "]
        affichage += ["   ╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗"]
        debutLigne = ""
        finLigne = ""

        for i in range(len(sudoku)):
            if i < 8 and i%3 != 2:
                finLigne = "   ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢"
            elif i == 8:
                finLigne = "   ╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝"
            elif i%3 == 2:
                finLigne = "   ╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣"
            
            debutLigne = " "+str(i+1)+" "

            for j in range(len(sudoku[i])):
                
                if j%3 == 0:
                    debutLigne += "║"
                else:
                    debutLigne += "│"

                if sudoku[i][j] != 0:
                    debutLigne += " "+str(sudoku[i][j]) + " "
                elif sudoku[i][j] == 0:
                    debutLigne += "   "
                
                if j == 8:
                    debutLigne += "║"
            
            affichage.append(debutLigne)
            affichage.append(finLigne)
            debutLigne = ""
        for i in affichage:
            print(i)




# checks if you won, that's it
def win(sudokuOriginal,sudokuHidden):
    return True if sudokuOriginal.all() == sudokuHidden.all() else False




def get_Coordinates(coordinates):
    alphabetAtoI = [chr(i) for i in range(65,74)]

    if len(coordinates) == 2:
        if (ord(coordinates[0]) >= 49 and ord(coordinates[0]) <= 57) and (ord(coordinates[1]) >= 65 and ord(coordinates[1]) <= 73):
            return([int(coordinates[0])-1,alphabetAtoI.index(coordinates[1])])

        elif (ord(coordinates[1]) >= 49 and ord(coordinates[1]) <= 57) and (ord(coordinates[0]) >= 65 and ord(coordinates[0]) <= 73):
            return([int(coordinates[1])-1,alphabetAtoI.index(coordinates[0])])
    else:
        return False




def affichageLives(nbrlives):
    
    afficher = "["
    
    for i in range(nbrlives):
        afficher += "█"
        if i < nbrlives-1:
            afficher += "-"
    
    if nbrlives < 3:
        for i in range(3-nbrlives):
            afficher += " "
    
    
    afficher += "]"
    
    
    return(afficher)




def play(language):
    # setup variables
    lives = 3
    sudoku = algo_RD3()
    sudoku_hidden = get_sudoku(sudoku)


    while win(sudoku,sudoku_hidden) != True and lives > 0:

        # affichage de début de tour
        if language == "EN":
            print("lives: ",affichageLives(lives))
        elif language == "FR":
            print("Vies: ",affichageLives(lives))
        affichage(sudoku_hidden)

        if language == "EN":
            tile = get_Coordinates(input("which tile?"))
        elif language == "FR":
            tile = get_Coordinates(input("Quelle case ?"))

        if tile == False:
            
            if language == "EN":
                print("The coordinates must be written as this example: 3A")
            elif language == "FR":
                print("les coordonnées doivent êtres écrites comme dans l'exemple çi-contre: 5C")
            
        
        else:
            if sudoku_hidden[tile[0]][tile[1]] == 0:
                if language == "EN":
                    numberToPlace = input("Which number do you want to place? ")
                elif language == "FR":
                    numberToPlace = input("Quel chiffre voulez vous placer ? ")

                while len(numberToPlace) == 0:
                    numberToPlace = input()
                
                while ord(numberToPlace) < 49 and ord(numberToPlace) > 57:
                    if language == "EN":
                        print("you need to choose a number between 1 and 9.")
                        numberToPlace = input("Which number do you want to place? ")
                    elif language == "FR":
                        print("Vous devez choisir un nombre entre 1 et 9")
                        numberToPlace = input("Quel chiffre voulez vous placer ? ")
                    
                    while len(numberToPlace) == 0:
                        numberToPlace = input()
                        
                   
                numberToPlace = int(numberToPlace)



                while numberToPlace < 0 or numberToPlace > 10:

                    if language == "EN":
                        print("you need to choose a number between 1 and 9.")
                        numberToPlace = input("Which number do you want to place? ")
                    elif language == "FR":
                        print("Vous devez choisir un nombre entre 1 et 9")
                        numberToPlace = input("Quel chiffre voulez vous placer ? ")
                    
                    while len(numberToPlace) == 0:
                        numberToPlace = input()
                    
                    
                if check_pos(sudoku, tile, numberToPlace) == True:
                    sudoku_hidden[tile[0]][tile[1]] = numberToPlace
                
                else:

                    if language == "EN":
                        print("you can't place this number here,\n -1 life!")
                    elif language == "FR":
                        print("Vous ne pas placer ce chiffre ici,\n -1 vie!")
                    
                    lives -= 1
            
            else:

                if language == "EN":
                    print("You can't place a number here.")
                elif language == "FR":
                    print("Vous ne pouvez pas placer de chiffre ici.")
                
    if lives > 0:
        if language == "EN":
            print("You won!")
        elif language == "FR":
            print("Vous avez gagné!")
    elif lives == 0:
        if language == "EN":
            print("You lose!")
        elif language == "FR":
            print("Vous avez perdu!")





# -------------------------------------------------------------------------------------------------------------------------------------------- #

#                                                              GAME PHASE                                                                      #

# -------------------------------------------------------------------------------------------------------------------------------------------- #



endGame = False
language = "EN"

while endGame != True:
    print("||------------------||")
    print("||                  ||")
    print("|| Actions:         ||")
    print("||                  ||")
    if language == "EN":
        print("|| 1 - Play         ||")
        print("|| 2 - options      ||")
        print("|| 3 - Quit         ||")
    elif language == "FR":
        print("|| 1 - Jouer        ||")
        print("|| 2 - options      ||")
        print("|| 3 - Quitter      ||")
    print("||                  ||")
    print("||------------------||")

    action = input()
    while len(action) == 0:
        action = input()

    if ord(action) >= 49 and ord(action) <= 51:
        
        action = int(action)
        
        
        if   action == 1:
            play(language)

        elif action == 2:
            print("||--------------------------||")
            print("||                          ||")
            print("|| Actions:                 ||")
            print("||                          ||")
            if language == "EN":
                print("|| 1 - Change Language      ||")
                print("|| 2 - Return               ||")
            elif language == "FR":
                print("|| 1 - Changer de langue    ||")
                print("|| 2 - Retour               ||")
            print("||                          ||")
            print("||--------------------------||")
        
            action = input()
            while len(action) == 0:
                action = input()
            


            if ord(action) >= 49 and ord(action) <= 50:
                action = int(action)

                if int(action) == 1:
                    print("||--------------------------||")
                    print("||                          ||")
                    print("|| Actions:                 ||")
                    print("||                          ||")
                    print("|| 1 - Français             ||")
                    print("|| 2 - English              ||")
                    if language == "EN":
                        print("|| 3 - Return               ||")
                    elif language == "FR":
                        print("|| 3 - Retour               ||")
                    print("||                          ||")
                    print("||--------------------------||")

                    action = input()
                    if ord(action) >= 49 and ord(action) <= 51:
                        action = int(action)

                        if action == 1:
                            language = "FR"
                        elif action == 2:
                            language = "EN"
        elif action == 3:
            endGame = True
    else:
        print(" ")

print("See you next time!")

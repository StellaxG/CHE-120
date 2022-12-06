import random
import sys 
import numpy as np #importing numpy for array functionality
import tabulate as tabulate #imported tabulate library for new graphic for game 

WIDTH = 10 #changing dimensions of the board from 8x8 to 10x10
HEIGHT = 10

def highscore(player_score):
    highscores = [] #creates an empty list for new highscores
    originalscores = [] #creates an empty list for old highscores for comparison purposes
    file_path = '/Users/yangsmacbook/Documents/UW 1A/CHE120/highscores.txt' #file path to txt file with highscores 
    with open(file_path) as file_object:
        lines = file_object.read().splitlines() #reads lines of highscores to a list called lines
    for line in lines:
        highscores.append(int(line)) #appends scores to highscores list
        originalscores.append(int(line)) #appends scores to original scores list 

    highscores.append(player_score) #appends new score to highscore list 
    highscores_sorted = sorted(highscores) #sorts highscore list with new player score 
    originalscores.reverse() #reverses original score list for comparison purposes

    with open('/Users/yangsmacbook/Documents/UW 1A/CHE120/highscores.txt', 'w') as file_object: #opens the highscores.txt file for writing
        for i in range(-1, -6, -1): #goes from larget element backwards in list
            if i == -1:
                file_object.write((str(highscores_sorted[i]))) #writes new highscores to txt file 
            else:
                file_object.write(('\n' + str(highscores_sorted[i])))

    for i in range(-1, -6, -1):
        if originalscores[i] != highscores_sorted[i+1]: #if the new highscores list is different than the original scores list, then a highscore was recorded
            return True #therefore, return true
        else:
            return False #else, return false

def drawBoard(board): #new graphic function 

    letter_index = np.array(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']).reshape(10,1) #creating a 10x1 array for the sides of the table
    indexes = np.array([' ', '1',  '2', '3', '4', '5', '6', '7', '8', '9', '10', ' ']) #creating a 1x12 array for the top and bottom of the table
    title = np.array(['R', 'E',  'V', 'E', 'R', 'S', 'E', ' ', 'G', 'A', 'M', 'E']) #creating a 1x12 array for the very top title of the table
    new_table = np.hstack((letter_index, board, letter_index)) #joining the arrays to the table given to the function
    new_table = np.vstack([title, indexes, new_table, indexes]) 
    table = tabulate.tabulate(new_table, tablefmt = 'fancy_grid') #using tabulate function to create function

    print(table) #printing graphic 

def getNewBoard():
    board = []
    for i in range(WIDTH):
        board.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']) #changed to an empty list with 10 possible elements
    return board

def isOnBoard(x, y):
    return x >= 0 and x <= WIDTH - 1 and y >= 0 and y <= HEIGHT - 1

def getBoardCopy(board):
    boardCopy = getNewBoard()
    for x in range(WIDTH):
        for y in range(HEIGHT):
            boardCopy[x][y] = board[x][y]
    return boardCopy

def getValidMoves(board, tile):
    validMoves = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if isValidMove(board, tile, x, y) != False: 
                validMoves.append([x, y])
    return validMoves

def getBoardWithValidMoves(board, tile):
    boardCopy = getBoardCopy(board)
    for x, y in getValidMoves(boardCopy, tile):
        boardCopy[x][y] = '.'
    return boardCopy

def makeMove(board, tile, xstart, ystart):
    tilesToFlip = isValidMove(board, tile, xstart, ystart)
    if tilesToFlip == False:
        return False
    board[xstart][ystart] = tile 
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True

def isOnCorner(x, y):
    return (x == 0 or x == WIDTH - 1) and (y == 0 or y == HEIGHT - 1)

def whoGoesFirst():
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

def enterPlayerTile():
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Do you want to be X or O?')
        tile = input().upper() 
    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

def enterPlayerTilepvp(): #new function that is identical to enterPlayerTile function but with different print statements for pvp game 
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Does Player 1 want to be X or O?')
        tile = input().upper() 
    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

def getScoreOfBoard(board):
    xscore = 0
    oscore = 0
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {'X':xscore, 'O':oscore}

def printScore(board, playerTile, computerTile, player_player):
    scores = getScoreOfBoard(board)
    if player_player == False: #if pvc is enabled, print this
        print('You: %s points. Computer: %s points.' % (scores[playerTile], scores[computerTile])) 
    else: #else, print pvp message
        print('Player 1: %s points. Player 2: %s points.' % (scores[playerTile], scores[computerTile])) 

def getComputerMove(board, computerTile):
    possibleMoves = getValidMoves(board, computerTile)
    random.shuffle(possibleMoves)
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]
    bestScore = -1
    for x, y in possibleMoves:
        boardCopy = getBoardCopy(board)
        makeMove(boardCopy, computerTile, x, y)
        score = getScoreOfBoard(boardCopy)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove

def isValidMove(board, tile, xstart, ystart):
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False

    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    tilesToFlip = []

    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]: 

        x, y = xstart, ystart 
        x += xdirection 
        y += ydirection 

        while isOnBoard(x, y) and board[x][y] == otherTile:
            
            x += xdirection
            y += ydirection

            if isOnBoard(x, y) and board[x][y] == tile: 
                
                while True:

                    x -= xdirection 
                    y -= ydirection

                    if x == xstart and y == ystart:
                        break

                    tilesToFlip.append([x, y])

    if len(tilesToFlip) == 0:
        return False
    
    return tilesToFlip 

def getPlayerMove(board, playerTile):
 
    DIGITS1TO8 = '1 2 3 4 5 6 7 8 9'.split()
    ALPHAATOJ = 'a b c d e f g h i j'.split() #added valid user inputs for lettering check
    ALPHAATOJDIC = {'a': 0, 'b': 1, 'c': 2, 'd' : 3, 'e' : 4, 'f' : 5, 'g': 6, 'h' : 7, 'i' : 8, 'j' : 9} #dictionary to pair letters with their correct move values 
    
    while True:
        print('Enter your move, "quit" to end the game, or "hints" to toggle hints.')
        move = input().lower() 
        if move == 'quit' or move == 'hints':
            return move

        if (len(move) == 2 and move[0] in ALPHAATOJ and move[1] in DIGITS1TO8): #the first half of the user input is now evaluated using the valid lettering list
            x = ALPHAATOJDIC[move[0]] #if the move is valid, its corresponding value according to the dictionary is used for the move
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                continue
            else:
                break

        elif(len(move) == 3 and move[0] in ALPHAATOJ and move[1] == '1' and move[2] == '0'): #new if statement accounts for the 10 space
            x = ALPHAATOJDIC[move[0]]
            y = 9
            if isValidMove(board, playerTile, x, y) == False:
                continue 
            else:
                break

        else:
            print('That is not a valid move. Enter the row (a-j) and then the column (1-10).')
            print('For example, a10 will move on the top-right corner.')

    return [x, y]

def random_piece(board, tile):
    
    randx = np.random.randint(WIDTH) #gives a random width value 
    randy = np.random.randint(HEIGHT) #gives a random height value

    if board[randx][randy] == ' ': #if the given space on the table is a space
        board[randx][randy] = tile #gives that tile the specified tile value 
        return board
    else:
        random_piece(board, tile) #else, the code is run again until a space tile is found 

def playGamepvc(playerTile, computerTile, player_player): #player vs computer game function
    showHints = False
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first.')

    board = getNewBoard()
    board[4][4] = 'X' #new center pieces due to the larger board
    board[4][5] = 'O'
    board[5][4] = 'O'
    board[5][5] = 'X'

    if (random_pieces == True): #if user requested random pieces
        random_piece(board, 'X') #random pieces are created for the specified tile 
        random_piece(board, 'O')
        random_piece(board, 'X')
        random_piece(board, 'O')

    while True:
        playerValidMoves = getValidMoves(board, playerTile)
        computerValidMoves = getValidMoves(board, computerTile)

        if playerValidMoves == [] and computerValidMoves == []:
            return board

        elif turn == 'player':
            if playerValidMoves != []:
                if showHints:
                    validMovesBoard = getBoardWithValidMoves(board, playerTile)
                    drawBoard(validMovesBoard)
                else:
                    drawBoard(board)
                printScore(board, playerTile, computerTile, player_player)

                move = getPlayerMove(board, playerTile)
                if move == 'quit':
                    print('Thanks for playing!')
                    sys.exit()
                elif move == 'hints':
                    showHints = not showHints
                    continue
                else:
                    makeMove(board, playerTile, move[0], move[1])
            turn = 'computer'

        elif turn == 'computer':
            if computerValidMoves != []:
                drawBoard(board)
                printScore(board, playerTile, computerTile, player_player)

                input('Press Enter to see the computer\'s move.')
                move = getComputerMove(board, computerTile)
                makeMove(board, computerTile, move[0], move[1])
            turn = 'player'

def playGamepvp(playerTile, computerTile, player_player): #player vs player game function
    showHints = False
    turn = whoGoesFirst()
    if turn == 'computer': #new print statements for player vs player UI
        print('Player 2 will go first.')
    else:
        print('Player 1 will go first.')

    board = getNewBoard()
    board[4][4] = 'X'
    board[4][5] = 'O'
    board[5][4] = 'O'
    board[5][5] = 'X'

    if (random_pieces == True):
        random_piece(board, 'X')
        random_piece(board, 'O')
        random_piece(board, 'X')
        random_piece(board, 'O')

    while True:
        playerValidMoves = getValidMoves(board, playerTile)
        computerValidMoves = getValidMoves(board, computerTile)

        if playerValidMoves == [] and computerValidMoves == []:
            return board

        elif turn == 'player':
            if playerValidMoves != []:
                if showHints:
                    validMovesBoard = getBoardWithValidMoves(board, playerTile)
                    drawBoard(validMovesBoard)
                else:
                    drawBoard(board)
                printScore(board, playerTile, computerTile, player_player)

                move = getPlayerMove(board, playerTile)
                if move == 'quit':
                    print('Thanks for playing!')
                    sys.exit()
                elif move == 'hints':
                    showHints = not showHints
                    continue
                else:
                    makeMove(board, playerTile, move[0], move[1])
            turn = 'computer'

        elif turn == 'computer': #the player code is duplicated under the computer move to simplify variable names 
            if computerValidMoves != []:
                if showHints:
                    validMovesBoard = getBoardWithValidMoves(board, computerTile)
                    drawBoard(validMovesBoard)
                else:
                    drawBoard(board)
                printScore(board, computerTile, playerTile, player_player)

                move = getPlayerMove(board, computerTile)
                if move == 'quit':
                    print('Thanks for playing!')
                    sys.exit()
                elif move == 'hints':
                    showHints = not showHints
                    continue
                else:
                    makeMove(board, computerTile, move[0], move[1])
            turn = 'player'

print('Welcome to Reverse Game!')

continue_game = False #boolean values to keep tract of what settings the user desires
random_pieces = False
player_player = False
x_score = 0
o_score = 0
game_count = 1 #game count to count the number of games played 
repeat_game = ' ' #empty variables 
rand = ' '
pvp = ' '

while not (pvp[0] == 'p' or pvp[0] == 'c'): #prompts to ask user for preferred settings that continues to run until the first letter of the user input is valid 
    print('Player vs Player or Player vs Computer? (player, computer)')
    pvp = input().lower() #sets the user input to all lower case for easy verification
if (pvp[0] == 'p'): #if user requests pvp
    player_player = True #player vs player boolean is set as true, which later calls on the pvp game function
while not (repeat_game[0] == 't' or repeat_game[0] == 's'): #similar concept for the rest of the functions
    print('Would you like to play a single game or make it a best of three? (single, three)')
    repeat_game = input().lower()
if (repeat_game[0] == 't'):
    continue_game = True
while not (rand[0] == 'y' or rand[0] == 'n'):
    print('Would you like to start with two random tiles? (yes, no)')
    rand = input().lower()
if (rand[0] == 'y'):
    random_pieces = True

if player_player == False: #if user requested pvc
    playerTile, computerTile = enterPlayerTile() #messaging would read as player and computer tiles
else:
    playerTile, computerTile = enterPlayerTilepvp() #else, pvp specific messaging

while True:
    if player_player == False: #if user requested pvc
        finalBoard = playGamepvc(playerTile, computerTile, False) #pvc game function is called 
    else:
        finalBoard = playGamepvp(playerTile, computerTile, True)

    drawBoard(finalBoard)
    scores = getScoreOfBoard(finalBoard)

    print('This game, X scored %d points. O scored %d points.' % (scores['X'], scores['O']))

    if (highscore(scores['X']) == True): #if a new highscore was recorded
        print('New highscore for X! Here is the leaderboard now: ')
        file_path = '/Users/yangsmacbook/Documents/UW 1A/CHE120/highscores.txt'
        with open(file_path) as file_object:
            lines = file_object.read().splitlines() #create list of scores
            rank = 1
        for line in lines:
            print('Number %d: ' %(rank), end = '') #prints scores with associated ranking
            print(line)
            rank+=1

    if (highscore(scores['O']) == True): #if a new highscore was recorded
        print('New highscore for O! Here is the leaderboard now: ')
        file_path = '/Users/yangsmacbook/Documents/UW 1A/CHE120/highscores.txt'
        with open(file_path) as file_object:
            lines = file_object.read().splitlines() #creates list of scores
            rank = 1
        for line in lines:
            print('Number %d: ' %(rank), end = '') #prints scores with associated ranking
            print(line)
            rank+=1

    x_score += int(scores['X'])
    o_score += int(scores['O'])

    if player_player == True:
        print('In total, X scored %d points. O scored %d points.' % (x_score, o_score))

    if(continue_game == False or game_count == 3) and (player_player == True): #this messaging will only occur if user requested pvp (and depending on number of games requested)
        scores['O'] = o_score
        scores['X'] = x_score
        if scores[playerTile] > scores[computerTile]:
            print('Player 1 beat Player 2 by %s points! Congratulations!' % (scores[playerTile] - scores[computerTile]))
        elif scores[playerTile] < scores[computerTile]:
            print('Player 2 beat Player 1 by %s points! Congratulations!' % (scores[computerTile] - scores[playerTile]))
        else:
            print('The game was a tie!')

    elif(continue_game == False or game_count == 3) and (player_player == False): #this messaging will only occur if user requested pvp (and depending on number of games requested)
        scores['O'] = o_score
        scores['X'] = x_score
        if scores[playerTile] > scores[computerTile]:
            print('You beat the computer by %s points! Congratulations!' % (scores[playerTile] - scores[computerTile]))
        elif scores[playerTile] < scores[computerTile]:
            print('You lost. The computer beat you by %s points.' % (scores[computerTile] - scores[playerTile]))
        else:
            print('The game was a tie!')

    if(continue_game == True): #if the user requested for 3 games 
        if(game_count == 3): #if it has already been three games
            print('Do you want to play again? (yes or no)') #prompts user if they want to play again
            if not input().lower().startswith('y'): #if not yes
                print('Thanks for playing!') 
                break #breaks out of loop
        game_count += 1 #game count goes up by one
        print('Next game:')
    
    else: #if user requested one game 
        print('Do you want to play again? (yes or no)') #prompts user if they want to play again
        if not input().lower().startswith('y'): #if not yes
            print('Thanks for playing!') 
            break #breaks out of loop
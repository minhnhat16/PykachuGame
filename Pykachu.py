import os
PATH =  current_directory = os.getcwd()

import pygame,sys, random, copy, time, collection, os
from pygame.locals import *
from collections import defaultdict


TARGET_FPS = 30
S_WIDTH = 1280 #window width
S_HEIGHT = 720 # window height
BOX_SIZE = 75
BOARD_WIDHT = 14
BOARD_HEIGHT = 9
NUMBER_PAIRS = 21 #NUMHEROES_ONBOARD
REPEAT_PAIR_MAXIMUM = 4 # number pair can repeat
UI_TIME_BAR_LENGHT = 300 #time bar lenght
UI_TIME_BAR_WIDTH =30 
MAXIMUM_LEVEL = 5
LIVES = 10
GAME_TIME = 240
SHOW_HINT_TIME = 20

XMARGIN = (S_WIDTH - (BOX_SIZE *BOARD_WIDHT)) // 2
YMARGIN = (S_HEIGHT - (BOX_SIZE *BOARD_HEIGHT)) //2

# set up the colors 
GRAY = (100,100,100)
NAVY = (60,60,100)
WHITE = (255, 255, 255)
RED = (255, 0,0)
DARK_GREEN = (0, 175, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255 , 255)
BLACK = (0, 0 ,0)
BGCOLOR = NAVY
HIGHTLIGTH_COLOR = BLUE
BORDERCORLOR = RED


# setting up time bar
bar_position = (S_WIDTH // 2 - UI_TIME_BAR_LENGHT // 22, YMARGIN //2  - UI_TIME_BAR_WIDTH//2)
bar_size = (UI_TIME_BAR_LENGHT,UI_TIME_BAR_WIDTH)
borderColor = WHITE
bar_color = DARK_GREEN


# dict store icon champions img
LIST_CHAMPIONS = os.listdir(os.path.join(PATH, "championicons/converted"))

NUM_CHAMPS = len(LIST_CHAMPIONS)
CHAMPS_DICT = {}

if not LIST_CHAMPIONS:
    print("No champions found in the directory.")

for i, filename in enumerate(LIST_CHAMPIONS):
    full_path = os.path.join(PATH, "championicons/converted", filename)
    print(f"Loading image from: {full_path}")  # Debugging output
    try:
        image = pygame.image.load(full_path)
        CHAMPS_DICT[i + 1] = pygame.transform.scale(image, (BOX_SIZE, BOX_SIZE))
    except Exception as e:
        print(f"Error loading image {full_path}: {e}")

# Optional: Print the keys of CHAMPS_DICT for debugging
print("CHAMPS_DICT keys:", CHAMPS_DICT.keys())

#load  logo
lollogo = pygame.image.load(PATH + '/championicons/logo.jpg')
lollogo = pygame.transform.scale(lollogo,(45,45,))

#load BG

startBG = pygame.image.load('background/startBG.jpeg')
startBG = pygame.transform.scale(startBG,(S_WIDTH,S_HEIGHT))

# Path to the background directory
background_path = os.path.join(PATH, "background")

# Get all image files in the background directory
listBG = [pygame.image.load(os.path.join(background_path, filename)) 
          for filename in os.listdir(background_path) if filename.endswith(('.jpg', '.png', '.jpeg'))]

# Scale each image to the specified dimensions
for i in range(len(listBG)):
    listBG[i] = pygame.transform.scale(listBG[i], (S_WIDTH, S_HEIGHT))
    
#load music 
pygame.mixer.pre_init()
pygame.mixer.init()
clickSound = pygame.mixer.Sound('music/beep4.ogg')
getPointSound = pygame.mixer.Sound('music/beep1.ogg')
startScreenSound  = pygame.mixer.Sound('music/league-of-legends-original-sounds-welcome-to-summoners-rift.mp3')
listMusicBG = ['music/bg/snowmusic.mp3','music/bg/lunarmusic.mp3','music/bg/braum.mp3', 'music/bg/aatrox.mp3','music/bg/demaciamusic.mp3']

LIST_SFX = os.listdir(os.path.join(PATH, 'music/KillSFX'))


for i in range(len(LIST_SFX)):
    LIST_SFX[i] = pygame.mixer.Sound('music/KillSFX/' + LIST_SFX[i])

print("Initializing Pygame 1...")
    
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, LIVESFONT, LEVEL
    print("Initializing Pygame...")
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    print("Setting up display...")
    DISPLAYSURF = pygame.display.set_mode((S_WIDTH,S_HEIGHT))
    pygame.display.set_caption('Pykachu in League of Legends')
    BASICFONT = pygame.font.SysFont('comicsansms',70)
    LIVESFONT = pygame.font.SysFont('comicsanssms',45)
    
    
    print("Entering the game loop...")
    while True:
        random.shuffle(listBG)
        random.shuffle(listMusicBG)
        LEVEL = 1
        showStartScreen()
        while LEVEL <= MAXIMUM_LEVEL:
            print("while level is smaller than max ..." ,LEVEL)
            runGame()
            LEVEL += 1 
            pygame.time.wait(1000)
        showGameOverScreen()

    
def showStartScreen():
    startScreenSound.play()
    
    print("showStartScreen...")
    while True:
        DISPLAYSURF.blit(startBG,(0,0))
        newGameSurf = BASICFONT.render('NEW GAME',True, WHITE)
        newGameRect = newGameSurf.get_rect()
        newGameRect.center = (S_WIDTH//2,S_HEIGHT//2)
        DISPLAYSURF.blit(newGameSurf,newGameRect)
        pygame.draw.rect(DISPLAYSURF,WHITE, newGameRect,4)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mouseX, mouseY = event.pos
                if newGameRect.collidepoint((mouseX,mouseY)):
                    return
        
        pygame.display.update()
        FPSCLOCK.tick(TARGET_FPS)

def runGame():
    
    
    mainBoard = getRandomizeBoard()
    clickedBoxes = []
    firstSelection =None
    mouseX = 0
    mouseY = 0
    lastTimeGetPoint = time.time()
    hint = getHint(mainBoard)
    
    global GAMETIME, LEVEL, LIVES, TIMEBONUS, STARTTIME
    STARTTIME = time.time()
    TIMEBONUS = 0      
    randomBG = listBG[LEVEL - 1]
    randomMusicBG = listMusicBG[LEVEL - 1]
    pygame.mixer.music.load(randomMusicBG)
    pygame.mixer.music.play(-1,0.0)
    
    while True:
        mouseClicked = False
        
        DISPLAYSURF.blit(randomBG, (0,0))
        drawBoard(mainBoard)
        drawClickedBox(mainBoard,clickedBoxes)
        drawTimeBar()
        drawLives()
        
        if time.time()  - STARTTIME > GAME_TIME + TIMEBONUS:
            LEVEL = MAXIMUM_LEVEL + 1
            return
        if time.time() - lastTimeGetPoint >= SHOW_HINT_TIME:
            drawHint(hint)
            
        for event in pygame.event.get():
            if event.type ==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouseX, mouseY = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouseX, mouseY = event.pos  
                mouseClicked = True  
            if event.type == KEYUP:
                if event.key == K_n:
                    boxY1,boxX1 = hint[0][0], hint[0][1]
                    boxY2,boxX2 = hint[1][0], hint[1][1]
                    mainBoard[boxY1][boxX1] = 0
                    mainBoard[boxY2][boxX2] = 0
                    TIMEBONUS +=1
                    alterBoardWithLevevel(mainBoard,boxY1,boxX1,boxY2,boxX2, LEVEL) 
                    
                    if isGameComplete(mainBoard): 
                        drawBoard(mainBoard)
                        pygame.display.update ()
                        return
                    
                    if not ( mainBoard[boxY1][boxX1] != 0 and bfs(mainBoard,boxY1,boxX1,boxY2, boxX2)):
                        hint = getHint(mainBoard)
                        while not hint:
                            pygame.time.wait(100)
                            resetBoard(mainBoard)
                            LIVES += -1
                            if LIVES == 0:
                                LEVEL = MAXIMUM_LEVEL + 1 
                                return
                            
                            hint = getHint(mainBoard)
                            
        boxX, boxY = getBoxAtPixel(mouseX,mouseY)
        
        if boxX is not None and boxY is not None and mainBoard[boxY][boxX] != 0:
            drawHighlightBox(mainBoard,boxX,boxY)
      
        if boxX is not None and boxY is not None and mainBoard[boxY][boxX] != 0 and mouseClicked == True:
            
            clickedBoxes.append((boxX, boxY))
            drawClickedBox(mainBoard,clickedBoxes)
            mouseClicked = False
            
            if firstSelection == None:
                firstSelection = (boxX,boxY)
                clickSound.play()
            else:
                path  = bfs(mainBoard,firstSelection[1], firstSelection[0], boxY,boxX) 
                if path:
                    if random.randint(0,100) < 20:
                        soundObject = random.choice(LIST_SFX)
                        soundObject.play()
                    getPointSound.play()
                    mainBoard[firstSelection[1]][firstSelection[0]] = 0
                    mainBoard[boxY][boxX] = 0 
                    drawPath(mainBoard,path)
                    TIMEBONUS += 1
                    lastTimeGetPoint = time.time()
                    alterBoardWithLevevel(mainBoard, firstSelection[1],firstSelection[0],boxY,boxX,LEVEL)                    
                    
                    if isGameComplete(mainBoard):
                        drawBoard(mainBoard)
                        pygame.display.update()
                        return
                    
                    if not(mainBoard[hint[0][0]][hint[0][1]] != 0 and bfs(mainBoard, hint[0][0], hint[0][1], hint[1][0], hint[1][1])):
                        hint = getHint(mainBoard)
                        while not hint:
                            pygame.time.wait(500)
                            resetBoard(mainBoard)
                            LIVES += -1
                            if LIVES == 0:
                                LEVEL = MAXIMUM_LEVEL + 1
                                return

                            hint = getHint(mainBoard)
                else:
                    clickSound.play()

                clickedBoxes = []
                firstSelection = None

        pygame.display.update()
        FPSCLOCK.tick(TARGET_FPS)
    pygame.mixer.music.stop()
def getRandomizeBoard():
    # Create a list of icons based on the number of champions
    list_icons = list(range(1, len(CHAMPS_DICT) + 1))
    
    # Shuffle the icons to randomize their order
    random.shuffle(list_icons)

    # Create pairs and shuffle again
    list_icons = list_icons[:NUMBER_PAIRS] * REPEAT_PAIR_MAXIMUM

    # Shuffle the list again
    random.shuffle(list_icons)

    # Initialize the board with zeros
    board = [[0 for _ in range(BOARD_WIDHT)] for _ in range(BOARD_HEIGHT)]

    k = 0 
    # Fill the board with randomized icons
    for i in range(1, BOARD_HEIGHT - 1):
        for j in range(1, BOARD_WIDHT - 1):
            board[i][j] = list_icons[k]
            k += 1
    return board

def leftTopCoordsOfBox(boxX, boxY):
     left = boxX * BOX_SIZE + XMARGIN
     top = boxY *BOX_SIZE + YMARGIN
     return left,top

def getBoxAtPixel(x, y):
    if x <= XMARGIN or x >= S_WIDTH - XMARGIN or y <= YMARGIN or y >= S_HEIGHT - YMARGIN:
        return None, None
    return (x - XMARGIN) // BOX_SIZE, (y - YMARGIN) // BOX_SIZE
 
def drawBoard(board):
    for boxx in range(BOARD_WIDHT):
        for boxy in range(BOARD_HEIGHT):
            champ_id = board[boxy][boxx]  # Get the champion ID from the board
            
            if champ_id != 0:  # If the box is not empty
                left, top = leftTopCoordsOfBox(boxx, boxy)  # Get the coordinates
                boxRect = pygame.Rect(left, top, BOX_SIZE, BOX_SIZE)  # Create a rectangle for blitting
                
                if champ_id in CHAMPS_DICT:  # Check if the champion ID is valid
                    DISPLAYSURF.blit(CHAMPS_DICT[champ_id], boxRect)  # Draw the champion
                else:
                    print(f"Warning: Invalid champion ID {champ_id} at position ({boxx}, {boxy}).")
            else:
                # Optionally draw a placeholder for empty boxes
                # Example: pygame.draw.rect(DISPLAYSURF, (200, 200, 200), boxRect)  # Draw a grey box for empty slots
                pass

def drawHighlightBox(board, boxX,boxY):
    left, top = leftTopCoordsOfBox(boxX,boxY) 
    pygame.draw.rect(DISPLAYSURF, HIGHTLIGTH_COLOR, (left - 2, top -2 ,
                                                       BOX_SIZE + 4,BOX_SIZE +4),2 ) 
    
def drawClickedBox(board, clickedBoxes):
    for boxX,boxY in clickedBoxes:
        left, top = leftTopCoordsOfBox(boxX,boxY)
        boxRect = pygame.Rect(left, top, BOX_SIZE, BOX_SIZE)
        image  = CHAMPS_DICT[board[boxY][boxX]].copy()
        
        
        image.fill((60,60,60), special_flags = pygame.BLEND_RGB_SUB)
        DISPLAYSURF.blit(image,boxRect)   
        
def bfs(board, boxy1, boxx1, boxy2, boxx2):
    def backtrace(parent, boxy1, boxx1, boxy2, boxx2):
        start = (boxy1, boxx1, 0, 'no_direction')
        end = 0
        for node in parent:
            if node[:2] == (boxy2, boxx2):
                end = node

        path = [end]
        while path[-1] != start:
            path.append(parent[path[-1]])
        path.reverse()

        for i in range(len(path)):
            path[i] = path[i][:2]
        return path

    if board[boxy1][boxx1] != board[boxy2][boxx2]:
        return []

    n = len(board)
    m = len(board[0])

    import collections
    q = collections.deque()
    q.append((boxy1, boxx1, 0, 'no_direction'))
    visited = set()
    visited.add((boxy1, boxx1, 0, 'no_direction'))
    parent = {}

    while len(q) > 0:
        r, c, num_turns, direction = q.popleft()
        if (r, c) != (boxy1, boxx1) and (r, c) == (boxy2, boxx2):
            return backtrace(parent, boxy1, boxx1, boxy2, boxx2)

        dict_directions = {(r + 1, c): 'down', 
                           (r - 1, c): 'up',
                           (r, c - 1): 'left',
                           (r, c + 1): 'right'}
        for neiborX, neiborY in dict_directions:
            next_direction = dict_directions[(neiborX, neiborY)]
            if 0 <= neiborX <= n - 1 and 0 <= neiborY <= m - 1 and (
                    board[neiborX][neiborY] == 0 or (neiborX, neiborY) == (boxy2, boxx2)):
                if direction == 'no_direction':
                    q.append((neiborX, neiborY, num_turns, next_direction))
                    visited.add((neiborX, neiborY, num_turns, next_direction))
                    parent[(neiborX, neiborY, num_turns, next_direction)] = (
                    r, c, num_turns, direction)
                elif direction == next_direction and (
                        neiborX, neiborY, num_turns, next_direction) not in visited:
                    q.append((neiborX, neiborY, num_turns, next_direction))
                    visited.add((neiborX, neiborY, num_turns, next_direction))
                    parent[(neiborX, neiborY, num_turns, next_direction)] = (
                    r, c, num_turns, direction)
                elif direction != next_direction and num_turns < 2 and (
                        neiborX, neiborY, num_turns + 1, next_direction) not in visited:
                    q.append((neiborX, neiborY, num_turns + 1, next_direction))
                    visited.add((neiborX, neiborY, num_turns + 1, next_direction))
                    parent[
                        (neiborX, neiborY, num_turns + 1, next_direction)] = (
                    r, c, num_turns, direction)
    return []
           

def getCenterPos(pos):
    left, top = leftTopCoordsOfBox(pos[1],pos[0])
    return tuple([left + BOX_SIZE//2, top + BOX_SIZE//2]) 
          
def drawPath(board, path):
    for i in range(len(path) - 1):
        startPos = getCenterPos(path[i])
        endPos = getCenterPos(path[i+1])
        pygame.draw.line(DISPLAYSURF, RED, startPos, endPos,4)
    pygame.display.update()
    pygame.time.wait(300)  

def drawTimeBar():
    progress =  1 - ((time.time() -STARTTIME - TIMEBONUS)/ GAME_TIME)
    
    pygame.draw.rect(DISPLAYSURF,borderColor, (bar_position, bar_size), 1)
    inner_pos = (bar_position[0] + 2 , bar_position[1] + 2)
    inner_size = (bar_size[0] -4 * progress,bar_size[1] -4)
    pygame.draw.rect(DISPLAYSURF,bar_color,(inner_pos,inner_size))

def showGameOverScreen():
    playAgainFont = pygame.font.Font('freesansbold.tft',50)
    playAgainSurf = playAgainFont.render('Play Again?', True, PURPLE)
    playAgainRect = playAgainSurf.get_rect()
    playAgainRect.center = (S_WIDTH//2,S_HEIGHT//2)
    pygame.draw.rect(DISPLAYSURF,PURPLE, playAgainRect,4)
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mouseX,mouseY = event.pos
                if playAgainRect.collidepoint((mouseX,mouseY)):
                     return

def getHint(board):
    boxPokesLocated =  defaultdict(list)

    hint = []
    for boxY in range (BOARD_HEIGHT):
        for boxX in range(BOARD_WIDHT):
            if board[boxY][boxX] != 0:
                boxPokesLocated[board[boxY][boxX]].append((boxY,boxX))
    for boxY in range(BOARD_HEIGHT):
        for  boxX in range(BOARD_WIDHT):
            if board[boxY][boxX] != 0:
                for ortherBox in boxPokesLocated[board[boxY][boxX]]:
                    if ortherBox != (boxY,boxX) and bfs(board,boxY,boxX,ortherBox[0], ortherBox[1]):
                            hint.append((boxY,boxX))
                            hint.append(ortherBox)
                            return hint        
    return []    

def drawHint(hint):
    for boxY,boxX in hint:
        left, top = leftTopCoordsOfBox(boxX,boxY)
        pygame.draw.rect(DISPLAYSURF,BLUE,(left,top,BOX_SIZE,BOX_SIZE),2)

def resetBoard(board):
    pokesOnBoard = []
    for boxY in range(BOARD_HEIGHT):
        for boxX in range (BOARD_WIDHT):
            if board[boxY][boxX] != 0:
                pokesOnBoard.append(board[boxY][boxX])
    referencedList = pokesOnBoard[:]
    while referencedList == pokesOnBoard:
        random.shuffle(pokesOnBoard)
    
    i = 0 
    for boxY in range(BOARD_HEIGHT):
        for boxX in range(BOARD_WIDHT):
            if(board[boxY][boxX]) != 0:
                board[boxY][boxX] = pokesOnBoard[i]
                i += 1
    return board

def isGameComplete(board):
    print("Checking game completion...")
    print("Board dimensions: {}x{}".format(len(board), len(board[0])))
    for boxY in range(len(board)):  # Use dynamic length
        for boxX in range(len(board[0])):  # Use dynamic length
            print(f"Checking box ({boxY}, {boxX}): {board[boxY][boxX]}")
            if board[boxY][boxX] != 0:
                return False
    return True


def alterBoardWithLevevel(board, boxY1,boxX1, boxY2,boxX2,level):
        if level == 2:
            for boxX in (boxX1,boxX2):
                cur_list = [0]
                for i in  range(BOARD_HEIGHT):
                    if board[i][boxX] != 0:
                        cur_list.append(board[i][boxX])
                    while len(cur_list) < BOARD_HEIGHT:
                        cur_list.append(0)
                        
                    j = 0 
                    for num in cur_list:
                        board[j][boxX] = num
                        j += 1
                        
        if level == 3:
            for boxX in (boxX1,boxX2):
                cur_list = []
                for i in range(BOARD_HEIGHT):
                    if board[i][boxX] != 0:
                        cur_list.append(board[i][boxX])
                    cur_list.append(0)
                    cur_list = [0] * (BOARD_HEIGHT - len(cur_list)) +cur_list
                    
                    j = 0 
                    for num in cur_list:
                        board[j][boxX] = num
                        j += 1 
                    
                    
        if level == 4:
            for boxY in (boxY1, boxY2):
                cur_list = [0]
                for i in range(BOARD_WIDHT):
                    if board[boxY][i] != 0:
                        cur_list.append(board[boxY][i])
                while len(cur_list) < BOARD_WIDHT:
                    cur_list.append(0)
                    
                j = 0
                
                for num in cur_list:
                    board[boxY][j] = num
                    j += 1 
            
        if level == 5:
            for boxY in (boxY1,boxY2):
                cur_list = []
                for i in range(BOARD_WIDHT):
                    if board[boxY][i] !=0:
                        cur_list.append(board[boxY][i])
                cur_list.append(0)
                cur_list = [0] * (BOARD_WIDHT- len(cur_list)) + cur_list    
                
                j = 0 
                for num in cur_list: 
                    board[boxY][j] = num
                    j += 1
        
        return board    

def drawLives():
    logoRect =  pygame.Rect(10,10,BOX_SIZE,BOX_SIZE)
    DISPLAYSURF.blit(lollogo,logoRect)
    liveSurf = LIVESFONT.render(str(LIVES),True,WHITE)
    liveRect = liveSurf.get_rect()
    liveRect.topleft = (65,0)
    DISPLAYSURF.blit(liveSurf,liveRect)


if __name__ == "__main__":
    main()
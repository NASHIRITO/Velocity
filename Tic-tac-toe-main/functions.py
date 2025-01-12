import math
import time
import config as cfg

##> Start new game
def init_game(winner = "X"):
    cfg.turn = winner # Current turn (default: X starting)
    cfg.moves = 0 # Movments counter
    cfg.win = 0 # Current winner (0 - No winner yet, "X" - X Winner, "O" - O Winner)
    cfg.pinch = 0 # Pinch gesture Counter
    cfg.ttt_matrix=[[0,0,0], [0,0,0], [0,0,0]] # Board matrix (0 - Empty, 1 - X, 2 - O)


##> Check if there is a winner
def check_for_win():
    # Check moves in diagonal
    if (cfg.ttt_matrix[0][0] == cfg.ttt_matrix[1][1] == cfg.ttt_matrix[2][2]) & (cfg.ttt_matrix[2][2] != 0):
        return cfg.ttt_matrix[0][0] 
    
    # Check moves in anti-diagonal
    if (cfg.ttt_matrix[0][2] == cfg.ttt_matrix[1][1] == cfg.ttt_matrix[2][0]) & (cfg.ttt_matrix[2][0] != 0):
        return cfg.ttt_matrix[2][0]

    # Check moves in all columns
    for i in range (0, 3):
            if (cfg.ttt_matrix[i][0] == cfg.ttt_matrix[i][1] == cfg.ttt_matrix[i][2]) & (cfg.ttt_matrix[i][0] != 0):
                return cfg.ttt_matrix[i][0]

    # Check moves in all rows
    for i in range (0, 3):
        if (cfg.ttt_matrix[0][i] == cfg.ttt_matrix[1][i] == cfg.ttt_matrix[2][i]) & (cfg.ttt_matrix[0][i] != 0):
            return cfg.ttt_matrix[0][i]
    return 0


##> Change turn
def change_turn():
    if(cfg.turn == "X"):
        cfg.turn = "O"
    else:
        cfg.turn = "X"


##> Set a winner
def set_winner():
    cfg.win = cfg.turn
    cfg.score[cfg.win]+= 1


##> Update the variables values when making a move
def update_movment_values(x, y):
    if (cfg.ttt_matrix[x][y] == 0) : # Make sure this is a leagl move (place is empty)
        cfg.moves += 1 # Increment movments counter
        cfg.ttt_matrix[x][y] =  1 if cfg.turn == "X" else 2 # Set the currect move in matrix
        if(cfg.moves >= 5): # Check if there is a winner after 5 moves (minimum moves required for a win)
            if check_for_win():
                set_winner()
        change_turn() # Change turn
        if (cfg.moves == 9) & (check_for_win() == 0): # In case of draw
            init_game() # Restart game


##> Make a move
def makeMove(_x,_y, cv2):
    x, y = getPositionInMatrix(_x, _y, cv2) # Get the location to place the move
    update_movment_values(x, y) # Update movment values

    
##> Render the matrix
def renderMatrix(cv2, frame):
    for i in range(0,3):
        for j in range(0, 3):
            x, y = getMatrixCorByindex(i, j, cv2)
            if(cfg.ttt_matrix[i][j] == 1):
                drawX(x, y, cv2, frame)
            if(cfg.ttt_matrix[i][j] == 2):
                drawCircle(x, y, cv2, frame)


##> Draw O
def drawCircle(x, y, cv2, frame):
    cv2.circle(frame, (x,y), 50, cfg.o_color, 3)


##> Draw X
def drawX(x, y, cv2, frame):
    winRect = cv2.getWindowImageRect(cfg.winName)
    withoutMiddleX = x - int(winRect[2]/6)
    withoutMiddleY = y - int(winRect[3]/6)
    cv2.line(frame, (withoutMiddleX + 20, withoutMiddleY + 20), (withoutMiddleX+int(winRect[2]/3 -20), withoutMiddleY+int(winRect[3]/3) - 20), cfg.x_color, 3)
    cv2.line(frame, (withoutMiddleX+int(winRect[2]/3 - 20), withoutMiddleY + 20) , (withoutMiddleX + 20, withoutMiddleY+int(winRect[3]/3) - 20), cfg.x_color, 3)
    

##> Check if pinch gesture was made
def pinchAction(wrist, idx_fgr_mcp, idx_fgr_tip, tmb_tip):
    #Calculate if gesture was made with consider the distance from camera
    if math.dist(idx_fgr_tip, tmb_tip)/math.dist(wrist, idx_fgr_mcp) < 0.15:
        if time.time() >= (cfg.last_pinch+0.4): # 0.4 sec delay between gestures
            cfg.last_pinch = time.time()
            return True
    return False


##> Calculate Matrix coordinates
def getMatrixCorByindex(x, y, cv2):
    winRect = cv2.getWindowImageRect(cfg.winName)
    x_cor = (winRect[2]/6) + winRect[2]/3*(x)
    y_cor = (winRect[3]/6) + winRect[3]/3*(y)
    return int(x_cor), int(y_cor)


##> Calculate position in matrix by finger tip coordinates
def getPositionInMatrix(x, y, cv2):
    _x = _y = 0
    winRect = cv2.getWindowImageRect(cfg.winName)
    for index in range(0, 3):
        if(x <= winRect[2]/3*(index+1)):
            _x = index
            break
    for index in range(0, 3):
        if(y <= winRect[3]/3*(index+1)):
            _y = index
            break
    return _x, _y


##> Draw grid on screen
def drawGrid(cv2, frame):
    winRect = cv2.getWindowImageRect(cfg.winName)
    x1, y1 = int(winRect[2]/3), 0
    x2, y2 = int(winRect[2]/3), int(winRect[3])
    x3, y3 = 0 , int(winRect[3]/3)
    x4, y4 = int(winRect[2]), int(winRect[3]/3)
    cv2.line(frame, (x1, y1), (x2, y2), (0, 0,0), 1)
    cv2.line(frame, (x1*2, y1), (x2*2, y2), (0, 0,0), 1)
    cv2.line(frame, (x3, y3), (x4, y4), (0, 0,0), 1)
    cv2.line(frame, (x3, y3*2), (x4, y4*2), (0, 0,0), 1)


##> Print on screen
def print_on_screen(cv2, frame, text, position, size, color, backgroud=None):
    x, y = position
    text_h = 0
    if backgroud != None:
        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, size, 1)
        text_w, text_h = text_size
        cv2.rectangle(frame, position, (x + text_w, y + text_h), backgroud, -1)
    cv2.putText(frame, text, (x, y + text_h + size - 1), cv2.FONT_HERSHEY_DUPLEX, size, color, 1)
import cv2
import mediapipe as mp
import functions as fnc
import config as cfg


cv2.namedWindow(cfg.winName)
vc = cv2.VideoCapture(0)
mp_Hands = mp.solutions.hands
hands = mp_Hands.Hands()

if vc.isOpened():
    rval, frame = vc.read()
else:
    rval = False

while rval:
    frame = cv2.flip(frame, 1)
    winRect = cv2.getWindowImageRect(cfg.winName)
    RGB_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(RGB_image)
    multiLandMarks = results.multi_hand_landmarks
    if multiLandMarks:
        handList = []
        for handLms in multiLandMarks:
            for idx, lm in enumerate(handLms.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                handList.append((cx, cy))
        if(cfg.win == 0):
            if(fnc.pinchAction(handList[0], handList[5], handList[8], handList[4])):
                fnc.makeMove(handList[8][0], handList[8][1], cv2)
        else:
            if(fnc.pinchAction(handList[0], handList[5], handList[8], handList[4])):
                cfg.pinch+=1 
    if(cfg.win == 0):
        fnc.renderMatrix(cv2, frame)
        fnc.drawGrid(cv2, frame)
        fnc.print_on_screen(cv2, frame, "Turn "+ cfg.turn, (0, 0), 1, cfg.x_color if cfg.turn == "X" else cfg.o_color, (255,255,0))

    else:
        fnc.print_on_screen(cv2, frame, cfg.win + " is the winner!", (50, int(winRect[3]/2)), 2, (255, 0, 0))
        fnc.print_on_screen(cv2, frame, "Pinch "+str(2-cfg.pinch)+" times to restart.", (50, int(winRect[3]/2)+50), 1, (255, 255, 255), (0,0,0))
        if(cfg.pinch >= 2):
            fnc.init_game(cfg.win)
    fnc.print_on_screen(cv2, frame, "Score:", (winRect[2]-100, 0), 1, (255,255,255), (0,0,0))
    fnc.print_on_screen(cv2, frame, "X - "+str(cfg.score["X"]), (winRect[2]-100, 25), 1, cfg.x_color, (0,0,0))
    fnc.print_on_screen(cv2, frame, "O - "+str(cfg.score["O"]), (winRect[2]-100, 45), 1, cfg.o_color, (0,0,0))
    fnc.print_on_screen(cv2, frame, "", (winRect[2]-175, winRect[3]-25), 1, (72,73,213), (0,0,0))
    cv2.imshow(cfg.winName, frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27:
        break
vc.release()
cv2.destroyWindow(cfg.winName)
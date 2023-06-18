import cv2 as cv
import numpy as np
import copy
from VisionConstants import *
import time
##################################
#funkcje odpowiedzialne za ruch plotera
import serial
# Ustawienia połączenia szeregowego
serial_port = 'COM11'
baud_rate = 115200

# Funkcja przesuwająca głowicę
def move_to(x, y,feed_rate):
    cmd = f'G1 X{x} Y{y} F{feed_rate}\n'
    ser.write(cmd.encode('utf-8'))
    response = ser.readline().decode('utf-8')
    print(f'{cmd.strip()} - {response.strip()}')

# Funkcja do rotacji serva używahj wartości między 30(bezpieczna pozycja w górze) a 60 
def rotate(a):
    cmd = f'M03 S{a}\n'
    ser.write(cmd.encode('utf-8'))
    response = ser.readline().decode('utf-8')
    print(f'{cmd.strip()} - {response.strip()}')
# funckja ustalająca gdzie  jest pozycja dom 
def set_home():
    cmd = f'G28 X0 Y0\n'
    ser.write(cmd.encode('utf-8'))
    response = ser.readline().decode('utf-8')
    print(f'{cmd.strip()} - {response.strip()}')
# funckja powrtou do domu 
def go_home():
    cmd = f'G28\n'
    ser.write(cmd.encode('utf-8'))
    response = ser.readline().decode('utf-8')
    print(f'{cmd.strip()} - {response.strip()}')
#funkcja do rysowania planszy

def make_board():

    set_home()
    rotate(25)
    move_to(105,18.50,1000)
    rotate(60)
    move_to(285,18.50,1000)
    move_to(285,198.50,1000)
    move_to(105,198.50,1000)
    move_to(105,18.50,1000)
    rotate(25)
    move_to(165,18.50,1000)
    rotate(60)
    move_to(165,198.5,1000)
    move_to(225,198.5,1000)
    move_to(225,18.5,1000)
    rotate(25)
    move_to(285,78.5,1000)
    rotate(60)
    move_to(105,78.5,1000)
    move_to(105,138.5,1000)
    move_to(285,138.5,1000)
    rotate(25)
    move_to(10,0,1000)
    go_home()


def make_x(i,j):
    
    set_home()
    rotate(25)
    if i == 0 and j == 0:
        move_to(115,188.50,1000)
        rotate(60)
        move_to(155,148.50,1000)
        rotate(25)
        move_to(155,188.50,1000)
        rotate(60)
        move_to(115,148.50,1000)
        rotate(25)
        go_home()
    elif i == 0 and j == 1:
        move_to(175,148.50,1000)
        rotate(60)
        move_to(215,188.50,1000)
        rotate(25)
        move_to(215,148.50,1000)
        rotate(60)
        move_to(175,188.50,1000)
        rotate(25)
        go_home()
    elif i == 0 and j == 2:
        move_to(235,148.50,1000)
        rotate(60)
        move_to(275,188.50,1000)
        rotate(25)
        move_to(275,148.50,1000)
        rotate(60)
        move_to(235,188.50,1000)
        rotate(25)
        go_home()
    elif i == 1 and j == 0:
        move_to(115,128.50,1000)
        rotate(60)
        move_to(155,88.50,1000)
        rotate(25)
        move_to(155,128.50,1000)
        rotate(60)
        move_to(115,88.50,1000)
        rotate(25)
        go_home()
    elif i == 1 and j == 1:
        move_to(175,88.50,1000)
        rotate(60)
        move_to(215,128.50,1000)
        rotate(25)
        move_to(175,128.50,1000)
        rotate(60)
        move_to(215,88.50,1000)
        rotate(25)
        go_home()
    elif i == 1 and j == 2:
        move_to(235,88.50,1000)
        rotate(60)
        move_to(275,128.50,1000)
        rotate(25)
        move_to(235,128.50,1000)
        rotate(60)
        move_to(275,88.50,1000)
        rotate(25)
        go_home()
    elif i == 2 and j == 0:
        move_to(115,28.50,1000)
        rotate(60)
        move_to(155,68.50,1000)
        rotate(25)
        move_to(115,68.50,1000)
        rotate(60)
        move_to(155,28.50,1000)
        rotate(25)
        go_home()
    elif i == 2 and j == 1:
        move_to(175,28.50,1000)
        rotate(60)
        move_to(215,68.50,1000)
        rotate(25)
        move_to(175,68.50,1000)
        rotate(60)
        move_to(215,28.50,1000)
        rotate(25)
        go_home()
    elif i == 2 and j == 2:
        move_to(235,28.50,1000)
        rotate(60)
        move_to(275,68.50,1000)
        rotate(25)
        move_to(235,68.50,1000)
        rotate(60)
        move_to(275,28.50,1000)
        rotate(25)
        go_home()
        



##################################
capture=cv.VideoCapture(0)
board = np.zeros((BOARD_ROWS, BOARD_COLS), dtype=int)


def mark_field(row,col,player):
    if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
        if board[row][col] == 0:
            board[row][col] = player
            return True
    return False

def avaiable_field(row,col):
     if board[row][col] == 0:
        return True
     else:
        return False
def is_boardFull():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True 

def get_empty_positions(board):
    empty_positions = []
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            if board[i][j] == 0:
                empty_positions.append((i, j))
    return empty_positions     

def check_win(board,player):
    for col in range (BOARD_COLS):
        #vertical
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True
        #horizontal
    for row in range (BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True
        
        #desc diagonal wins
    if board[0][0] == board[1][1] == board[2][2] == player:
          return True
    
        #asc diagonal wins
    if board[2][0] == board[1][1] == board[0][2] == player:
          return True
    
    return False
    
def minimax(board,  isMaximizing):
    empty_sqrs = get_empty_positions(board)

    if check_win(board,1):  # Jeżeli wygrał człowiek
        return -10, None
    if check_win(board,2):  # Jeżeli wygrało AI
        return 10, None
    if not empty_sqrs:  # Jeżeli remis
        return 0, None
    
    
    if isMaximizing:  # Jeżeli to kolej AI
        best_score = -100
        best_move = None
        for (row, col) in empty_sqrs:
            temp_board = copy.deepcopy(board)
            temp_board[row][col] = 2  # AI wykonuje ruch
            score = minimax(temp_board, False)[0]  # Wywołanie funkcji dla przeciwnika
            if score > best_score:
                best_score = score
                best_move = (row, col)
        return best_score, best_move
    
    elif not isMaximizing:
        best_score = 100
        best_move = None
        for (row, col) in empty_sqrs:
            temp_board = copy.deepcopy(board)
            temp_board[row][col] = 1  # AI wykonuje ruch
            score = minimax(temp_board, True)[0]  # Wywołanie funkcji dla przeciwnika
            if score < best_score:
                best_score = score
                best_move = (row, col)
        return best_score, best_move
    

def is_thereaCrircle():
    #wykrywanie okręgów
    kolka = cv.HoughCircles(edges, cv.HOUGH_GRADIENT,1, 40, param1=70, param2=20, minRadius=28, maxRadius=55) 
    if kolka is not None:
        # Konwersja współrzędnych okręgu z (x, y, r) na (cx, cy)
        kolka = np.round(kolka[0, :]).astype("int")
        for (x, y, r) in kolka:
            # Sprawdzanie, w którym polu znajduje się środek okręgu
            rows, cols = edges.shape
            row_step = rows // 3
            col_step = cols // 3
            field_row = y // row_step
            field_col = x // col_step

            # Zabezpieczenie przed wykryciem okręgu poza planszą
            if field_row < BOARD_ROWS and field_col < BOARD_COLS:
                mark_field(field_row, field_col, 1)
        return field_row, field_col
        
def draw_figure(row, col):
    cell_width = 450 // BOARD_COLS  # Width of each cell on the board
    cell_height = 450 // BOARD_ROWS  # Height of each cell on the board
    margin = 30  # Smaller margin inside each cell

    # Oblicz środek pola
    center_x = col * cell_width + cell_width // 2
    center_y = row * cell_height + cell_height // 2

    # Rysuj "X"
    start_x = center_x - cell_width // 2 + margin
    end_x = center_x + cell_width // 2 - margin
    start_y = center_y - cell_height // 2 + margin
    end_y = center_y + cell_height // 2 - margin

    # Rysuj dwie linie składające się na "X"
    cv.line(plansza, (start_x, start_y), (end_x, end_y), CROSS_COLOR, CROSS_WIDTH)
    cv.line(plansza, (end_x, start_y), (start_x, end_y), CROSS_COLOR, CROSS_WIDTH)




player = 1
current_count = 0
prev_count = 0
game_over = False
ser = serial.Serial(serial_port, baud_rate)
make_board()
time.sleep(20)
while True:
    
    
    ret, frame = capture.read() 

    #wyznaczanie pola działania i konwersja na widzenie krawedziwoe za pomoca algorytmu Canny    
    plansza = frame[10:460 , 110:570]
    grey = cv.cvtColor(plansza, cv.COLOR_BGR2GRAY)
    blur = cv.medianBlur(grey, 5)
    edges = cv.Canny(blur,100,200)    
    #wykrywanie okręgów

        
    if player == 1:
        
        if is_thereaCrircle():
            field_row , field_col = is_thereaCrircle()
            #print(field_row,field_col)
            #mark_field(field_row, field_col, 1)
            current_count = np.count_nonzero(board == 1)
            if current_count == prev_count + 1:
                 prev_count = current_count
                 print("Liczba jedynek:" , prev_count)
                 print(player)
                 if check_win(board,player):
                     print(player , " Wygral")
                     game_over=True
                     
                     
                 player = 2
            else:
                continue 
    elif player == 2:
       
            _ , best_move= minimax(board,True)
            if best_move is not None:
                i , j = best_move
                if mark_field(i , j , player):
                    #print(i,j)
                    draw_figure(i , j)
                    capture.release()
                    make_x(i , j)
                    time.sleep(15)
                    capture=cv.VideoCapture(0)
            
                    if check_win(board , player):
                        print(player , "Wygrał")
                        game_over = True
                
                    player = 1
                    

    cv.imshow("obraz", frame)
    cv.imshow("ROI", plansza)
    print(board)

    key=cv.waitKey(27)
    if key == 27:
        break

capture.release()
cv.destroyAllWindows()
ser.close()
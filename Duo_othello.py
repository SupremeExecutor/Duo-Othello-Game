
import sys
import time
import copy
import numpy
import random

#Definition/定义棋盘：
SIZE_OF_BOARD = 12 #Size of the board/棋盘大小 12x12

BLACK = 1 
WHITE = -1
EMPTY = 0

#Dictionary for Conversion/转换字典
num_to_word = {
    0:"a",
    1:"b",
    2:"c",
    3:"d",
    4:"e",
    5:"f",
    6:"g",
    7:"h",
    8:"i",
    9:"j",
    10:"k",
    11:"l"
    }
word_to_num = {v : k for k,v in num_to_word.items()}

#Globalization/全局变量
global weight_board

# Initialization/初始化棋盘(12X12 八个预设子) 
def initialize_board():
    board = [[EMPTY] * SIZE_OF_BOARD for _ in range(SIZE_OF_BOARD)]
    player_type = ""
    time = 0
    f = open("input.txt") #Need input.txt/需要预设input(通过修改input可以方便实现多种棋盘大小与初始局面)
    # player_type = f.readline()
    # player_type = ''.join(player_type.split('\n')) #！！！读取txt会带有换行符!!!
    # time = str(f.readline()).split()
    # if player_type == "X":
    #     time = time[1]
    # else:
    #     time = time[0]
    for i in range(SIZE_OF_BOARD):
        line = f.readline()
        for j in range(SIZE_OF_BOARD):
            if line[j] == '.':
                board[i][j] = EMPTY
            elif line[j] == 'X':
                board[i][j] = BLACK
            elif line[j] == 'O':
                board[i][j] = WHITE
    
    return player_type, time, board #Only board return/只使用board（如果有其他需要可以修改）

#Initialization of weight board/权重棋盘
def initialize_weight_board():
    try:
        board = [[EMPTY] * SIZE_OF_BOARD for _ in range(SIZE_OF_BOARD)]
        f = open("weight.txt","r")
        for x in range(SIZE_OF_BOARD):
            line = f.readline()
            line = list(line.split(" "))
            for y in range(SIZE_OF_BOARD):
                board[x][y] = int(line[y])
        f.close()
        return board
    except:                 
        board = [[100,-8,10,8,6,6,6,6,8,10,-8,100], #Weight board/棋盘权重（可以自定义）
                 [-8,-24,-4,-3,-3,-3,-3,-3,-3,-4,-24,-8],
                 [10,-4,1,1,4,3,3,3,4,7,-4,10],
                 [8,-3,1,1,4,3,3,3,3,4,-3,8],
                 [6,-3,4,4,7,3,1,1,3,3,-3,6],
                 [6,-3,3,3,3,3,3,3,3,3,-3,6],
                 [6,-3,3,3,3,3,3,3,3,3,-3,6],
                 [6,-3,3,3,3,3,3,7,4,4,-3,6],
                 [8,-3,4,3,3,3,3,4,1,1,-3,8],
                 [10,-4,7,4,3,3,3,4,1,1,-4,10],
                 [-8,-24,-4,-3,-3,-3,-3,-3,-3,-4,-24,-8],
                 [100,-8,10,8,6,6,6,6,8,10,-8,100]]              

        f = open("weight.txt","w", encoding="utf-8")
        for x in range(SIZE_OF_BOARD):
            for y in range(SIZE_OF_BOARD):
                f.write(str(board[x][y])+" ")
            f.write("\n")
        f.close()

        return board

#Print board/打印棋盘
def board_print(board):
    print("\nPrint board/打印棋盘:")
    for i in range(SIZE_OF_BOARD):
        if i == 0:
            print("  ", end="")
            for k in range(SIZE_OF_BOARD):
                print(num_to_word[k], end=" ")
            print("\n")
        for j in range(SIZE_OF_BOARD):
            if j == 0:
                print(i+1, end=" ")

            if board[i][j] == 0:
                print(".", end=" ")
            elif board[i][j] == 1:
                print("X", end=" ")
            else:
                print("O", end=" ")
        print("\n")

def board_file_print(board):

    file = open("Finalboard.txt","w", encoding="utf-8")
    file.write("Print board/打印棋盘:\n")
    for i in range(SIZE_OF_BOARD):
        for j in range(SIZE_OF_BOARD):
            if board[i][j] == 0:
                file.write(".")
            elif board[i][j] == 1:
                file.write("X")
            else:
                file.write("O")
        file.write("\n")
    file.close()

#Operation for gaming/操作
        
def in_board(x, y): #位置是否在棋盘内
    return 0<= x < SIZE_OF_BOARD and 0 <= y < SIZE_OF_BOARD

def is_empty(board, x, y): #位置是否为空
    return board[x][y] == EMPTY

def black_or_white(board, x, y, color): #位置是否为某一颜色旗子
    return in_board(x, y) and board[x][y] == color

def is_rival(board, x, y, color): #是否是对手的棋子
    return in_board(x, y) and board[x][y] != EMPTY and board[x][y] != color #不是自己的就是对面的

def search_valid_move(board, x, y, color): #Return boolean valid and coordinate list/返回值：是否有valid值；有效移动的坐标列表
    if not is_empty(board, x, y): #If coordinate is EMPTY, then return/坐标不为空就没法放置
        return False, []

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    valid = False
    move_targets = []

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        temp = []

        while is_rival(board, new_x, new_y, color):
            temp.append((new_x, new_y))
            new_x += dx
            new_y += dy
            if black_or_white(board, new_x, new_y, color):
                valid = True
                move_targets.extend(temp)
                break
        
    return valid, move_targets

def make_move(board, x, y, color, move_targets): #Place the piece/执行落子
    board[x][y] = color
    for nx, ny in move_targets:
        board[nx][ny] = color

def undo_move(board, x, y, move_targets): #Undo the place/执行撤销
    board[x][y] = EMPTY
    for nx, ny in move_targets:
        board[nx][ny] = 3 - board[nx][ny]

#Evaluate the board/评估当前棋盘上自己与对手的棋子数量
#    Base score (player +1/ rival -1) 基础子数差
#    weight score (Each position of the board has its score) 权重
#    stable score (Whether the piece can be flipped by the counterplayer) 稳定子
#    mobility (evaluate valid locations that can place the piece) 移动力
#

def eval_func(board, color): 
    base_score = 0
    weight_score = 0
    stable_score = 0
    mobility = 0
    stable_weight = 2 #Unit score for each stable piece/稳定子分数
    mymove = []
    rivalmove = []
    
    new_map = numpy.array(board)
    Vmap = numpy.array(weight_board)

    count = sum(sum(abs(new_map)))*color
    base_score = sum(sum(new_map))*color
    weight_score = sum(sum(new_map*Vmap))*color
    
    for x in range(SIZE_OF_BOARD):
        for y in range(SIZE_OF_BOARD):
            # if board[x][y] == color and ai_color == BLACK: #是自己+1分
            #     if is_stable(board, x, y, color):
            #         stable_score += stable_weight #* weight_board[x][y]
            # elif board[x][y] == -color and ai_color == BLACK: #是对手-1分
            #     if is_stable(board, x, y, -color):
            #         stable_score -= stable_weight #* weight_board[x][y]
            # else:
                if board[x][y] == EMPTY:
                    newBoard = board.copy()
                    valid,_ = search_valid_move(newBoard, x, y, color)
                    if valid:
                        mymove.append((x, y))
                    valid,_ = search_valid_move(newBoard, x, y, -color)
                    if valid:
                        rivalmove.append((x, y))  
    
    if len(mymove)+len(rivalmove) == 0:
        mobility = 0
    else:
        mobility = ((len(mymove)-len(rivalmove))/(len(mymove)+len(rivalmove)))*100
     
    
    if count <= 120 and base_score <= 0 and len(mymove) == 0 and len(rivalmove) == 0:
        mixed_score = float("-inf")
        return mixed_score
                        
                        
    if ai_color == WHITE:
        mixed_score = 5*100 * (base_score/count) + 0.5*100*(weight_score/count) + 0.5*mobility    
    else:
        if count <= 72:
            mixed_score = base_score + weight_score + 5*stable_score + 15*(len(mymove)-len(rivalmove))
        else:
            mixed_score = 5*base_score + weight_score + 10*stable_score + 5*(len(mymove)-len(rivalmove))

    return mixed_score

def is_stable(board, x, y, player): #Check if the piece is stable/是否为稳定子
    directions = ((0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1))   
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        while 0 <= nx < SIZE_OF_BOARD and 0 <= ny < SIZE_OF_BOARD and board[nx][ny] == player:
            nx += dx
            ny += dy
        if 0 <= nx < SIZE_OF_BOARD and 0 <= ny < SIZE_OF_BOARD and board[nx][ny] == EMPTY:
            return False
    return True

def board_status(board): #Count total pieces/计算棋盘全局棋子数
    new_map = numpy.array(board)
    count = sum(sum(abs(new_map)))
    return count

def minimax(board, depth, maximizing_player, alpha, beta, color, maxdepth): # Minimax with alpha-beta prune/加入剪枝的 Minimax
    if depth == 0:
        return eval_func(board, color), None
    
    valid_moves = []
    if maximizing_player == True:
        for i in range(SIZE_OF_BOARD):
            for j in range(SIZE_OF_BOARD):
                valid, _ = search_valid_move(board, i, j, color)
                if valid:
                    valid_moves.append((i, j))
    else:
        for i in range(SIZE_OF_BOARD):
            for j in range(SIZE_OF_BOARD):
                valid, _ = search_valid_move(board, i, j, -color)
                if valid:
                    valid_moves.append((i, j))        

    if not valid_moves:
        return eval_func(board, color), None
    
    # If we could place at the corner, then do it!/抢占四个角
    if depth == maxdepth:
        for i in range(len(valid_moves)):
            if weight_board[valid_moves[i][0]][valid_moves[i][1]] == weight_board[0][0] and maximizing_player:
                move = [valid_moves[i]]
                return 1000, move
            
    ##Preseach operation(if needed)/ 预搜索前maxN个最优操作(如果深度太高，运行太慢，则使用预搜索)
            
    # if depth >= 4:
    #     Vmoves = []
    #     for move in valid_moves:
    #         x, y = move
    #         new_board = copy.deepcopy(board)
    #         _, moves = search_valid_move(new_board, x, y, color)
    #         make_move(new_board, x, y, color, moves)
    #         value, _ = minimax(new_board, 1, not maximizing_player, float('-inf'), float("inf"), color, maxdepth)
    #         Vmoves.append(value)
    #     ind = numpy.argsort(Vmoves)
    #     maxN = 6
    #     valid_moves = [valid_moves[i] for i in ind[0:maxN]]
        
    if maximizing_player: #Maximize ourselves/是自己则最大化评估
        max_eval = float('-inf')
        best_move = []

        for move in valid_moves:
            x, y = move
            new_board = copy.deepcopy(board)
            _, moves = search_valid_move(new_board, x, y, color)
            make_move(new_board, x, y, color, moves)
            eval_num, _= minimax(new_board, depth - 1, False, alpha, beta, color, maxdepth)
            undo_move(new_board, x, y, moves)

            if eval_num >= max_eval: 
                if eval_num > max_eval:
                    max_eval = eval_num
                    best_move = []
                    best_move.append(move)
                else:
                    best_move.append(move)                    
            
            alpha = max(alpha, eval_num)
            if beta <= alpha: #Prune/剪枝
                break

        return max_eval, best_move
    
    else: #Minimize enemy/是对方则最小化评估

        min_eval = float("inf")
        best_move = []

        for move in valid_moves:
            x, y = move
            new_board = copy.deepcopy(board)
            _, moves = search_valid_move(new_board, x, y, -color)
            make_move(new_board, x, y, -color, moves)
            eval_num, _= minimax(new_board, depth - 1, True, alpha, beta, color, maxdepth)
            undo_move(new_board, x, y, moves)

            if eval_num <= min_eval:
                if eval_num < min_eval:
                    min_eval = eval_num
                    best_move = []
                    best_move.append(move)
                else:
                    best_move.append(move)  
            
            beta = min(beta, eval_num)
            if beta <= alpha: #Prune/剪枝
                break

        return min_eval, best_move 
    

def ai_decision(board, color): #Set AI player/设置ai棋手
    depth = 4
    _, move = minimax(board, depth, True, float('-inf'), float('inf'), color, depth)
    if len(move) == 1:
        return move[0]
    else:
        n = len(move)
        return move[random.randint(0,n-1)]

def player_decision(board, valid_moves): #Player function/设置玩家操作
    while True:
        board_print(board)
        print("Please choose the location to place/请玩家选择落子位置如下：", end="")
        valid_moves = sorted(valid_moves, key = lambda x: x[1])
        for v in valid_moves:
            print("(%s,%d)" %(num_to_word[v[1]],v[0]+1) , end="")
        while True:
            y = input("\nPlease enter column coordinate/请输入字母坐标 y (列):")
            x = input("Please enter row coordinate/请输入数字坐标 x (行):")
            if y.isalpha() and x.isdigit():
                break
            else:
                print("\nPlease enter again!/请重新输入!")
        move = tuple((int(x)-1, word_to_num[y]))
        if move not in valid_moves:
            print("\nInvalid location, please enter again!/错误, 非有效落子位置！请重新输入！\n")
            continue
        else:
            print("Successfully placed!/成功，玩家落子：(%c,%d)" %(num_to_word[move[1]], move[0]+1))
            return move
        
def progress_bar():
    print("\n")
    for i in range(1, 101):
        print("\r", end="")
        print("Initializing, please wait!/初始化中.....: {}%: ".format(i), "▋" * (i // 2), end="") #其实没什么用
        sys.stdout.flush()
        time.sleep(0.05)

def main():

    progress_bar()  
    global weight_board, ai_color
    _, _, board = initialize_board()
    weight_board = initialize_weight_board()
    
    print("\n\nGame start!/黑白棋游戏开始！\n")

    while True: #First or second/请选择先手后手 (1:BLACK,2:WHITE,3:AI vs AI)
        player_color = input("Please choose your color/请玩家选择自己的颜色(BLACK:1;WHITE:2;AutoGame:3):")

        if player_color.isdigit():
            player_color = int(player_color)
            if player_color != BLACK and player_color != WHITE+3 and player_color != 3:
                print("Invalid choice!Please choose again!/棋子颜色选择错误！请重试！")
                continue
            else:
                if player_color == BLACK:
                    print("\nPlayer: BLACK/人类玩家: 黑棋")
                else:
                    if player_color == WHITE+3:
                        player_color = WHITE
                        print("\nPlayer: WHITE/人类玩家: 白棋")
                    print("\nAutoplay On!/开启自动局\n")
                break

        else:
            print("Invalid choice!Please choose again!/棋子颜色选择错误！请重试！")
            continue           

    current_color = BLACK #BLACK FIRST/设置黑棋先手
    last_valid_moves = []
    if player_color == BLACK:
        ai_color = WHITE
    else:
        ai_color = BLACK
    if player_color == WHITE:
        print("AI Player: BLACK/设置AI玩家: 黑棋\n")
    
    elif player_color == BLACK:
        print("AI Player: WHITE/设置AI玩家: 白棋\n")
    else:
        print("AI Player: BLACK/设置AI玩家: 黑棋\n")       
        print("AI Player: WHITE/设置AI玩家: 白棋\n")

    while True:
        valid_moves = []
        for i in range(SIZE_OF_BOARD):
            for j in range(SIZE_OF_BOARD):
                valid, _ = search_valid_move(board, i, j, current_color)
                if valid:
                    valid_moves.append((i, j))        
        
        if not valid_moves:
            if not last_valid_moves: #If neither player has valid moves, then game over/如果两人都没有落子的地方比赛结束
                break 
            else:
                last_valid_moves = valid_moves #Record the decision of the last move/记录上一个选手的有效棋位
                current_color = -current_color
                continue    

        if current_color == BLACK:
            print("\nTurn BLACK.../黑方思考中...")
            if player_color == BLACK:
                move = player_decision(board, valid_moves)
            else:
                move = ai_decision(board, current_color)
                if move is None:  # 检查move是否为None
                    print("CANNOT FIND VALID MOVE, SKIP!/无法找到有效的移动！")
                    current_color = -current_color
                    continue
                print("BLACK MOVE/黑方落子:(%c,%d)" %(num_to_word[move[1]], move[0]+1))         

        else:
            print("\nTurn WHITE.../白方思考中...")
            if player_color == WHITE:
                move = player_decision(board, valid_moves)
            else:
                move = ai_decision(board, current_color)
                if move is None:  # 检查move是否为None
                    print("CANNOT FIND VALID MOVE, SKIP!/无法找到有效的移动！")
                    current_color = -current_color
                    continue
                print("WHITE MOVE/白方落子:(%c,%d)" %(num_to_word[move[1]], move[0]+1))
        
        x, y = move
        _, moves = search_valid_move(board, x, y, current_color)
        make_move(board, x, y, current_color, moves)
        
        current_color = -current_color        

    # 输出最终结果
    black_score = sum(row.count(BLACK) for row in board)
    white_score = sum(row.count(WHITE) for row in board)
    print("\nBlack scores/黑方得分:", black_score)
    print("White scores/白方得分:", white_score)
    if black_score > white_score:
        print("\n#Congratulation, BLACK WIN!/黑方胜利!")     
        if player_color == BLACK:
            print("#Winner is the Human player!/人类玩家获胜!")   
        else:
            print("#Winner is the ai player!/AI获胜!")              
    elif black_score < white_score:
        print("\n#Congratulation, WHITE WIN!/白方胜利!")
        if player_color == WHITE:
            print("#Winner is the Human player!/人类玩家获胜!")   
        else:
            print("#Winner is the ai player!/AI获胜!")   
    else:
        print("#DRAW!/平局!")

    board_print(board)
    board_file_print(board)
    print("#Final status has been saved!/终局已保存!")    

if __name__ == "__main__":
    main()



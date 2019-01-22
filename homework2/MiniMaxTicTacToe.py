from math import inf as infinity

# game board
initial_board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
humanPlayer = "O"
AIPlayer = "X"


# printing the board
def print_board(board):
    print("  " + board[0] + "  |  " + board[1] + "  |   " + board[2] + " ")
    print("---------------")
    print("  " + board[3] + "  |  " + board[4] + "  |   " + board[5] + " ")
    print("---------------")
    print("  " + board[6] + "  |  " + board[7] + "  |   " + board[8] + " ")


def determine_win(ch):
    if ch == "O":
        return -1
    elif ch == "X":
        return 1


def utility(state):
    if state[0] == state[1] and state[1] == state[2] and state[2] != " ":
        return determine_win(state[0])
    elif state[3] == state[4] and state[5] == state[4] and state[4] != " ":
        return determine_win(state[3])
    elif state[6] == state[7] and state[7] == state[8] and state[8] != " ":
        return determine_win(state[6])
    elif state[0] == state[3] and state[3] == state[6] and state[6] != " ":
        return determine_win(state[3])
    elif state[1] == state[4] and state[7] == state[4] and state[4] != " ":
        return determine_win(state[1])
    elif state[2] == state[5] and state[5] == state[8] and state[8] != " ":
        return determine_win(state[2])
    elif state[0] == state[4] and state[4] == state[8] and state[8] != " ":
        return determine_win(state[0])
    elif state[2] == state[4] and state[6] == state[4] and state[6] != " ":
        return determine_win(state[2])
    elif " " in state:
        return None
    else:
        return 0;


def available_moves(state):
    moves = []
    for i in range(len(state)):
        if state[i] == " ":
            moves.append(i)
    return moves


def minmax(state,depth,player):
    #print(depth)
    #print(player)
    #print(state)
    if player == AIPlayer:
        fpos = [-1,-infinity]
    else:
        fpos = [+1,+infinity]
        
    cur_utility = utility(state)
    if depth == 0 or cur_utility in (1, -1, 0):
        return[-1, cur_utility]
    
    next_player = humanPlayer if player == AIPlayer else AIPlayer
    
    for available_pos in available_moves(state):
        state[available_pos] = player
        probable_score = minmax(state,depth-1,next_player)
        state[available_pos] = " "
        probable_score[0] = available_pos
        
        if player == AIPlayer:
            if probable_score[1] > fpos[1]:
                fpos = probable_score
        else:
            if probable_score[1] < fpos[1]:
                fpos = probable_score
    
    return fpos




print(utility(["O","O","X","X"," ","O"," "," ","X"]))
print(utility([" ", " ", " ", " ", " ", " ", " ", " ", " "]))
print(utility(["O", "X", "O", "X", "X", "0", "X", "O", "X"]))
board1 = ["O","O","X","X"," ","O"," "," ","X"]
print(minmax(initial_board,9,AIPlayer))
print_board(initial_board)
print(minmax(board1,4,AIPlayer))
print_board(board1)


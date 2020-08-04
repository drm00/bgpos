#!/usr/bin/env python3

import pprint
# gnubg position id has 14 characters
# extreme gammon position id has 51 characters (?)

XGID = '-a-B--E-B-a-dDB--b-bcb----:1:1:-1:63:0:0:0:3:8'
XGID = '-b--B-C-CA-AdC-a-c-e-A--A-:3:-1:1:62:0:0:3:0:10'

# board consists of 11•18 cells
board = [
    [' ', '\u00F1', '\u00A1', '\u00B2', '\u00B1', '\u00B2', '\u00A2', '\u00F2'],
    [' ', '\u00F0', 'F', 'A', 'F', 'A', 'F', 'A', '\u0040', ' ', '\u0040', 'F', 'A', 'F', 'A', 'F', 'A', '\u00F0'],
    [' ', '\u00F0', 'G', 'B', 'G', 'B', 'G', 'B', '\u0040', ' ', '\u0040', 'G', 'B', 'G', 'B', 'G', 'B', '\u00F0'],
    [' ', '\u00F0', 'H', 'C', 'H', 'C', 'H', 'C', '\u0040', ' ', '\u0040', 'H', 'C', 'H', 'C', 'H', 'C', '\u00F0'],
    [' ', '\u00F0', 'I', 'D', 'I', 'D', 'I', 'D', '\u0040', ' ', '\u0040', 'I', 'D', 'I', 'D', 'I', 'D', '\u00F0'],
    [' ', '\u00F0', 'J', 'E', 'J', 'E', 'J', 'E', '\u0040', ' ', '\u0040', 'J', 'E', 'J', 'E', 'J', 'E', '\u00F0'],
    [' ', '\u00F0', ' ', ' ', ' ', ' ', ' ', ' ', '\u0040', ' ', '\u0040', ' ', ' ', ' ', ' ', ' ', ' ', '\u00F0'],
    [' ', '\u00F0', 'e', 'j', 'e', 'j', 'e', 'j', '\u0040', ' ', '\u0040', 'e', 'j', 'e', 'j', 'e', 'j', '\u00F0'],
    [' ', '\u00F0', 'd', 'i', 'd', 'i', 'd', 'i', '\u0040', ' ', '\u0040', 'd', 'i', 'd', 'i', 'd', 'i', '\u00F0'],
    [' ', '\u00F0', 'c', 'h', 'c', 'h', 'c', 'h', '\u0040', ' ', '\u0040', 'c', 'h', 'c', 'h', 'c', 'h', '\u00F0'],
    [' ', '\u00F0', 'b', 'g', 'b', 'g', 'b', 'g', '\u0040', ' ', '\u0040', 'b', 'g', 'b', 'g', 'b', 'g', '\u00F0'],
    [' ', '\u00F0', 'a', 'f', 'a', 'f', 'a', 'f', '\u0040', ' ', '\u0040', 'a', 'f', 'a', 'f', 'a', 'f', '\u00F0'],
    [' ', '\u00F3', '\u00A3', '\u00B4', '\u00B3', '\u00B4', '\u00A4', '\u00F4'],
]

b = [''.join(s) for s in board]
pprint.pprint(b)

def XG_get_pipcount_for_point(c):
    if c == '-':
        return 0

    return ord(c.lower()) - 96

def set_pips(position, checkers, board):

    if position < 1 or position > 24:
        return False

    stack_height = XG_get_pipcount_for_point(checkers)

    if stack_height < 1 or stack_height > 15:
        return False

    if checkers == checkers.lower():
        player = 'white'
    else:
        player = 'black'

    indices = {
        0: (11, 9),
        1: (11, 16),
        2: (11, 15),
        3: (11, 14),
        4: (11, 13),
        5: (11, 12),
        6: (11, 11),
        7: (11, 7),
        8: (11, 6),
        9: (11, 5),
        10: (11, 4),
        11: (11, 3),
        12: (11, 2),
        13: (1, 2),
        14: (1, 3),
        15: (1, 4),
        16: (1, 5),
        17: (1, 6),
        18: (1, 7),
        19: (1, 11),
        20: (1, 12),
        21: (1, 13),
        22: (1, 14),
        23: (1, 15),
        24: (1, 16),
        25: (1, 9),
    }

    row = indices[position][0]
    col = indices[position][1]
    if row == 1:
        direction = 1
    else:
        direction = -1

    top_or_bottom = 32 if direction == -1 else 0

    for stack_elem in range(stack_height):

        if col != 9 and stack_elem >= 5:
            # choose approp. symbol and exit
            pass

        if col == 9:
            # checkers on the bar
            pass
        elif position % 2 == 0:
            # white points
            if player == 'black':
                board[row+(stack_elem*direction)][col] = chr(int('0x55', 16) + top_or_bottom + stack_elem)
            else:
                board[row+(stack_elem*direction)][col] = chr(int('0x4B', 16) + top_or_bottom + stack_elem)
        else:
            # black points
            if player == 'black':
                board[row+(stack_elem*direction)][col] = chr(int('0x5A', 16) + top_or_bottom + stack_elem)
            else:
                board[row+(stack_elem*direction)][col] = chr(int('0x50', 16) + top_or_bottom + stack_elem)
    print(board)

def set_cube(value, position, board):
    value = int(value)
    position = int(position)

    if position == -1:
        row = 1
    elif position == 1:
        row = 11
    else:
        row = 6

    if value == 0:
        value = 6
        row = 6

    board[row][0] = chr(int('0x21', 16) + int(value))

def set_turn(turn, dice, board):
    turn = int(turn)
    roll1, roll2 = dice[0], dice[1]
    print(roll1, roll2)


    row = 6 
    if turn == 1:
        # bottom players turn, right side of the board
        col1, col2 = 12, 15
        roll1 = chr(int(int('0x37', 16) + int(roll1)))
        roll2 = chr(int(int('0x37', 16) + int(roll2)))
        print(roll1, roll2)
    else:
        # top players turn, left side of the board
        col1, col2 = 3, 6

    board[row][col1] = roll1
    board[row][col2] = roll2

if __name__ == "__main__":
    # board positions 1-24
    for position, c in enumerate(XGID[0:26], start=1):
        set_pips(position, c, board)

    cube_value, cube_position, turn, dice, score1, score2, crawford_jacoby, match_length, max_cube = XGID[27:].split(':')
    set_cube(cube_value, cube_position, board)
    set_turn(turn, dice, board)

    print(cube_value, cube_position, turn, dice, score1, score2, crawford_jacoby, match_length, max_cube)

    b = '\n'.join([''.join(s) for s in board])
    print(b)

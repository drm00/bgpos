#!/usr/bin/env python3

import sys

# gnubg position id has 14 characters
# extreme gammon position id has 51 characters (?)

XGID = '-a-B--E-B-a-dDB--b-bcb----:1:1:-1:63:0:0:0:3:8'
XGID = '-b--B-C-CA-AdC-a-c-e-A--A-:3:-1:1:62:0:0:3:0:10'
XGID = 'g-----E-C---fE-----b----B-:1:1:1:22:0:0:3:0:10'
XGID = 'aFBBB-A---A-------A---c-b-:1:1:1:21:0:0:3:0:10'

# board consists of 11•19 cells
board = [
    [' ', '\u00F1', '\u00A1', '\u00B2', '\u00B1', '\u00B2', '\u00A2', '\u00F2'],
    [' ', '\u00F0', 'F', 'A', 'F', 'A', 'F', 'A', '\u0040', ' ', '\u0040', 'F', 'A', 'F', 'A', 'F', 'A', '\u00F0', ' '],
    [' ', '\u00F0', 'G', 'B', 'G', 'B', 'G', 'B', '\u0040', ' ', '\u0040', 'G', 'B', 'G', 'B', 'G', 'B', '\u00F0', ' '],
    [' ', '\u00F0', 'H', 'C', 'H', 'C', 'H', 'C', '\u0040', ' ', '\u0040', 'H', 'C', 'H', 'C', 'H', 'C', '\u00F0', ' '],
    [' ', '\u00F0', 'I', 'D', 'I', 'D', 'I', 'D', '\u0040', ' ', '\u0040', 'I', 'D', 'I', 'D', 'I', 'D', '\u00F0', ' '],
    [' ', '\u00F0', 'J', 'E', 'J', 'E', 'J', 'E', '\u0040', ' ', '\u0040', 'J', 'E', 'J', 'E', 'J', 'E', '\u00F0', ' '],
    [' ', '\u00F0', ' ', ' ', ' ', ' ', ' ', ' ', '\u0040', ' ', '\u0040', ' ', ' ', ' ', ' ', ' ', ' ', '\u00F0', ' '],
    [' ', '\u00F0', 'e', 'j', 'e', 'j', 'e', 'j', '\u0040', ' ', '\u0040', 'e', 'j', 'e', 'j', 'e', 'j', '\u00F0', ' '],
    [' ', '\u00F0', 'd', 'i', 'd', 'i', 'd', 'i', '\u0040', ' ', '\u0040', 'd', 'i', 'd', 'i', 'd', 'i', '\u00F0', ' '],
    [' ', '\u00F0', 'c', 'h', 'c', 'h', 'c', 'h', '\u0040', ' ', '\u0040', 'c', 'h', 'c', 'h', 'c', 'h', '\u00F0', ' '],
    [' ', '\u00F0', 'b', 'g', 'b', 'g', 'b', 'g', '\u0040', ' ', '\u0040', 'b', 'g', 'b', 'g', 'b', 'g', '\u00F0', ' '],
    [' ', '\u00F0', 'a', 'f', 'a', 'f', 'a', 'f', '\u0040', ' ', '\u0040', 'a', 'f', 'a', 'f', 'a', 'f', '\u00F0', ' '],
    [' ', '\u00F3', '\u00A3', '\u00B4', '\u00B3', '\u00B4', '\u00A4', '\u00F4'],
]

def XG_get_pipcount_for_point(c):
    if c == '-':
        return 0

    return ord(c.lower()) - 96

def set_pips(position, player, stack_height, board):

    if position < 0 or position > 25:
        return False

    if stack_height < 1 or stack_height > 15:
        return False

    columns = [16, 15, 14, 13, 12, 11, 7, 6, 5, 4, 3, 2]
    if position <= 12:
        row = 11
    else:
        row = 1

    if position == 0 or position == 25:
        # bar
        col = 9
    else:
        # regular points
        if position > len(columns):
            index = 24 - position
        else:
            index = position - 1

        col = columns[index]

    if row == 1:
        direction = 1
    else:
        direction = -1

    top_or_bottom = 32 if direction == -1 else 0

    for stack_elem in range(stack_height):

        if col == 9:
            # checkers on the bar
            if stack_elem <= 4:
                if player == 'bottom':
                    board[row+((4-stack_elem)*direction)][col] = chr(int('0xDB', 16))
                else:
                    board[row+((4-stack_elem)*direction)][col] = chr(int('0xD0', 16))
            else:
                if player == 'bottom':
                    board[row][col] = chr(int('0xDB', 16) + (stack_height-5))
                else:
                    board[row][col] = chr(int('0xD0', 16) + (stack_height-5))

                break

        elif stack_elem <= 4:
            if position % 2 == 0:
                # white points
                if player == 'bottom':
                    board[row+(stack_elem*direction)][col] = chr(int('0x55', 16) + top_or_bottom + stack_elem)
                else:
                    board[row+(stack_elem*direction)][col] = chr(int('0x4B', 16) + top_or_bottom + stack_elem)
            else:
                # black points
                if player == 'bottom':
                    board[row+(stack_elem*direction)][col] = chr(int('0x5A', 16) + top_or_bottom + stack_elem)
                else:
                    board[row+(stack_elem*direction)][col] = chr(int('0x50', 16) + top_or_bottom + stack_elem)

        else:
            if player == 'bottom':
                board[row+(4*direction)][col] = chr(int('0xDB', 16) + (stack_height-5))
            else:
                board[row+(4*direction)][col] = chr(int('0xD0', 16) + (stack_height-5))

            break

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
    if len(dice) == 1:
        if dice == 'D':
            # player has doubled
            pass
        elif dice == 'B':
            # player has doubled, opp. has beavered
            pass
        elif dice == 'R':
            # player has doubled, opp. has beavered, player racconed
            pass
        return

    roll1, roll2 = dice[0], dice[1]

    if roll1 == '0' and roll2 == '0':
        # player is to roll or double
        return

    row = 6
    if turn == 1:
        # bottom players turn, right side of the board
        col1, col2 = 12, 15
        roll1 = chr(int('0x37', 16) + int(roll1))
        roll2 = chr(int('0x37', 16) + int(roll2))
    else:
        # top players turn, left side of the board
        col1, col2 = 3, 6

    board[row][col1] = roll1
    board[row][col2] = roll2

def set_bearoff(checkers, board):
    for i, stack_height in enumerate(checkers):
        if stack_height == 0:
            continue

        full, part = divmod(stack_height, 5)
        if i == 0:
            # top player
            row = 1
            direction = 1
            diff = 0
        else:
            # bottom player
            row = 11
            direction = -1
            diff = 5

        for j in range(full):
            board[row+(j*direction)][18] = chr(int('0xE6', 16) + diff)
        board[row+(full*direction)][18] = chr(int('0xE6', 16) + diff + (5-part))


def XG_validate_id(id):
    s = id.split(':')
    points = s[0]
    setup = s[1:]

    if len(points) != 26:
        return False

    for c in points:
        if c.lower() not in '-abcdefg':
            return False

    try:
        cube_value = int(setup[0])
        if cube_value not in range(10):
            return False

        cube_position = int(setup[1])
        if cube_position not in [1, 0, -1]:
            return False

        turn = int(setup[2])
        if turn not in [1, -1]:
            return False

        roll = setup[3]
        if len(roll) == 1:
            if roll not in ['D', 'B', 'R']:
                return False
        elif len(roll) == 2:
            if roll == '00':
                pass
            else:
                roll1, roll2 = int(roll[0]), int(roll[1])
                if roll1 not in range(1, 7):
                    return False
                if roll2 not in range(1, 7):
                    return False

        score1 = int(setup[4])
        if score1 < 0:
            return False

        score2 = int(setup[5])
        if score2 < 0:
            return False

        crawford_jacoby = int(setup[6])
        match_length = int(setup[7])

        if match_length == 0:
            # unlimited game
            if crawford_jacoby not in range(4):
                return False
        else:
            # match game
            if crawford_jacoby not in range(2):
                return False

        max_cube = int(setup[8])

    except:
        return False

    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"USAGE: {sys.argv[0]} <position id> [--makeimg]")
        sys.exit(1)

    id = sys.argv[1]
    if len(id) == 14:
        # gnubg id
        # translate to xgid? or parse?
        print("GnuBG-IDs not supported yet")
        sys.exit(0)

    if not XG_validate_id(id):
        print("ID not valid!")
        sys.exit(1)

    generate_image = False
    if len(sys.argv) == 3 and sys.argv[2] == '--makeimg':
        from position_to_anki import positions_to_tex, tex_to_pdf, pdf_to_png
        generate_image = True

    # board positions 1-24
    checkers = [0, 0] # top, bottom player
    for position, c in enumerate(id[0:26]):
        stack_height = XG_get_pipcount_for_point(c)
        if c.islower():
            # top player
            player = 'top'
            checkers[0] += stack_height
        else:
            player = 'bottom'
            checkers[1] += stack_height
        set_pips(position, player, stack_height, board)

    checkers[0] = 15 - checkers[0]
    checkers[1] = 15 - checkers[1]
    set_bearoff(checkers, board)

    cube_value, cube_position, turn, dice, score1, score2, crawford_jacoby, match_length, max_cube = id[27:].split(':')
    set_cube(cube_value, cube_position, board)
    set_turn(turn, dice, board)

    #print(cube_value, cube_position, turn, dice, score1, score2, crawford_jacoby, match_length, max_cube)

    position = '\n'.join([''.join(s) for s in board])

    if generate_image:
        tex = positions_to_tex([position])
        tempfile = tex_to_pdf(tex)
        pdf_to_png(tempfile, '.', id)
    else:
        print(position)

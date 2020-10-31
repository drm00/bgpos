#!/usr/bin/env python3

import base64
import sys

import gnubg
import xg

# TODO
# add flag to rotate the board
# combine pips, match and safe_id into one datastructure

XGID = '-a-B--E-B-a-dDB--b-bcb----:1:1:-1:63:0:0:0:3:8'
XGID = '-b--B-C-CA-AdC-a-c-e-A--A-:3:-1:1:62:0:0:3:0:10'
XGID = 'g-----E-C---fE-----b----B-:1:1:1:22:0:0:3:0:10'
xg_to_gnubgids = {
    'aFBBB-A---A-------A---c-b-:1:1:1:21:0:0:3:0:10': 'cwAAoN82IUAAAA:UQkFAAAAAAAA',
}
# AADABwEA2rYAAA:VAkSAAAAAAAA

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
        # TODO set roll1/roll2?

    board[row][col1] = roll1
    board[row][col2] = roll2

def set_bearoff(pips, board):
    # collect total amount of checkers on the board for each player
    checkers = [0, 0]
    for position, data in pips.items():
        if data['player'] == 'top':
            checkers[0] += data['stack']
        else:
            checkers[1] += data['stack']

    checkers = [15-checkers[0], 15-checkers[1]]

    for i, stack_height in enumerate(checkers):
        if stack_height == 0:
            continue

        # a full stack of beared off checkers has height 5
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

        # draw full stacks
        for j in range(full):
            board[row+(j*direction)][18] = chr(int('0xE6', 16) + diff)

        # draw the remaining stack, if there is one
        if part:
            board[row+(full*direction)][18] = chr(int('0xE6', 16) + diff + (5-part))



def position_to_png(position, safe_id, metatext):
    from PIL import Image, ImageDraw, ImageFont

    xg_font_size = 40
    xg_font = ImageFont.truetype('/home/nils/.fonts/extreme gammon.ttf', xg_font_size)
    text_font = ImageFont.truetype('/home/nils/.fonts/libertinusserif-regular.otf', xg_font_size)

    img = Image.new('RGB', (17*xg_font_size, 17*xg_font_size), color='white')
    d = ImageDraw.Draw(img)

    d.text((0,0), position, font=xg_font, spacing=0, fill='black')
    if len(metatext):
        d.text((xg_font_size, 16*xg_font_size), metatext, font=text_font, fill='black')

    img.save(f"{safe_id}.png")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"USAGE: {sys.argv[0]} <position id> [<--topng|--topdf|--convert>]")
        sys.exit(1)

    id = sys.argv[1]
    if len(id) == 14 + 1 + 12:
        pips, match, safe_id = gnubg.parse_id(id)
        metatext = '' # TODO
        print(f"%{match}")
        id_type = 'gnubg'
    else:
        pips, match, safe_id = xg.parse_id(id)
        metatext = '' # TODO
        id_type = 'xg'

    generate_image = False
    generate_pdf = False
    convert = False
    if len(sys.argv) == 3:
        if sys.argv[2] == '--topng':
            generate_image = True
        elif sys.argv[2] == '--topdf':
            generate_pdf = True
        elif sys.argv[2] == '--convert':
            convert = True

    if convert:
        if id_type == 'gnubg':
            print(xg.create_id(pips, match))
        else:
            print(gnubg.create_id(pips, match))
        sys.exit(0)

    for position, data in pips.items():
        set_pips(position, data['player'], data['stack'], board)

    set_bearoff(pips, board)
    set_cube(match["cube_exponent"], match["cube_position"], board)
    set_turn(match["turn"], match["dice"], board)

    #print(cube_value, cube_position, turn, dice, score1, score2, crawford_jacoby, match_length, max_cube)

    position = '\n'.join([''.join(s) for s in board])

    if generate_image:
        position_to_png(position, safe_id, metatext)
    elif generate_pdf:
        from position_to_anki import positions_to_tex, tex_to_pdf
        import shutil
        tex = positions_to_tex([position])
        tempfile = tex_to_pdf(tex)
        shutil.move(f"{tempfile}.pdf", f"{safe_id}.pdf")
    else:
        print(position)

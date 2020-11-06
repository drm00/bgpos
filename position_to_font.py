#!/usr/bin/env python3

import argparse
import base64
import sys

import gnubg
from player import Player
import xg

# TODO
# combine pips, match and safe_id into one datastructure

# board consists of 11•19 cells
# view codepoints with xfd -fa 'eXtreme Gammon'
board = [
    [0x20, 0xF1, 0xA1, 0xB2, 0xB1, 0xB2, 0xA2, 0xF2],
    [0x20, 0xF0, 0x46, 0x41, 0x46, 0x41, 0x46, 0x41, 0x40, 0x20, 0x40, 0x46, 0x41, 0x46, 0x41, 0x46, 0x41, 0xF0, 0x20],
    [0x20, 0xF0, 0x47, 0x42, 0x47, 0x42, 0x47, 0x42, 0x40, 0x20, 0x40, 0x47, 0x42, 0x47, 0x42, 0x47, 0x42, 0xF0, 0x20],
    [0x20, 0xF0, 0x48, 0x43, 0x48, 0x43, 0x48, 0x43, 0x40, 0x20, 0x40, 0x48, 0x43, 0x48, 0x43, 0x48, 0x43, 0xF0, 0x20],
    [0x20, 0xF0, 0x49, 0x44, 0x49, 0x44, 0x49, 0x44, 0x40, 0x20, 0x40, 0x49, 0x44, 0x49, 0x44, 0x49, 0x44, 0xF0, 0x20],
    [0x20, 0xF0, 0x4A, 0x45, 0x4A, 0x45, 0x4A, 0x45, 0x40, 0x20, 0x40, 0x4A, 0x45, 0x4A, 0x45, 0x4A, 0x45, 0xF0, 0x20],
    [0x20, 0xF0, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x40, 0x20, 0x40, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0xF0, 0x20],
    [0x20, 0xF0, 0x65, 0x6A, 0x65, 0x6A, 0x65, 0x6A, 0x40, 0x20, 0x40, 0x65, 0x6A, 0x65, 0x6A, 0x65, 0x6A, 0xF0, 0x20],
    [0x20, 0xF0, 0x64, 0x69, 0x64, 0x69, 0x64, 0x69, 0x40, 0x20, 0x40, 0x64, 0x69, 0x64, 0x69, 0x64, 0x69, 0xF0, 0x20],
    [0x20, 0xF0, 0x63, 0x68, 0x63, 0x68, 0x63, 0x68, 0x40, 0x20, 0x40, 0x63, 0x68, 0x63, 0x68, 0x63, 0x68, 0xF0, 0x20],
    [0x20, 0xF0, 0x62, 0x67, 0x62, 0x67, 0x62, 0x67, 0x40, 0x20, 0x40, 0x62, 0x67, 0x62, 0x67, 0x62, 0x67, 0xF0, 0x20],
    [0x20, 0xF0, 0x61, 0x66, 0x61, 0x66, 0x61, 0x66, 0x40, 0x20, 0x40, 0x61, 0x66, 0x61, 0x66, 0x61, 0x66, 0xF0, 0x20],
    [0x20, 0xF3, 0xA3, 0xB4, 0xB3, 0xB4, 0xA4, 0xF4],
]

def set_pips(position, player, stack_height, mirror, board):

    if position < 0 or position > 25:
        return False

    if stack_height < 1 or stack_height > 15:
        return False

    columns = [16, 15, 14, 13, 12, 11, 7, 6, 5, 4, 3, 2]
    if mirror:
        columns.reverse()

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

    # positions 13-24 are at the top, 1-12 at the bottom
    # build checker stacks on points down from above or up from below
    if position > 12:
        row = 1
        direction = 1
        top_or_bottom = 0
    else:
        row = 11
        direction = -1
        top_or_bottom = 32

    point_color = position % 2 # 0 or 1
    step = 10 * player.value # 10 or 0
    mirror = 5 * int(mirror) # 5 or 0
    if point_color == 1:
        mirror *= -1 # -5 or 0 for black points
    single_checker = 0xD0 + (player.value * 0x0B)
    # white points on even positions, black points on odd positions
    checker_on_point = 0x4B + step + mirror + point_color*5

    for stack_elem in range(stack_height):
        if col == 9:
            # checkers on the bar
            if stack_elem <= 4:
                board[row+((4-stack_elem)*direction)][col] = single_checker
            else:
                board[row][col] = single_checker + (stack_height-5)
                break
        elif stack_elem <= 4:
            board[row+(stack_elem*direction)][col] = checker_on_point + top_or_bottom + stack_elem
        else:
            board[row+(4*direction)][col] = single_checker + (stack_height-5)
            break

def set_cube(cube_exponent, position, mirror, board):

    if position == -1:
        row = 1
    elif position == 1:
        row = 11
    else:
        row = 6

    if cube_exponent == 0:
        # place cube with value 2^6 = 64 in the middle
        cube_exponent = 6
        row = 6

    if mirror:
        cube_col = 18
    else:
        cube_col = 0

    board[row][cube_col] = 0x21 + cube_exponent

def set_turn(turn, dice, board):
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

    roll1, roll2 = int(dice[0]), int(dice[1])

    if roll1 == 0 and roll2 == 0:
        # player is to roll or double
        return

    row = 6
    if int(turn) == 1:
        # bottom players turn, right side of the board
        col1, col2 = 12, 15
        roll1 += 0x37
        roll2 += 0x37
    else:
        # top players turn, left side of the board
        col1, col2 = 3, 6
        roll1 += 0x30
        roll2 += 0x30

    board[row][col1] = roll1
    board[row][col2] = roll2

def set_bearoff(pips, mirror, board):
    # collect total amount of checkers on the board for each player
    checkers = [0, 0]
    for position, data in pips.items():
        checkers[data['player'].value] += data['stack']

    checkers = [15-checkers[0], 15-checkers[1]]
    bearoff_col = 0 if mirror else 18

    for player, stack_height in enumerate(checkers):
        if stack_height == 0:
            continue

        # a full stack of beared off checkers has height 5
        full, part = divmod(stack_height, 5)
        if player == Player.TOP:
            row = 1
            direction = 1
            diff = 0
        else:
            row = 11
            direction = -1
            diff = 5

        # draw full stacks
        for j in range(full):
            board[row+(j*direction)][bearoff_col] = 0xE6 + diff

        # draw the remaining stack, if there is one
        if part:
            board[row+(full*direction)][bearoff_col] = 0xE6 + diff + (5-part)



def position_to_png(position, filename, metatext, show):
    from PIL import Image, ImageDraw, ImageFont

    xg_font_size = 40
    xg_font = ImageFont.truetype('/home/nils/.fonts/extreme gammon.ttf', xg_font_size)
    text_font = ImageFont.truetype('/home/nils/.fonts/libertinusserif-regular.otf', xg_font_size)

    img = Image.new('RGB', (17*xg_font_size, 17*xg_font_size), color='white')
    d = ImageDraw.Draw(img)

    d.text((0,0), position, font=xg_font, spacing=0, fill='black')
    if metatext:
        d.text((xg_font_size, 16*xg_font_size), metatext, font=text_font, fill='black')

    img.save(filename)

    if show:
        img.show()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Create diagrams from position ids.')
    parser.add_argument('gameid', help='GnuBG ID or XGID.')
    parser.add_argument('--mirror', action='store_true', help='Create a mirrored position with the checkers beared off to the left.')
    parser.add_argument('--output', choices=['text', 'png', 'pdf'], default='text', help='Create position as text, png or pdf.')
    parser.add_argument('--show', action='store_true', help='Show png after creation - only valid with --output=png.')
    parser.add_argument('--convert', action='store_true', help='Convert gnubgid to xgid and vice versa.')
    parser.add_argument('--prefix', help='Prefix that gets added before the id in the output filename - only useful with --output=png/pdf')
    args = parser.parse_args()

    if len(args.gameid) == 14 + 1 + 12:
        pips, match, safe_id = gnubg.parse_id(args.gameid)
        if match is None:
            sys.exit(1)
        metatext = '' # TODO
        id_type = 'gnubg'
    else:
        pips, match, safe_id = xg.parse_id(args.gameid)
        if pips is None:
            sys.exit(1)
        metatext = '' # TODO
        id_type = 'xg'

    if args.convert:
        if id_type == 'gnubg':
            print(xg.create_id(pips, match))
        else:
            print(gnubg.create_id(pips, match))
        sys.exit(0)

    if args.mirror:
        # reverse top
        # the font contains 0xAD, but that encodes the 'soft-hyphen',
        # which is not handled well in latex, it seems. Luckily, the
        # font contains the same image at another code point, 0xFE,
        # so just use that.
        # more info on soft hyphen: http://archives.miloush.net/michkap/archive/2006/09/02/736881.html
        board[0][2] = 0xFE
        board[0][6] = 0xAE

        # reverse bottom
        board[-1][2] = 0xAF
        board[-1][6] = 0xB0

    for position, data in pips.items():
        set_pips(position, data['player'], data['stack'], args.mirror, board)

    set_bearoff(pips, args.mirror, board)
    set_cube(match["cube_exponent"], match["cube_position"], args.mirror, board)
    set_turn(match["turn"], match["dice"], board)

    position = '\n'.join([''.join(map(chr, row)) for row in board])

    if args.output.startswith('p') and args.prefix:
        filename = f"{args.prefix}_{safe_id}.{args.output}"
    else:
        filename = f"{safe_id}.{args.output}"

    if args.output == 'png':
        position_to_png(position, filename, metatext, args.show)
    elif args.output == 'pdf':
        from position_to_anki import positions_to_tex, tex_to_pdf
        import shutil
        tex = positions_to_tex([position])
        tempfile = tex_to_pdf(tex)
        shutil.move(f"{tempfile}.pdf", filename)
    else:
        print(position)

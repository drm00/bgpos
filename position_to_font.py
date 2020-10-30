#!/usr/bin/env python3

import base64
import sys

# gnubg position id has 14 characters
# extreme gammon position id has 51 characters (?)
# documentation:
# XGID: http://www.extremegammon.com/extremegammon2.pdf, pp. 146-147
# GnuBG Position ID: https://www.gnu.org/software/gnubg/manual/html_node/A-technical-description-of-the-Position-ID.html#A-technical-description-of-the-Position-ID
# GnuBG Match ID: https://www.gnu.org/software/gnubg/manual/html_node/A-technical-description-of-the-Match-ID.html#A-technical-description-of-the-Match-ID
# GnuBG Match ID (code): https://cvs.savannah.gnu.org/viewvc/gnubg/gnubg/matchid.c?view=log

# TODO
# add flag to rotate the board

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

def XGID_to_GNUBG(xgid):
    pass

def pips_to_gnubgid(pips):
    # assemble position id
    # player on roll is bottom player
    top = []
    bottom = []

    # bottom player starts
    # pos. 25 is the bar of the bottom player
    for position in range(1, 26):

        if position not in pips or pips[position]['player'] != 'bottom':
            bottom.append('0')
            continue

        stack = pips[position]['stack']
        s = '1' * stack + '0'
        bottom.append(s)

    # now, lets do the same for the top player
    # pos. 0 is the bar of the top player
    for position in range(24, -1, -1):

        if position not in pips or pips[position]['player'] != 'top':
            top.append('0')
            continue

        stack = pips[position]['stack']
        s = '1' * stack + '0'
        top.append(s)

    # combine them to a bitstring - gnubg emits top player first
    # also pad the right end to 80 bits
    bitstring = ''.join(top) + ''.join(bottom) + ''.zfill(80-len(bitstring))

    all_bytes = []
    for i in range(0, len(bitstring), 8):
        chunk = bitstring[i:i+8][::-1]
        byte = int(chunk, 2)
        all_bytes.append(byte)
    position_id = base64.b64encode(bytes(all_bytes))
    position_id = position_id[:-2]

    return position_id.decode('utf-8')

def cube_exponent_to_gnubg(cube_exponent):
    if cube_exponent > 15:
        return False

    return bin(2**cube_exponent)[2:].zfill(4)

def pips_to_xgid():
    pass

def gnubg_id_to_bitstring(id):

    # add padding if necessary
    id += '=' * (len(id) % 4)

    key = base64.b64decode(id)

    # strip 0b, expand to 8 bits per byte
    little_endian_bytes = [bin(x)[2:].zfill(8) for x in key]

    # reverse order of bits to get big endian encoding
    big_endian_bytes = [b[::-1] for b in little_endian_bytes]

    bitstring = ''.join(big_endian_bytes)

    return bitstring

def gnubg_create_safe_ids(id):

    # add padding if necessary
    id += '=' * (len(id) % 4)
    key = base64.b64decode(id)
    safe_id = base64.urlsafe_b64encode(key).decode('ascii')
    # remove padding again
    safe_id = safe_id.rstrip('=')

    return safe_id

def gnubg_bitstring_to_pips(bitstring):
    """The gnubg bitstring starts with the top player, while the xgid
    assumes the positions from the bottom players perspective.  Therefore,
    we have to start at position 24 (from the bottom players perspective)
    and go down until we reach the bits from the bottom player, where we
    count up from position 1 again."""

    pips = {}
    pos = 24
    step = -1
    player = 'top'

    for i, bit in enumerate(bitstring):

        if pos == -1:
            # switch to bottom player
            pos = 1
            step = 1
            player = 'bottom'

        if bit == '0':
            pos += step
            continue

        if pos not in pips:
            pips[pos] = {}
        pips[pos] = {
            'stack': pips[pos].get('stack', 0) + int(bit),
            'player': player,
        }

    return pips

def xgid_to_pips(xgid):
    # position 0: checkers on the bar of top player
    # board positions 1-24
    # position 25: checkers on the bar of bottom player
    pips = {}
    for position, c in enumerate(xgid[0:26]):
        stack_height = XG_get_pipcount_for_point(c)
        if stack_height == 0:
            continue
        player = 'top' if c.islower() else 'bottom'
        pips[position] = {
            'stack': stack_height,
            'player': player,
        }

    return pips

def gnubgid_to_pips(positionid):
    bitstring = gnubg_id_to_bitstring(positionid)
    pips = gnubg_bitstring_to_pips(bitstring)

    return pips

def xg_parse_matchid(matchid):
    cube_exponent, cube_position, turn, dice, score1, score2, crawford_jacoby, match_length, max_cube = matchid.split(':')
    cube_position = int(cube_position)

    match = {
        "cube_exponent": cube_exponent,
        "cube_position": cube_position,
        "turn": turn,
        "dice": dice,
        "score_bottom": score1,
        "score_top": score2,
        "match_length": match_length,
    }

    return match

def bitmask(n):
    """Returns a bitmask with n bits set to 1.
    Example: bitmask(4) = 0b1111
    """

    return (1 << n) - 1

def bitsequal(a, b):
    """Compare two integers by XORing them - when they are equal, XOR results in 0 bits set, which is 0.
    Example: bitsequal(1, 1) == True; bitsequal(1, 2) == False
    """

    return (a ^ b) == 0

def extract_and_remove_bits(bitstring, n):
    """Extract the last n bits and remove them from the bitstring integer.
    Example: extract_and_remove_bits(0b10001100, 4) = 0b1100, 0b1000
    """

    extracted = bitstring & bitmask(n)
    bitstring >>= n

    return extracted, bitstring

def gnubg_parse_matchid(matchid):
    """The (extended, now default) match id is a bitstring of length 67.
    Bits are taken from the right end of the bitstring.

    Bit 1-4: Cube
    Bit 5-6: CubeOwner
    Bit 7: DiceOwner
    Bit 8: Crawford
    Bit 9-11: GameState
    Bit 12: TurnOwner
    Bit 13: Double
    Bit 14-15: Resign
    Bit 16-18: Dice1
    Bit 19-21: Dice2
    Bit 22-36: Match length
    Bit 37-51: Score player 0
    Bit 52-66: Score player 1
    Bit 67: Jacoby - this is not documented in the html-matchid-documentation, check the code of matchid.c

    Test:
        QYkqASAAIAAA
        => 0x41 0x89 0x2A 0x01 0x20 0x00 0x20 0x00 0x00
        => 1000 00 1 0 100 1 0 00 101 010 100100000000000 010000000000000 001000000000000
        => has to be reversed
    """

    # bitstring for extended match id has length of 67, but due to base64-encoding,
    # the resulting bitstring from the function is of length 72.
    # We just ignore the remaining bits.
    bitstring = gnubg_id_to_bitstring(matchid)

    # gnubg reverses the position string - maybe the integer gets too big otherwise,
    # as it has a large number of leading zeroes when reversed.
    bitstring = int(bitstring[::-1], 2)

    cube_exponent,  bitstring = extract_and_remove_bits(bitstring, 4)
    cube_owner,     bitstring = extract_and_remove_bits(bitstring, 2)
    player_on_roll, bitstring = extract_and_remove_bits(bitstring, 1)
    crawford,       bitstring = extract_and_remove_bits(bitstring, 1)
    game_state,     bitstring = extract_and_remove_bits(bitstring, 3)
    turn,           bitstring = extract_and_remove_bits(bitstring, 1)
    double_offered, bitstring = extract_and_remove_bits(bitstring, 1)
    resign,         bitstring = extract_and_remove_bits(bitstring, 2)
    dice1,          bitstring = extract_and_remove_bits(bitstring, 3)
    dice2,          bitstring = extract_and_remove_bits(bitstring, 3)
    match_length,   bitstring = extract_and_remove_bits(bitstring, 15)
    score0,         bitstring = extract_and_remove_bits(bitstring, 15)
    score1,         bitstring = extract_and_remove_bits(bitstring, 15)
    jacoby,         bitstring = extract_and_remove_bits(bitstring, 1)
    remaining_bits, bitstring = extract_and_remove_bits(bitstring, 5)

    # input is fully consumed
    assert remaining_bits == 0b00000
    assert bitstring == 0

    # turn bits to xgid match notation
    if bitsequal(cube_owner, 0b11):
        cube_position = 0 # center
    elif bitsequal(cube_owner, 0b00):
        cube_position = -1 # player 0 / top player
    elif bitsequal(cube_owner, 0b01):
        cube_position = 1 # player 1 / bottom player
    else:
        print(f"ERROR: illegal cube position: {cube_position}")
        sys.exit(1)

    if player_on_roll == 0:
        xg_turn = -1 # player0, top player
    else:
        xg_turn = 1 # player1, bottom player

    crawford = bool(crawford)

    # TODO game state

    # TODO turn

    # TODO resign

    dice = ''
    if double_offered:
        dice = 'D'
    elif not double_offered and dice1 == 0 and dice2 == 0:
        # not rolled yet
        dice = '00'
    elif dice1 >= 1 and dice1 <= 6 and dice2 >= 1 and dice2 <= 6:
        dice = str(dice1) + str(dice2)
    else:
        print(f"ERROR: illegal dice: {dice1}/{dice2}")
        sys.exit(1)

    jacoby = not bool(jacoby)

    print(f"%cube exponent: {cube_exponent}")
    print(f"%cube pos: {cube_position}")
    print(f"%player on roll: {player_on_roll}")
    print(f"%crawford: {crawford}")
    print(f"%game state: {game_state}")
    print(f"%xg_turn: {xg_turn}")
    print(f"%double offered: {double_offered}")
    print(f"%resign: {resign}")
    print(f"%dice1: {dice1}")
    print(f"%dice2: {dice2}")
    print(f"%match length: {match_length}")
    print(f"%score0: {score0}")
    print(f"%score1: {score1}")
    print(f"%jacoby: {jacoby}")

    # TODO assemble match description
    # money game / jacoby vs. match game / crawford

    match = {
        "cube_exponent": cube_exponent,
        "cube_position": cube_position,
        "turn": xg_turn,
        "dice": dice,
        "score_bottom": score1, # bottom player
        "score_top": score0, # top player
        "match_length": match_length,
        "jacoby": jacoby,
    }

    return match

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
        print(f"USAGE: {sys.argv[0]} <position id> [<--topng|--topdf>]")
        sys.exit(1)

    id = sys.argv[1]
    if len(id) == 14 + 1 + 12:
        # gnubg id
        positionid, matchid = id.split(':')
        pips = gnubgid_to_pips(positionid)
        match = gnubg_parse_matchid(matchid)
        metatext = '' # TODO
        print(f"%{match}")
        safe_id = gnubg_create_safe_ids(positionid) + ':' + gnubg_create_safe_ids(matchid)
    else:
        if not XG_validate_id(id):
            print("ID not valid!")
            sys.exit(1)
        positionid, matchid = id[:26], id[26:]
        pips = xgid_to_pips(positionid)
        match = xg_parse_matchid(matchid)
        metatext = '' # TODO
        safe_id = id

    #for pos in sorted(pips.keys()):
        #print(f"pos {pos}: {pips[pos]}")

    generate_image = False
    generate_pdf = False
    if len(sys.argv) == 3:
        if sys.argv[2] == '--topng':
            generate_image = True
        elif sys.argv[2] == '--topdf':
            generate_pdf = True

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

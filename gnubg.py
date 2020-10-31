#!/usr/bin/env python3

import base64
import sys

# GnuBG Position ID: https://www.gnu.org/software/gnubg/manual/html_node/A-technical-description-of-the-Position-ID.html#A-technical-description-of-the-Position-ID
# GnuBG Position ID (code): https://cvs.savannah.gnu.org/viewvc/gnubg/gnubg/positionid.c?view=log
# GnuBG Match ID: https://www.gnu.org/software/gnubg/manual/html_node/A-technical-description-of-the-Match-ID.html#A-technical-description-of-the-Match-ID
# GnuBG Match ID (code): https://cvs.savannah.gnu.org/viewvc/gnubg/gnubg/matchid.c?view=log

def _pips_to_gnubgid(pips):
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
    bitstring = ''.join(top) + ''.join(bottom)
    # also pad the right end to 80 bits
    bitstring += ''.zfill(80-len(bitstring))

    all_bytes = []
    for i in range(0, len(bitstring), 8):
        chunk = bitstring[i:i+8][::-1]
        byte = int(chunk, 2)
        all_bytes.append(byte)
    position_id = base64.b64encode(bytes(all_bytes)).decode('ascii')
    position_id = position_id.rstrip('=')

    return position_id

def _match_to_matchid(match):
    return 'TODO'

def create_id(pips, match):
    return _pips_to_gnubgid(pips) + ':' + _match_to_matchid(match)

def cube_exponent_to_gnubg(cube_exponent):
    if cube_exponent > 15:
        return False

    return bin(2**cube_exponent)[2:].zfill(4)

def _id_to_bitstring(id):

    # add padding if necessary
    id += '=' * (len(id) % 4)

    key = base64.b64decode(id)

    # strip 0b, expand to 8 bits per byte
    little_endian_bytes = [bin(x)[2:].zfill(8) for x in key]

    # reverse order of bits to get big endian encoding
    big_endian_bytes = [b[::-1] for b in little_endian_bytes]

    bitstring = ''.join(big_endian_bytes)

    return bitstring

def _create_safe_ids(id):

    # add padding if necessary
    id += '=' * (len(id) % 4)
    key = base64.b64decode(id)
    safe_id = base64.urlsafe_b64encode(key).decode('ascii')
    # remove padding again
    safe_id = safe_id.rstrip('=')

    return safe_id

def _bitstring_to_pips(bitstring):
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

def _id_to_pips(positionid):
    bitstring = _id_to_bitstring(positionid)
    pips = _bitstring_to_pips(bitstring)

    return pips

def _bitmask(n):
    """Returns a bitmask with n bits set to 1.
    Example: _bitmask(4) = 0b1111
    """

    return (1 << n) - 1

def _bitsequal(a, b):
    """Compare two integers by XORing them - when they are equal, XOR results in 0 bits set, which is 0.
    Example: _bitsequal(1, 1) == True; _bitsequal(1, 2) == False
    """

    return (a ^ b) == 0

def _extract_and_remove_bits(bitstring, n):
    """Extract the last n bits and remove them from the bitstring integer.
    Example: _extract_and_remove_bits(0b10001100, 4) = 0b1100, 0b1000
    """

    extracted = bitstring & _bitmask(n)
    bitstring >>= n

    return extracted, bitstring

def _parse_matchid(matchid):
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
    bitstring = _id_to_bitstring(matchid)

    # gnubg reverses the position string - maybe the integer gets too big otherwise,
    # as it has a large number of leading zeroes when reversed.
    bitstring = int(bitstring[::-1], 2)

    cube_exponent,  bitstring = _extract_and_remove_bits(bitstring, 4)
    cube_owner,     bitstring = _extract_and_remove_bits(bitstring, 2)
    player_on_roll, bitstring = _extract_and_remove_bits(bitstring, 1)
    crawford,       bitstring = _extract_and_remove_bits(bitstring, 1)
    game_state,     bitstring = _extract_and_remove_bits(bitstring, 3)
    turn,           bitstring = _extract_and_remove_bits(bitstring, 1)
    double_offered, bitstring = _extract_and_remove_bits(bitstring, 1)
    resign,         bitstring = _extract_and_remove_bits(bitstring, 2)
    dice1,          bitstring = _extract_and_remove_bits(bitstring, 3)
    dice2,          bitstring = _extract_and_remove_bits(bitstring, 3)
    match_length,   bitstring = _extract_and_remove_bits(bitstring, 15)
    score0,         bitstring = _extract_and_remove_bits(bitstring, 15)
    score1,         bitstring = _extract_and_remove_bits(bitstring, 15)
    jacoby,         bitstring = _extract_and_remove_bits(bitstring, 1)
    remaining_bits, bitstring = _extract_and_remove_bits(bitstring, 5)

    # input is fully consumed
    assert remaining_bits == 0b00000
    assert bitstring == 0

    # turn bits to xgid match notation
    if _bitsequal(cube_owner, 0b11):
        cube_position = 0 # center
    elif _bitsequal(cube_owner, 0b00):
        cube_position = -1 # player 0 / top player
    elif _bitsequal(cube_owner, 0b01):
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

def parse_id(id):
    positionid, matchid = id.split(':')
    pips = _id_to_pips(positionid)
    match = _parse_matchid(matchid)
    safe_id = _create_safe_ids(positionid) + ':' + _create_safe_ids(matchid)

    return pips, match, safe_id


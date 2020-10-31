#!/usr/bin/env python3

import sys

# extreme gammon position id has 51 characters (?)
# documentation:
# XGID: http://www.extremegammon.com/extremegammon2.pdf, pp. 146-147

def _pipcount_for_point(c):
    if c == '-':
        return 0

    # a is 1, o is 15
    return ord(c.lower()) - ord('a') + 1

def _is_valid(id):
    points, *setup = id.split(':')

    if len(points) != 26:
        return False

    # check if checker count is above 15 for each player
    total_checkers = [0, 0]
    for c in points:
        if c.lower() not in '-abcdefghijklmno':
            return False

        i = 0 if c.isupper() else 1
        total_checkers[i] += _pipcount_for_point(c)
        if total_checkers[i] > 15:
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

def create_id(pips, match):
    return 'TODO:TODO'

def _parse_positionid(positionid):
    # position 0: checkers on the bar of top player
    # board positions 1-24
    # position 25: checkers on the bar of bottom player
    pips = {}
    for position, c in enumerate(positionid):
        stack_height = _pipcount_for_point(c)
        if stack_height == 0:
            continue
        player = 'top' if c.islower() else 'bottom'
        pips[position] = {
            'stack': stack_height,
            'player': player,
        }

    return pips

def _parse_matchid(matchid):

    m = matchid.split(':')
    cube_exponent = m[0]
    cube_position = int(m[1])
    turn = m[2]
    dice = m[3]
    score1 = m[4]
    score2 = m[5]
    crawford_jacoby = m[6]
    match_length = m[7]
    max_cube = m[8]

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

def parse_id(id):
    if not _is_valid(id):
        print("ID not valid!")
        sys.exit(1)

    positionid, matchid = id.split(':', 1)
    pips = _parse_positionid(positionid)
    match = _parse_matchid(matchid)

    # id is already safe
    return pips, match, id

BULLISH = 1
BEARISH = 0

# class AnalyzeChart:

def hammer(cs0, cs1):
    if cs0.direction == BEARISH:
        return False, 0x00
    elif cs0.us/abs(cs0.body) > .4:
        return False, 0x00
    elif abs(cs0.body)/cs0.range > .2:
        return False, 0x00
    # elif cs0.l > cs1.l:
    #     return False, 0
    return True, 0x01

def star(cs0, cs1):
    if cs0.direction == BULLISH:
        return False, 0x00
    elif cs0.ls/abs(cs0.body) > .2:
        return False, 0x00
    elif abs(cs0.body)/cs0.range > .3:
        return False, 0x00
    # elif cs0.h < cs1.h:
    #     return False, 0
    return True, 0x02

def bearish_engulfing(cs0, cs1):
    if cs0.direction == BULLISH:
        return False, 0
    elif cs1.direction == BEARISH:
        return False, 0
    elif cs1.c > cs0.o:
        return False, 0
    elif cs1.o < cs0.c:
        return False, 0
    elif cs1.h > cs0.h:
        return False, 0
    elif cs1.l < cs0.l:
        return False, 0
    return True, 0x20

def bullish_engulfing(cs0, cs1):
    if cs0.direction == BEARISH:
        return False, 0
    elif cs1.direction == BULLISH:
        return False, 0
    elif cs1.o > cs0.c:
        return False, 0
    elif cs1.c < cs0.o:
        return False, 0
    elif cs1.h > cs0.h:
        return False, 0
    elif cs1.l < cs0.l:
        return False, 0
    return True, 0x040

def piercing_line(cs0, cs1):
    if cs0.direction == BEARISH:
        return False, 0
    elif cs1.direction == BULLISH:
        return False, 0
    elif cs1.o < cs0.o:
        return False, 0
    elif cs1.c < cs0.c:
        return False, 0
    elif cs1.h < cs0.h:
        return False, 0
    elif cs1.l < cs0.l:
        return False, 0
    elif cs0.c < (cs1.range/2 + cs1.c):
        return False, 0
    return True, 0x80

def threeBears(bar1, bar2, bar3):
    if bar1.o > bar2.open:
        return False, 0
    elif bar2.high > bar3.high:
        return False, 0
    return True

def get_avg_range(data):
    sum = 0
    count = 0
    length = 0
    for cs in data:
        if count > 2:
            sum = sum + (float(cs[1]) - float(cs[2]))
            length += 1
        count += 1
    return sum/length

def major_move(cs, atr):
    if abs(cs.body) < atr:
        return False, 0
    elif cs.us/abs(cs.body) > .15:
        return False, 0
    elif cs.ls/abs(cs.body) > .15:
        return False, 0
    return True, 0x004

def gap_up(cs0, cs1):
    if cs1.h < cs0.l:
        return True, 0x008
    else:
        return False, 0

def gap_down(cs0, cs1):
    if cs1.l > cs0.h:
        return True, 0x010
    else:
        return False, 0

def black_marubozu(cs, atr):
    if cs.h != cs.o:
        return False, 0
    elif cs.l != cl.c:
        return False, 0
    elif cs.range < atr:
        return False, 0
    return True, 0x100

def white_marubozu(cs, atr):
    if cs.h != cs.c:
        return False, 0
    elif cs.l != cl.o:
        return False, 0
    elif cs.range < atr:
        return False, 0
    return True, 0x200

def bearish_doji(cs0, cs1):
    if abs(cs0.o-cs0.c)/cs0.range > .05:
        return False, 0
    elif abs(cs0.h - cs0.c)/cs0.range < .7:
        return False, 0
    elif abs(cs0.c - cs0.l)/cs0.range > .3:
        return False, 0
    elif cs0.h < cs1.h:
        return False, 0
    return True, 0x400

def bullish_doji(cs0, cs1):
    if abs(cs0.o-cs0.c)/cs0.range > .05:
        return False, 0
    elif abs(cs0.h - cs0.c)/cs0.range > .3:
        return False, 0
    elif abs(cs0.c - cs0.l)/cs0.range < .7:
        return False, 0
    elif cs0.l > cs1.l:
        return False, 0
    return True,0x800

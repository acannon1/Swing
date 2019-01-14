BULLISH = 1
BEARISH = 0

def isHammer(cs0, cs1):
    if cs0.direction == BEARISH:
        return False
    elif cs0.wick/abs(cs0.body) > .4:
        return False
    elif abs(cs0.body)/cs0.range > .2:
        return False
    # elif cs0.l > cs1.l:
    #     return False
    return True

def isStar(cs0, cs1):
    if cs0.direction == BULLISH:
        return False
    elif cs0.tail/abs(cs0.body) > .2:
        return False
    elif abs(cs0.body)/cs0.range > .3:
        return False
    # elif cs0.h < cs1.h:
    #     return False
    return True

def isCloudCover(cs0, cs1):
    # if cs.direction == BULLISH:
    #     return False
    # elif cs.tail/abs(cs.body) > .2:
    #     return False
    # elif abs(cs.body)/cs.range > .3:
    #     return False
    return True

def isThreeBears(bar1, bar2, bar3):
    if bar1.o > bar2.open:
        return False
    elif bar2.high > bar3.high:
        return False
    return True

def getAvgRange(data):
    sum = 0
    count = 0
    length = 0
    for cs in data:
        if count > 2:
            sum = sum + (float(cs[1]) - float(cs[2]))
            length += 1
        count += 1
    return sum/length

def majorMove(cs):
    if abs(cs.body) < 4:
        return False
    elif cs.wick/abs(cs.body) > .15:
        return False
    elif cs.tail/abs(cs.body) > .15:
        return False
    return True

def gapUp(cs0, cs1):
    if cs1.h < cs0.l:
        return True
    else:
        return False

def gapDown(cs0, cs1):
    if cs1.l > cs0.h:
        return True
    else:
        return False

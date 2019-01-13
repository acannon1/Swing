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

def isStar(cs0):
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

def getAvgRange(cs):
  for i in cs:
    sum = sum + cs[i].range
  return sum/len(cs)

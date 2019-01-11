def isHammer(candleStick):
  if candleStick.h > candleStick.l:
    return True
  else
    return False

def isStar(candleStick):
  if candleStick.h > candleStick.l:
    return True
  else
    return False

def getAvgRange(candleStick):
  for i in candleStick:
    sum = sum + candleStick[i].range
  return sum/len(candleStick)

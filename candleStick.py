
BULLISH = 1
BEARISH = 0

class CandleStick:
  def __init__(self, o, c, h, l, time):
    self.o = o
    self.c = c
    self.h = h
    self.l = l
    self.body = c - o
    self.range = h - l
    if self.body < 0:
      self.direction = BEARISH
      self.wick = h - o
      self.tail = c - l
    else:
      self.direction = BULLISH
      self.wick = h - c
      self.tail = o - l
    self.time = time
    


    

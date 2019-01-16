
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
      self.us = h - o
      self.ls = c - l
    else:
      self.direction = BULLISH
      self.us = h - c
      self.ls = o - l
    self.time = time

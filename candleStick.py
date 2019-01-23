
import datetime as datetime

BULLISH = 1
BEARISH = 0

class CandleStick:
  def __init__(self, quote):
    self.o = quote['open']
    self.c = quote['close']
    self.h = quote['high']
    self.l = quote['low']
    self.body = self.c - self.o
    self.range = self.h - self.l
    if self.body < 0:
      self.direction = BEARISH
      self.us = self.h - self.o
      self.ls = self.c - self.l
    else:
      self.direction = BULLISH
      self.us = self.h - self.c
      self.ls = self.o - self.l
    date = datetime.datetime.fromtimestamp(quote['datetime']/1000.0)
    date = str(date)[0:10]
    self.date = date
    self.volume = quote['volume']

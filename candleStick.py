
BULLISH = 1
BEARISH = 0

class CandleStick:
  def __init__(self, op, cl, hi, lo, time):
    self.op = op
    self.cl = cl
    self.hi = hi
    self.lo = lo
    self.body = cl - op
    self.range = hi - lo
    if self.body < 0:
      self.direction = BEARISH
      self.wick = hi - op
      self.tail = cl - lo
    else:
      self.direction = BULLISH
      self.wick = hi - cl
      self.tail = op - lo
    self.time = time
    


    
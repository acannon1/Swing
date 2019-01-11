import socket #for sockets
import sys	#for exit

import CandleStick
import fxn

def main():
  candleSticks = []
  for i in range(20):
    candleSticks.append(CandleStick())

  idx = 0
  interrupted = False

  try:
	#create an AF_INET, STREAM socket (TCP)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]


  f = open("demofile.txt", "a")
  f.write("Date = ")

  while True:
    time.sleep(3)

    idx = idx + 1
    if idx >= 20:
      idx = 0

    curr = 0
    if idx = 0:
      prev = 19

    if fxn.isHammer(candleSticks[curr]):
      print "Hammer detected."
      f.write("Hammer detected.")

    elif fxn.isStar(candleSticks[curr]):
      print "Star detected."
      f.write("Star detected.")

    if interrupted:
      print "Gotta go"
      break

    avgRange = fxn.getAvgRange(candleSticks)

s.close()
print "Good bye!"

if __name__ == '__main__':
  main()

#!/usr/bin/python
import wiiweight
import sys

def main():
    bb = wiiweight.WiiWeight()

    bb.calibrate()

    exit = False
    while not exit:
        avg = 0.0
        wavg = 0.0
        temp = 0.0

        print "Press something to read stuff"
        c= sys.stdin.read(1)
        if c == 'q':
            exit = True
    
        print bb.getweightedavgweight(5)
        print bb.getaverageweight(5)
#        bb.readweight()
#        bb.printvals()
#        print float(bb.calcweight())
#        for x in range(0,5):
 #           bb.readweight()
  #          bb.printvals()
   #         #print bb.calcweight()
    #        temp = float(bb.calcweight())
     #       print temp
      #      avg = avg + temp
       #     if x == 0:
        #        wavg = temp
         #   else:
          #      wavg = (wavg + temp)/2.0
            
#        print "value of x",x
 #       avg = avg / (x + 1)
  #      print "wavg", wavg
   #     print "avg", avg
    return 0

if __name__ == "__main__":
        sys.exit(main())

#!/usr/bin/python
import sys
sys.path.insert(0, '/home/matt/Downloads/wiibalance/cwiid/python/build/lib.linux-x86_64-2.7/')
import cwiid
import sys
import time

class WiiWeight(object):
    debug = 0

    #constructor/initializer of class
    def __init__( self ):
        self.wiimote = cwiid.Wiimote()

    #Gets the values to actually read as close to zero as possible when nothing is on the scale
    def setzerovals( self, rtcal, rbcal, ltcal, lbcal ):
        self.readweight()
        self.rtzv = rtcal - self.readings['right_top']
        self.rbzv = rbcal - self.readings['right_bottom']
        self.ltzv = ltcal - self.readings['left_top']
        self.lbzv = lbcal - self.readings['left_bottom']
        if self.debug == 1:
            print "rtzv",self.rtzv," = calib",rtcal," - ",self.readings['right_top']
            print "ltzv",self.ltzv," = calib",ltcal," - ",self.readings['left_top']
            print "rbzv",self.rbzv," = calib",rbcal," - ",self.readings['right_bottom']
            print "lbzv",self.lbzv," = calib",lbcal," - ",self.readings['left_bottom']

    #Returns the lowest calibration value of the 3 calibration values for each load cell
    def getlowcal( self, cal):
        return cal[0]

    #Calibrates the balance board **this should be done first after a WiiWeight object is created**
    def calibrate( self ):
        time.sleep(0.5)
        self.wiimote.rpt_mode = cwiid.RPT_BALANCE | cwiid.RPT_BTN
        self.wiimote.request_status()
        self.balance_calibration = self.wiimote.get_balance_cal()
        self.named_calibration = { 'right_top': self.balance_calibration[0],
                                   'right_bottom': self.balance_calibration[1],
                                   'left_top': self.balance_calibration[2],
                                   'left_bottom': self.balance_calibration[3],}
        self.readweight()
        if self.debug == 1:
            print "rt",self.named_calibration['right_top'],"rb",self.named_calibration['right_bottom']
            print "rtlow",self.getlowcal(self.named_calibration['right_top']),"rblow",self.getlowcal(self.named_calibration['right_bottom'])
            print "reading rt",self.readings['right_top']
        self.setzerovals(self.getlowcal(self.named_calibration['right_top']),self.getlowcal(self.named_calibration['right_bottom']),self.getlowcal(self.named_calibration['left_top']),self.getlowcal(self.named_calibration['left_bottom']))

    #Reads the weight from the cwiid package
    def readweight( self ):
        time.sleep(0.2)
        self.wiimote.request_status()
        self.readings = self.wiimote.state['balance']

    #Converts the kg value native to the balance board to lbs
    def converttolbs( self, wkg ):
        """
        Convert weight to pounds
        """
        if self.debug == 1:
            print "wkg",wkg
        wlb = 0
        if ( wkg > 0 ):
            wlb = wkg * 2.20462
            if self.debug == 1:
                print "wlb",wlb
            return wlb
        else:
            return 0

    #Calculates the weight on the balance board in Kilograms but returns in lbs
    def calcweight( self ):
        """
	Determine the weight on the board in hundredths of a kilogram
	"""
        weight = 0
        zeroval = 0
        for sensor in ('right_top', 'right_bottom', 'left_top', 'left_bottom'):
		reading = self.readings[sensor]
		calibration = self.named_calibration[sensor]
                if sensor == 'right_top':
                    zeroval = self.rtzv
                elif sensor == 'right_bottom':
                    zeroval = self.rbzv
                elif sensor == 'left_top':
                    zeroval = self.ltzv
                else:
                    zeroval = self.lbzv
		if reading > calibration[2]:
			print "Warning, %s reading above upper calibration value" % sensor
		if reading < calibration[1]:
			weight += 1700 * (reading + zeroval - calibration[0]) / (calibration[1] - calibration[0])
		else:
			weight += 1700 * (reading + zeroval - calibration[1]) / (calibration[2] - calibration[1]) + 1700

        if self.debug == 1:
            print "weight calculated pre-conversion", weight
            print "return val", self.converttolbs( weight / 100.0 )

        # return self.converttolbs( weight / 100.0 )
        return weight / 100.0

    #Prints the sensor values
    def printvals( self ):
        for sensor in ('right_top', 'right_bottom', 'left_top', 'left_bottom'):
            reading = self.readings[sensor]
            calibration = self.named_calibration[sensor]
            if sensor == 'right_top':
                zeroval = self.rtzv
            elif sensor == 'right_bottom':
                zeroval = self.rbzv
            elif sensor == 'left_top':
                zeroval = self.ltzv
            else:
                zeroval = self.lbzv

            if self.debug == 1:
                print sensor," ",reading," zv ",zeroval," [",calibration[0],",",calibration[1],",",calibration[2],"]"

    #Classic averaging of the passed in number of readings
    def getaverageweight( self, numreadings ):
        avg = 0.0
        temp = 0.0

        for x in range(0,numreadings+1):
            self.readweight()
            self.printvals()
            temp = float(self.calcweight())
            if (self.debug ==1):
                print temp
            avg = avg + temp

        avg = avg / (numreadings + 1)
        if (self.debug == 1) or (self.debug == 2):
            print "Average value", avg,"x value",x

        return avg

    #Weighted average putting more emphasis on later readings
    #uses weighted avg = (weighted avg + new reading)/2 for passed in number of readings
    def getweightedavgweight( self, numreadings ):
        wavg = 0.0
        temp = 0.0

        for x in range(0,numreadings+1):
            self.readweight()
            self.printvals()
            temp = float(self.calcweight())
            if (self.debug ==1):
                print temp
            if x == 0:
                wavg = temp
            else:
                wavg = (wavg + temp)/2.0

        if (self.debug == 1) or (self.debug == 2):
            print "Weighted Average val", wavg,"x value",x

        return wavg

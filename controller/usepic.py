#!/usr/bin/python
import takepic
import sys

def main():

    #Value passed to Takepic is 0 for onboard webcam or 1 etc for usb cams
    tp = takepic.Takepic( 0 )

    tp.write_image("/home/matt/Downloads/wiibalance/cwiid/images/test_pic.png")

if __name__ == "__main__":
    sys.exit(main())

import argparse
import datetime
import imutils
import time
import cv2
from cadeogato import track_cat
from cadeogato2 import track_cat2
from laseraleatorio import random_position


ap = argparse.ArgumentParser()
ap.add_argument("-a","--min-area",type=int,default=900,help="minimum area size")
ap.add_argument("-m","--mode",type=int,default=0,help="0->tracking mode \n 1->random mode")
ap.add_argument("-f","--frame_size",type=int,default=500,help="0->tracking mode \n 1->random mode")

args=vars(ap.parse_args())

#aa
if args["mode"] == 0:
	track_cat(args["min_area"],args["frame_size"],5)
elif args["mode"] == 1:
	random_position(args["frame_size"],5)
elif args["mode"] == 2:
	track_cat2(args["min_area"],args["frame_size"],5)

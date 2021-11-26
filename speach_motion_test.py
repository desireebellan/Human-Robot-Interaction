#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import qi
import argparse
import sys
import time
import os

from say import say
from app_motion_pepper import PlayEmotionController


class test(object):
    def __init__(self,app):
        super(test, self).__init__()

        app.start()
        
        self.session = app.session
        
    def speach_motion(self):
        say(self.session)
        motion = PlayEmotionController(self.session)
        motion.playHappyEmotion()
        
        
        


if __name__ ==  "main":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default='127.0.0.1', help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559, help="Naoqi port number")
    
    args = parser.parse_args()
    pip = args.pip
    pport = args.pport
    
    try:
        	connection_url = "tcp://" + pip + ":" + str(pport)
        	print("trying to connect to "+str(connection_url)+"\n")

        	app = qi.Application(["HRI_test", "--qi-url=" + connection_url ])
        	print("connected to "+str(connection_url)+"\n")

    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n" 
                "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
        
    test(app)
    test.speach_motion()
  

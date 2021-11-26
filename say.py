import qi
import argparse
import sys
import time
import os



def say(session):
    
    language = 'English'
    speed = 1
    strsay = "Hello i'm Pepper"
    

    tts_service = session.service("ALTextToSpeech")

    tts_service.setLanguage(language)
    tts_service.setVolume(1.0)
    tts_service.setParameter("speed", speed)
    tts_service.say(strsay)
    print ("  -- Say: "+strsay)
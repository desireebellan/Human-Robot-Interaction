import qi
import argparse
import sys
import time
import os

from naoqi import ALProxy
import nltk
from nltk.tag.stanford import NERTagger




def say(text, pip, pport):
    
    ttsProxy = ALProxy("ALTextToSpeech", pip, pport)

    ttsProxy.setLanguage("English")
    ttsProxy.setVolume(1.0)
    ttsProxy.setParameter("speed", 50)

    ttsProxy.say(text)
    print ("  -- Say: "+ text)
    
def text():
    output = ""
    output += input()
    return output

def get_name(str:text):

    st = NERTagger('stanford-ner/all.3class.distsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar')

    for sent in nltk.sent_tokenize(text):
        tokens = nltk.tokenize.word_tokenize(sent)
        tags = st.tag(tokens)
        for tag in tags:
            if tag[1]=='PERSON': 
                name = tag
    print (name)
    return name
    
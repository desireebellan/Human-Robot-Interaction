import qi
import argparse
import sys
import time
import os

#to download correctly nltk.tag.stanford.StenfordNERTagger
# change the java_path to the path on you computer
java_path = "/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java.exe"
os.environ['JAVAHOME'] = java_path

from naoqi import ALProxy
import nltk
nltk.download('punkt')
from nltk.tag.stanford import StanfordNERTagger


dir_=os.path.abspath('.')+'/'
st = StanfordNERTagger(dir_+'stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz', dir_+'stanford-ner/stanford-ner.jar')
def say(text, pip, pport):
    
    ttsProxy = ALProxy("ALTextToSpeech", pip, pport)

    ttsProxy.setLanguage("English")
    ttsProxy.setVolume(1.0)
    ttsProxy.setParameter("speed", 50)
    
    ttsProxy.say(text)
    print ("  -- Say: "+ text)
    
def text():
    output = ""
    output += raw_input()
    return output

def get_name(text):

    for sent in nltk.sent_tokenize(text):
        tokens = nltk.tokenize.word_tokenize(sent)
        tags = st.tag(tokens)
        for tag in tags:
            if tag[1]=='PERSON': 
                name = tag
    print (name)
    return name
    

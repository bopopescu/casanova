#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys

windex = []

def index(word):
    encontrou = False
    for no in windex:
        if no[0]==word:
            no[1]+=1;
            encontrou = True
    if not encontrou:
        if len(word)>3:
            windex.append([word,1])

def indexPrint():
    for word in windex:
        print "%s -> %s" % (word[1], word[0])
    
def wordcount(tempfile):
    f = open(tempfile, 'r')
    lines = f.readlines()
    for line in lines:
        words = line.split(" ")
        for word in words:
            index(word)
    indexPrint()

print "Algorítimo de contagem de words"
if len(sys.argv) < 2:
    print "favor passe um arquivo como parametro"
else:
    f = sys.argv[1]
    wordcount(f)
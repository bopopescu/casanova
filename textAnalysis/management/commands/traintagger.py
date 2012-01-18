# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import nltk
from nltk.corpus import *
from textAnalysis.utils import *
import random


def simplify_tag(t):
    if "|" in t:
        return t[:t.index("|")]
    else:
        return t
        
class Command(BaseCommand): 
    
    def handle(self, *args, **options):

        tsents1 = mac_morpho.tagged_sents()
        tsents = [[(w,simplify_tag(t)) for (w,t) in sent] for sent in tsents1 if sent]

        random.shuffle(tsents)
        
        train = tsents[100:]
        test = tsents[:100]

        tagger0 = nltk.DefaultTagger('-None-')
        print tagger0.evaluate(test)

        tagger1 = nltk.UnigramTagger(train, backoff=tagger0)
        print tagger1.evaluate(test)

        tagger2 = nltk.BigramTagger(train, backoff=tagger1)
        print tagger2.evaluate(test)

        tagger3 = nltk.TrigramTagger(train, backoff=tagger2)
        print tagger3.evaluate(test)
        
        saveClassifier(tagger2, "tagger3")

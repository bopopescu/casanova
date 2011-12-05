# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from globocore.materia.models import Materia
from textAnalysis.utils import *
from textAnalysis.management.commands import nerbayes
import nltk

class Command(BaseCommand): 
    
    def handle(self, *args, **options):
        tag = " ".join(args).decode("UTF-8")

        tagger = nltk.data.load("taggers/mac_morpho_aubt.pickle")
        print "tagger antigo", tagger.tag([tag])
        
        tagger1 = nltk.data.load("taggers/unigram_tagger.pickle")
        print "tagger novo-1", tagger1.tag([tag])
        
        tagger2 = nltk.data.load("taggers/macmorpo_sed_tagger.pickle")
        print "tagger novo-2", tagger2.tag([tag])
        
        
        # tagger2 = nltk.BigramTagger(train, backoff=tagger1)
        # nltk.tag.accuracy(tagger2, test)
            
        # classificador = loadClassifier()
        # features = nerbayes.features(tag)
        # 
        # print features
        # print classificador.prob_classify(features).prob('sim')
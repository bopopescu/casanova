# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from globocore.materia.models import Materia
from textAnalysis.utils import *
from textAnalysis.management.commands import trainclassifier
import nltk

class Command(BaseCommand): 
    
    def handle(self, *args, **options):
        tag = " ".join(args).decode("UTF-8")
        _tagger = tagger()
        print "tagger", _tagger.tag([tag])
              
        classificador = loadClassifier()
        features = trainclassifier.features(tag)
        print "classificador", features, classificador.prob_classify(features).prob('sim')

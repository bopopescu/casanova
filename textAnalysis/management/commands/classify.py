# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from globocore.materia.models import Materia
from textAnalysis.utils import *
from textAnalysis.management.commands import trainclassifier, newclassifier
import nltk
from optparse import make_option


class Command(BaseCommand): 
    option_list = BaseCommand.option_list + (
        make_option('--sentenca',
            default='',
            help='features'),
        make_option('--tag',
            default='',
            help='editoria'),
        )
    
    def handle(self, *args, **options):
        
        classificador = loadClassifier()
        features = trainclassifier.features(options['tag'])
        print "classificador", features, classificador.prob_classify(features).prob('sim')

        classificador = loadClassifier("classificador_texto")
        features = newclassifier.features(options['sentenca'],options['tag'])
        print "classificador", features, classificador.prob_classify(features).prob('sim')

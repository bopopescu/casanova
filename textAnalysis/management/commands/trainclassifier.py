# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import nltk
from random import *
from textAnalysis.utils import *
from globocore.materia.models import Materia
import random

_entities = entities()
_tagger = tagger()

# accuracy:  0.923501476062
# Most Informative Features
#              firstletter = 'e'               nao : sim    =    728.9 : 1.0
#              firstletter = 's'               nao : sim    =    480.5 : 1.0
#                   classe = u'ART'            nao : sim    =     89.0 : 1.0
#                   classe = u'NPROP+NPROP+N'    sim : nao    =     88.8 : 1.0
#                   classe = u'N+KC+N'         nao : sim    =     80.7 : 1.0
#              firstletter = '1'               nao : sim    =     58.7 : 1.0
#                   classe = u'NPROP+-None-'    sim : nao    =     53.8 : 1.0
#                   classe = '-None-+-None-'    sim : nao    =     53.0 : 1.0
#                   classe = u'NPROP+N+NPROP'    sim : nao    =     50.8 : 1.0
#              firstletter = 'Y'               sim : nao    =     50.1 : 1.0
#                   classe = u'PRO-KS-REL'     nao : sim    =     47.8 : 1.0
#                   classe = u'NPROP+NPROP+NPROP'    sim : nao    =     43.3 : 1.0

def forced_entity(word):
    classes = ["N","N+N", "N+ADJ", "ADJ+N", "N+N+N", "N+PREP+N"]
    classe = "+".join([(_tagger.tag([w])[0][1]) for w in word.split()])
    if classe in classes:
        return True
    return False

def features(word): 
    features = {}
    classe = "+".join([(_tagger.tag([w])[0][1]) for w in word.split()])
    features['classe'] = classe
    features["firstletter"] = word.split()[0][0]    
    # features["total1"] = len(word)
    features["total2"] = len(word.split())
    return features

                    
class Command(BaseCommand): 
    
    def handle(self, *args, **options):

        materias = Materia.objects.filter(status='T')[:2000]
        words = []
        
        for materia in materias:
            text = "%s. %s. %s" % (materia.titulo,materia.subtitulo,extract_text_from_p(materia.corpo))
            words += extrai_ngram(text)
        
        words = [word for (word,i,f) in words if is_valid_ngram(word)]
            
        featuresets = [(features(word), 'sim' if word in _entities else 'nao') for word in words[:len(_entities)]]
        
        # aprende a identificar assuntos
        # forced_words = [word for word in words if forced_entity(word)]
        # featuresets += [(features(word), 'sim') for word in forced_words[:len(_entities)] if is_valid_ngram(word)]
        
        featuresets += [(features(word), 'sim') for word in _entities if is_valid_ngram(word)]
        
        random.shuffle(featuresets)
        
        # print featuresets
        train_set, test_set = featuresets[:len(featuresets)*80/100], featuresets[len(featuresets)*80/100:]
        classificador = nltk.NaiveBayesClassifier.train(train_set)
        print 'accuracy: ', nltk.classify.util.accuracy(classificador, test_set)
        print classificador.show_most_informative_features(20)
        
        saveClassifier(classificador)

        # print classificador.prob_classify(time_features(times[0][0])).prob('Entidade')


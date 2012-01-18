# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import nltk
from random import *
from textAnalysis.utils import *
from globocore.materia.models import Materia
import random
from lxml import html as lhtml


def features(m): 
    html = lhtml.fromstring(m.corpo.decode('utf-8'))

    title = tuple(m.titulo.split())
    related = tuple([(idx, tuple(val.text_content().split())) for (idx, val) in enumerate(html.cssselect('.saibamais ul li a'))])
    
    # related[idx] = val.text_content().split() 


    feats = {
        'related': related,
    }

    return feats    
    
    # feats = {
    #     'bias': True,
    #     'shape': shape(word),
    #     'wordlen': len(word),
    #     'prefix3': word[:3].lower(),
    #     'suffix3': word[-3:].lower(),
    #     'pos': pos,
    #     'word': word,
    #     'en-wordlist': (word in _short_en_wordlist), # xx!
    #     'prevtag': prevtag,
    #     'prevpos': prevpos,
    #     'nextpos': nextpos,
    #     'prevword': prevword,
    #     'nextword': nextword,
    #     'word+nextpos': '%s+%s' % (word.lower(), nextpos),
    #     'pos+prevtag': '%s+%s' % (pos, prevtag),
    #     'shape+prevtag': '%s+%s' % (shape, prevtag),
    #     }
    
    return feats

                    
class Command(BaseCommand): 
    
    def handle(self, *args, **options):

        materias = Materia.objects.filter(status='T')[:500]
        featuresets = [(features(m), tuple(m.titulo.split())) for m in materias]

        random.shuffle(featuresets)
        
        # print featuresets
        train_set, test_set = featuresets[:len(featuresets)*80/100], featuresets[len(featuresets)*80/100:]
        classificador = nltk.NaiveBayesClassifier.train(train_set)
        
        print 'accuracy: ', nltk.classify.util.accuracy(classificador, test_set)
        print classificador.show_most_informative_features(20)

        dict_test = {
            'related': (
                        (0, (u'Justi\xe7a', u'bloqueia', u'bens', u'de', u'dono', u'de', u'Porsche', u'envolvido', u'em', u'acidente', u'em', u'SP')), 
                        (1, ('Dono', 'de', 'Porsche', 'chora', 'ao', 'falar', 'sobre', 'acidente', 'em', 'SP,', 'diz', 'delegado'))
                        ), 
        }
        
        print classificador.prob_classify(dict_test).prob(tuple('Delegado diz que laudo mostra velocidade de Porsche antes de bater'.split()))


        # print features('sergio')
        # saveClassifier(classificador)


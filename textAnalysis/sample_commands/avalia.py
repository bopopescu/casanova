# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from globocore.materia.models import Materia
import time
from lxml import html as lhtml
from textAnalysis.estrategia_consulta import relacionadas
from django.conf import settings
import re
from textAnalysis.models import Analytics 
from textAnalysis.utils import *
from textAnalysis.classifier import * 
import nltk
from random import *

def remove_host(url):
    return re.sub(settings.BASE_URL,
                    "",
                    url)

def change_host(url):
    return re.sub('http://www.techtudo.com.br',
                    settings.BASE_URL,
                    url)
                    
def get_document(m):
    documento = {}
    documento['permalink'] = m.permalink
    documento['titulo']= m.titulo
    documento['subtitulo']= m.subtitulo
    documento['texto']= m.corpo
    documento['editorias'] = [editoria.folder for editoria in m.editorias()]
    documento['entidades'] = [entidade for entidade in m.cita.all()]
    return documento

def classifica(m, documents):
    shuffle(documents)
    featuresets = [(document_features_single(d), c) for (d,c) in documents]
    train_set, test_set = featuresets[:len(documents)*80/100], featuresets[len(documents)*80/100:]
    classificador = nltk.NaiveBayesClassifier.train(train_set)
    # print 'accuracy: ', nltk.classify.util.accuracy(classificador, test_set)
    # import pdb; pdb.set_trace();
    prob = classificador.prob_classify(document_features_single(tf(m.corpo).keys())).prob("dentro")
    return prob
                    
class Command(BaseCommand): 
    
    def handle(self, *args, **options):
        contador = 0
        total = 50
        materias = Materia.objects.filter(corpo__icontains='saibamais')[:total]
        # materias = [Materia.objects.get(id=863)]
        
        i = 0

        for m in materias:
            print  "\n",m.titulo
            documento = get_document(m)
            # html = lhtml.fromstring(m.corpo.decode('utf-8'))
            # documento['relacionadas'] = set([ change_host(h.attrib['href']) for h in html.cssselect('.saibamais ul li a')])            
            
            recomendadas = [str(recomendada.permalink) for recomendada in relacionadas(documento, 4)]
            for r in recomendadas:
                urls = [u.origem for u in Analytics.objects.filter(destino=r).order_by('pageviews')]
                documents = [(tf(m.corpo).keys(), "dentro") for m in Materia.objects.filter(permalink__in=urls)]
                
                prob = 0
                if documents:
                    documents += [(tf(m.corpo).keys(), "fora") for m in Materia.objects.exclude(permalink__in=urls)[:len(documents)]]
                    prob = classifica(m, documents)
                    # print i, round(prob, 2)
                    if prob > 0.7:
                        print round(prob, 2), r
                    i +=1
        
        # print "total de recomendações ok=>",contador
        # print "percentual=>%s" % (float(contador)/total)

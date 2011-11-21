# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from globocore.materia.models import Materia
import datetime
from textAnalysis.utils import *

                    
class Command(BaseCommand): 
    
    def handle(self, *args, **options):
        data = datetime.datetime(day=1,month=10,year=2011)
        contador = {}
        materias = Materia.objects.filter(ultima_publicacao__gt=data, status='P')
        moda = {}
        for m in materias:
            stop = stopwords()
            words = [word.lower() for word in clean(m.corpo).split() if word not in stop]
            for word_DE in words:
                moda[word_DE]={}
                for word_PARA in words:
                    if moda[word_DE].has_key(word_PARA):
                        moda[word_DE][word_PARA]+=1
                    else:
                        moda[word_DE][word_PARA]=0
                
        for key in sorted(moda.keys()):
            items = [(v, k) for k, v in moda[key].items()]
            items.sort()
            items.reverse()
            items = [(k, v) for v, k in items]
            print key, items[0][0], items[0][1]

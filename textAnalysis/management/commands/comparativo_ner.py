# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from globocore.materia.models import Materia
from textAnalysis.utils import *
from textAnalysis.ner import *
from textAnalysis.management.commands import nerbayes

class Command(BaseCommand): 
    
    def handle(self, *args, **options):

        methods = []
        methods.append(ltask)
        methods.append(yahoo)
        methods.append(nltk)
        methods.append(zemanta)
        methods.append(my_fastercts)
        accuracy={}

        entidades = [entidade for entidade in entities()][:100]

        for ent in entidades:
            for method in methods:
                ner = NER(method)
                entidades = ner.processa(ent)
                if ent in entidades:
                    if accuracy.has_key(method.func_name):
                        accuracy[method.func_name]+=1
                    else:
                        accuracy[method.func_name]=1
                else:
                    print "(%s)-%s" % (ent,entidades) 

        print accuracy

        

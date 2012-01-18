# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from globocore.materia.models import Materia
from textAnalysis.utils import *

from textAnalysis.management.commands import nerbayes
            
_entities = entities()
classificador = loadClassifier()

def is_entity(tag):
    features = nerbayes.features(tag)
    # print features, tag,  classificador.prob_classify(features).prob('sim')
    return True if classificador.prob_classify(features).prob('sim') > 0.70 else False    

def p_ngram(m):
    for n in m:
        tag = " ".join(n).decode("UTF-8")
        if is_entity(tag):  
            print tag             
                        
class Command(BaseCommand): 
    
    def handle(self, *args, **options):
        id = args[0]
        materia = Materia.objects.get(id=id)
        
        text = "%s %s %s" % (materia.titulo,materia.subtitulo,extract_text_from_p(materia.corpo))
        
        for i in range(1,4):
            m =[]
            for frase in text.split("."):
                m.extend(colocation(clean(frase.decode("UTF-8")),i))
            p_ngram(m)
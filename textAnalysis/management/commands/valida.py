# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from globocore.materia.models import Materia, Folder
import time
from lxml import html as lhtml
from textAnalysis.estrategia_consulta import relacionadas
from django.conf import settings
import re
from textAnalysis.estrategia_consulta import *
from textAnalysis.utils import *
from textAnalysis.ner import *


def remove_host(url):
    return re.sub(settings.BASE_URL,
                    "",
                    url)

def change_host(url):
    return re.sub('http://g1.globo.com',
                    settings.BASE_URL,
                    url)
                    
def monta_doc(m):
    documento ={}
    documento['permalink'] = m.permalink
    documento['titulo']= m.titulo
    documento['subtitulo']=m.subtitulo
    documento['texto']=m.corpo
    documento['editorias'] = [editoria.folder for editoria in m.editorias()]
    # documento['entidades'] = [entidade for entidade in m.cita.all()] 
    html = lhtml.fromstring(m.corpo.decode('utf-8'))
    documento['relacionadas'] = set([ change_host(h.attrib['href']).lower() for h in html.cssselect('.saibamais ul li a')])            
    return documento
            
class Command(BaseCommand): 
    
    def handle(self, *args, **options):
        total = 100
        # materias = Materia.objects.filter(status='T')[:total]
        
        folder = Folder.objects.get(name='Planeta Bizarro')
        materias = Materia.objects.filter(status='T').exclude(folders=folder)[:total]
        # materias = Materia.objects.filter(status='T', folders=folder)[:total]
        
        contador = 0

        for m in materias:
            documento = monta_doc(m)

            query, words = single_words_entities(documento)

            # query, words = word_frequency(documento)
            # query2, words2 = entidades(documento)
            # query.extend(query2)

            materiasSolr = relacionadas(documento, 5, query[0])
            recomendadas = []
            recomendadas = [str(recomendada.url) for (recomendada, score) in materiasSolr]
            encontradas = documento['relacionadas'].intersection(recomendadas)
            if any(encontradas):
                contador +=1
            
            print contador

        print "acerto=>", contador*1.0/len(materias),contador, len(materias)


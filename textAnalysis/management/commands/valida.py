# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from globocore.materia.models import Materia
import time
from lxml import html as lhtml
from textAnalysis.estrategia_consulta import relacionadas
from django.conf import settings
import re
from textAnalysis.estrategia_consulta import *
from textAnalysis.utils import *
from textAnalysis.ltask import *


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
    documento['subtitulo']= m.subtitulo
    documento['texto']= m.corpo
    documento['editorias'] = [editoria.folder for editoria in m.editorias()]
    # documento['entidades'] = [entidade for entidade in m.cita.all()] 
    html = lhtml.fromstring(m.corpo.decode('utf-8'))
    documento['relacionadas'] = set([ change_host(h.attrib['href']).lower() for h in html.cssselect('.saibamais ul li a')])            
    return documento
            
class Command(BaseCommand): 
    
    def handle(self, *args, **options):
        total = 50
        materias = Materia.objects.filter(status='T')[:total]
        contador = 0


        for m in materias:
            documento = monta_doc(m)
            query, words = better_words_from_doc(documento)
            ltask = lTask()
            
            corpo = clean(extract_text_from_p(documento['texto']),remove_signs=False)
            texto = "%s %s %s" % (documento['titulo'],documento['subtitulo'], corpo)
            
            entidades=[]
            entidades = ltask.html(texto)
            entidades += [(query,"QUERY")]
            
            # import pdb; pdb.set_trace();
            
            for (entidade,tipo) in entidades:
                # print m.id, entidade, tipo
                if tipo == "QUERY":
                    query = entidade
                else:
                    query = ["title:(%s)" % entidade]
                
                materiasSolr = relacionadas(documento, 5, query[0])
                recomendadas = []
                recomendadas = [str(recomendada.url) for (recomendada, score) in materiasSolr]
                encontradas = documento['relacionadas'].intersection(recomendadas)
                if any(encontradas):
                    contador +=1
                    # print contador
                    break

        print "acerto=>", contador*1.0/len(materias),contador, len(materias)


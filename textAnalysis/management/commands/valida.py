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
        total = 1000
        materias = Materia.objects.filter(status='T')[:total]
        contador = 0
        estrategias = []
        estrategias.append(Estrategia(consulta_unigrams_in_title))
        # estrategias.append(Estrategia(consulta_bigrams_in_title))
        # estrategias.append(Estrategia(consulta_trigrams_in_title))    
        # estrategias.append(Estrategia(consulta_na_categoria))
        for m in materias:
            documento = monta_doc(m)
            
            query = ""
            for e in estrategias:
                if query:
                    query += " OR "
                query += e.query(documento)[0]            
            
            recomendadas = []
            recomendadas = [str(recomendada.url) for (recomendada, score) in relacionadas(documento, 15, query)]
            encontradas = documento['relacionadas'].intersection(recomendadas)
            if any(encontradas):
                contador +=1

        print "acerto=>", contador*1.0/len(materias),contador, len(materias)

        total = 1000
        materias = Materia.objects.filter(status='T')[:total]
        contador = 0
        estrategias = []
        # estrategias.append(Estrategia(consulta_unigrams_in_title))
        estrategias.append(Estrategia(consulta_bigrams_in_title))
        # estrategias.append(Estrategia(consulta_trigrams_in_title))    
        # estrategias.append(Estrategia(consulta_na_categoria))
        for m in materias:
            documento = monta_doc(m)
            
            query = ""
            for e in estrategias:
                if query:
                    query += " OR "
                query += e.query(documento)[0]            
            
            recomendadas = []
            recomendadas = [str(recomendada.url) for (recomendada, score) in relacionadas(documento, 15, query)]
            encontradas = documento['relacionadas'].intersection(recomendadas)
            if any(encontradas):
                contador +=1

        print "acerto=>", contador*1.0/len(materias),contador, len(materias)

        total = 1000
        materias = Materia.objects.filter(status='T')[:total]
        contador = 0
        estrategias = []
        # estrategias.append(Estrategia(consulta_unigrams_in_title))
        # estrategias.append(Estrategia(consulta_bigrams_in_title))
        estrategias.append(Estrategia(consulta_trigrams_in_title))    
        # estrategias.append(Estrategia(consulta_na_categoria))
        for m in materias:
            documento = monta_doc(m)
            
            query = ""
            for e in estrategias:
                if query:
                    query += " OR "
                query += e.query(documento)[0]            
            
            recomendadas = []
            recomendadas = [str(recomendada.url) for (recomendada, score) in relacionadas(documento, 15, query)]
            encontradas = documento['relacionadas'].intersection(recomendadas)
            if any(encontradas):
                contador +=1

        print "acerto=>", contador*1.0/len(materias),contador, len(materias)
        
        total = 1000
        materias = Materia.objects.filter(status='T')[:total]
        contador = 0
        estrategias = []
        estrategias.append(Estrategia(consulta_unigrams_in_title))
        estrategias.append(Estrategia(consulta_bigrams_in_title))
        # estrategias.append(Estrategia(consulta_trigrams_in_title))    
        # estrategias.append(Estrategia(consulta_na_categoria))
        for m in materias:
            documento = monta_doc(m)
            
            query = ""
            for e in estrategias:
                if query:
                    query += " OR "
                query += e.query(documento)[0]            
            
            recomendadas = []
            recomendadas = [str(recomendada.url) for (recomendada, score) in relacionadas(documento, 15, query)]
            encontradas = documento['relacionadas'].intersection(recomendadas)
            if any(encontradas):
                contador +=1

        print "acerto=>", contador*1.0/len(materias),contador, len(materias)
        
        total = 1000
        materias = Materia.objects.filter(status='T')[:total]
        contador = 0
        estrategias = []
        estrategias.append(Estrategia(consulta_unigrams_in_title))
        estrategias.append(Estrategia(consulta_bigrams_in_title))
        estrategias.append(Estrategia(consulta_trigrams_in_title))    
        # estrategias.append(Estrategia(consulta_na_categoria))
        for m in materias:
            documento = monta_doc(m)
            
            query = ""
            for e in estrategias:
                if query:
                    query += " OR "
                query += e.query(documento)[0]            
            
            recomendadas = []
            recomendadas = [str(recomendada.url) for (recomendada, score) in relacionadas(documento, 15, query)]
            encontradas = documento['relacionadas'].intersection(recomendadas)
            if any(encontradas):
                contador +=1

        print "acerto=>", contador*1.0/len(materias),contador, len(materias)
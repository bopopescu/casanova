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

def link_e_valido(permalink):
    try:
        m = Materia.objects.get(permalink=permalink)
    except:
        return False
    return True
                    
def esta_no_solr(permalink):
    solr_connection = SolrConnection(settings.SOLRSERVER)
    m = Materia.objects.get(permalink=permalink)
    consulta = solr_connection.query('identifier:"%s"'%m.obtem_url_visao_de_busca(search_type='solr'))
    solr_connection.close()
    if not consulta.results:
        return False
    return True
            
class Command(BaseCommand): 
    
    def handle(self, *args, **options):
        documento = {}
        validas = 0
        datainicio = datetime.datetime(day=1,month=10,year=2011)
        datafim = datetime.datetime(day=31,month=10,year=2011)
        
        materias = Materia.objects.filter(corpo__icontains='saibamais', ultima_publicacao__gt=datainicio, ultima_publicacao__lt=datafim)[:2000]
        for m in materias:
            validas +=1
            html = lhtml.fromstring(m.corpo.decode('utf-8'))
            documento['relacionadas'] = set([ change_host(h.attrib['href']).lower() for h in html.cssselect('.saibamais ul li a')])            

            for uri in documento['relacionadas']:
                if link_e_valido(remove_host(uri)):
                    if not esta_no_solr(remove_host(uri)):
                        m.notifica_barramento("publicar")
                    
                    if len(Materia.objects.filter(status='T'))<1000:
                        m.status = 'T'
                        m.save()
                else:
                    validas -=1
                    break

            if validas >=1000:
                break 



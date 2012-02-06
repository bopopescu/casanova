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
        datainicio = datetime.datetime(day=1,month=1,year=2011)
        # datafim = datetime.datetime(day=30,month=10,year=2011)
        
        editorias = ['Brasil','São Paulo','Rio de Janeiro','Minas Gerais',
        'Economia','Política','Mundo','Espírito Santo','Pop & Arte',
        'Auto Esporte','Concursos e Emprego','Ciência e Saúde',
        'Mercados','Música','Tecnologia e Games']
        
        editorias_id = [39,31,119,214,339,216,146,
                        8,133,101,94,20,42,76,105]
        
        editorias_excluir = [182,360,349,351,138,329,109,219,284,373,229,285,108,271,272,268,266,
                             364,367,303,47,126,183,184,370,269,162,161,321,238,132,286,391,287,
                             217,258,290,179,384,385,142,309,310,148,334,335,164,356,357,292,331,
                             333,355,144,158,199,157,106,147,348,186,389,178,145,232,324,325,235,
                             318,320,387,388,163,342,344,185,350,361,4,130,131,256,44,177,352,181,
                             245,246,247,288,353,43,46,37,383,305,260,296,297,368,29,218,311,107,
                             228,221,276,248,249,379,359,222,323,322,237,300,301,358,283,374,215,230,
                             223,306,45,239,386,291,279,267,369,365,213,187,188,362,363,377,378,289,
                             336,337,220,151,326,327,236,175,340,345,371,255,171,295,390,275,278,293,
                             277,270,134,250,251,252,307,314,315,298,231,212,129,27]

        # materias = Materia.objects.filter(status='T')
        # print len(materias)
        # for m in materias:
        #     for f in m.relatedfolder_set.all():
        #         if f.folder_id in editorias_excluir:
        #             m.status = 'P'
        #             m.save()
        #             break
        #     print m.id, m.status
        #     
        # print len(Materia.objects.filter(status='T'))
                    
        total_editoria = 300
        sair = False
        # if len(Materia.objects.filter(status='T')) >= 1440:
        #     print "já chegamos no limite"
        #     return
            
        for editoria in editorias_id:
            folder = Folder.objects.get(id=editoria)
            
            materias = Materia.objects.filter(corpo__icontains='saibamais', folders=folder, status='P', ultima_publicacao__gt=datainicio).order_by('ultima_publicacao')
            # tot = len(Materia.objects.filter(status='T', folders=folder))
            tot =0
            print folder,tot,len(materias)            
        
            for i, m in enumerate(materias):
                valida = False
                if tot >= total_editoria:
                    break
                
                sair = False    
                for f in m.relatedfolder_set.all():
                    if f.folder_id in editorias_excluir:
                        sair = True
               
                if not sair:
                    try:
                        html = lhtml.fromstring(m.corpo.decode('utf-8'))
                        documento['relacionadas'] = set([ change_host(h.attrib['href']).lower() for h in html.cssselect('.saibamais ul li a')])            
                        for uri in documento['relacionadas']:
                            if link_e_valido(remove_host(uri)):
                                try:
                                    if not esta_no_solr(remove_host(uri)):
                                        m1 = Materia.objects.get(permalink=remove_host(uri))
                                        m1.status = 'P'
                                        m1.save()
                                        m1.notifica_barramento("publicar")
                                    valida = True
                                except:
                                    valida = False
                                    pass
                            else:
                                # import pdb; pdb.set_trace();
                                # print "fail", remove_host(uri)
                                m.status = 'R'
                                m.save()
                                valida = False
                                break
                    except:
                        valida = False
                        pass
                    
                    if valida:
                        tot+=1
                        m.status = 'T'
                        m.save()
                        
        
        

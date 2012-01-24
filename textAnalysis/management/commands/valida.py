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
from optparse import make_option

import itertools


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
    html = lhtml.fromstring(m.corpo.decode('utf-8'))
    documento['html_tags'] = [ tag.text for tag in html.cssselect('p strong') if tag.text]
    documento['html_tags'] += [ tag.text for tag in html.cssselect('p em') if tag.text]
    documento['caption'] = [ tag.text for tag in html.cssselect('.foto strong') if tag.text]
    documento['caption'] += [ tag.text for tag in html.cssselect('.video strong') if tag.text]
    documento['relacionadas'] = set([ change_host(h.attrib['href']).lower() for h in html.cssselect('.saibamais ul li a')])            
    return documento

            
class Command(BaseCommand): 
    option_list = BaseCommand.option_list + (
        make_option('--sequential',
            default='se',
            help='features'),
        make_option('--editoria',
            default='',
            help='editoria'),
        make_option('--total',
            default=100,
            help='total'),
        make_option('--recomendadas',
            default=5,
            help='materias recomendadas'),
        make_option('--similaridade',
            default=False,
            help='similaridade'),
        )
    
    def handle(self, *args, **options):
        
        if options['editoria']:
            folder = Folder.objects.get(name=options['editoria'])
            materias = Materia.objects.filter(status='T', folders=folder)
        else:
            materias = Materia.objects.filter(status='T')
            
        materias = materias[:options['total']]

        # editorias_id = [39,31,119,214,339,216,146,
        #                 8,133,101,94,20,42,76,105]
        # for f in editorias_id:
        #     folder = Folder.objects.get(id=f)
        #     materias = Materia.objects.filter(status='T', folders=folder)[:total]
    
        contador = 0
        combinacoes = []
        dict_combinacoes = {}
        seq = options['sequential']
        for tam_comb in range(len(seq)):
            for comb in itertools.combinations(seq,tam_comb+1):
                combinacoes.append("".join(comb))

        for m in materias:
            contador+=1
            print contador
            for comb in combinacoes: 
                documento = monta_doc(m)
                materiasSolr = relacionadas(documento, comb=comb, total=int(options['recomendadas']), similaridade=eval(options['similaridade']))
                recomendadas = []
                recomendadas = [str(recomendada.url) for (recomendada, score) in materiasSolr]
                encontradas = documento['relacionadas'].intersection(recomendadas)
                if any(encontradas):
                    if dict_combinacoes.has_key(comb):
                        dict_combinacoes[comb]+=1
                    else:
                        dict_combinacoes[comb]=1
        
        print "total de acertos em %s matérias" % (contador)
        
        for dc in dict_combinacoes.keys():
            print dc,dict_combinacoes[dc]
            


# -*- coding: utf-8 -*-
from textAnalysis.statistics import extrair_tags
from django.template import RequestContext
from django.shortcuts import render_to_response
from globocore.common.solr import SolrConnection
from django.conf import settings
from common.materia_do_solr import MateriaDoSolr        
import re
from globocore.materia.models import Materia

def classify(request):
    tags = ""
    textos = ""
    materias = []
    permalink = None
    
    if request.POST.get('permalink'):
        permalink = request.POST.get('permalink')
    
    
    if request.POST.get('titulo'):
        textos+=request.POST.get('titulo')
        textos+=" "
    if request.POST.get('subtitulo'):
        textos+=request.POST.get('subtitulo')
        textos+=" "
    if request.POST.get('texto'):
        textos+=request.POST.get('texto')
        textos+=" "

    if textos:

        for (tag, f) in extrair_tags(textos):
            tags += "%s " % tag
        solr_connection = SolrConnection(settings.SOLRSERVER)

        query = tags.encode('utf-8')
        consulta = solr_connection.query(query + " isIssued:true", wt='json', start=0, rows=15,
                                        indent='on', sort='issued', sort_order='desc')
        solr_connection.close()

        for materiaSolr in consulta.results:
            materia = MateriaDoSolr(materiaSolr)
            idMateria = re.search('(?<=[a-z]/)[0-9]*', materia.identifier).group(0)
            m = Materia.objects.get(id = idMateria)    
            
            # corta propria materia 
            if permalink != m.permalink:
                #gambi para mostrar foto em dev
                imagem = m.obtem_caminho_absoluto_de_delivery_do_thumbnail_para_plantao()
                if imagem:
                    imagem = re.sub('http://anotherdomain.localhost:8000/po/tt/f/',
                                    'http://s.glbimg.com/po/tt/f/',
                                    imagem)
                    m.thumbnail = imagem
                else:
                    m.thumbnail = ""
    
                if m not in materias:
                    materias += [m]
    
                if len(materias) >=5:
                    break
    
    context = {'saibamais':materias}
    return render_to_response('admin/materia/materia/materias.html', context, RequestContext(request,context) )

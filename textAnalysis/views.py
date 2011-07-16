# -*- coding: utf-8 -*-
from textAnalysis.statistics import extrair_tags
from django.http import HttpResponse
from globocore.common.solr import SolrConnection
from django.conf import settings
from common.materia_do_solr import MateriaDoSolr        


def classify(request):
    tags = ""
    textos = ""
    materias = ""
    
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
        print tags    
        query = tags.encode('utf-8')
        consulta = solr_connection.query(query + " isIssued:true", wt='json', start=0, rows=5,
                                        indent='on', sort='issued', sort_order='desc')
        solr_connection.close()
        for m in consulta.results:
            materia = MateriaDoSolr(m)
            # {% if noticia.thumbnail %} 
            # <div class="foto">
            #   <a class="borda-interna" href="{{ noticia.url }}"><img src="{{ noticia.thumbnail }}" /></a>
            #   {% rounded_corners %}
            # </div>
            # {% endif %}

            imagem = ""
            link = ""
            if materia.__dict__.has_key("url"):
                link = materia.url

            import re
            from globocore.materia.models import Materia
            from tectudo.templatetags.resize_image import resize
            
            idMateria = re.search('(?<=[a-z]/)[0-9]*', materia.identifier).group(0)
            m = Materia.objects.get(id = idMateria)    
            imagem = m.obtem_caminho_absoluto_de_delivery_do_thumbnail_para_plantao()
            if imagem:
                imagem = re.sub('http://anotherdomain.localhost:8000/po/tt/f/', 'http://s.glbimg.com/jo/g1/f/', imagem)
                imagem = "<img style='width: 45px; height: 45px; padding-right:5px; float:left;' src='%s' />" % resize(imagem,"60x45")
            else:
                imagem = ""
            
            title = materia.title
            
            materias += "<li style='float:left;'>%s <a href='%s'>%s</a></li>" % ( imagem, link, title)

    return HttpResponse(materias)

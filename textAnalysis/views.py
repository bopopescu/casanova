# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
import re
from globocore.estrutura.models import Folder
from lxml import html as lhtml
from estrategia_consulta import *
from textAnalysis.ner import *
from textAnalysis.utils import *



def alterar_path_imagens(imagem):
    if imagem:
        imagem = re.sub('http://localhost:8000/photo_static/',
                        'http://s.glbimg.com/jo/g1/f/',
                        imagem)
    return imagem

def extrair_dados_do_form(request):
    documento = {
        'titulo':'',
        'subtitulo':'',
        'texto':'',
        'permalink':'',
        'editorias':[],
        'entidades':[],
        'bold_text':[],
    }
    if request.POST.get('titulo'):
        documento['titulo']=request.POST.get('titulo')
    if request.POST.get('subtitulo'):
        documento['subtitulo']=request.POST.get('subtitulo')
    if request.POST.get('texto'):
        documento['texto']=request.POST.get('texto')
        html = lhtml.fromstring(documento['texto'].decode('utf-8'))
        documento['bold_text'] = [ h.text_content().strip() for h in html.cssselect('p strong')]
    if request.POST.get('entidades'):
        for entidade_id in request.POST.get('entidades').split(","):
            try:
                # documento['entidades'].append(Entidade.objects.get(id=entidade_id))
                pass
            except:
                pass
    if request.POST.get('editorias'):
        for editoria_id in request.POST.get('editorias').split(","):
            try:
                documento['editorias'].append(Folder.objects.get(uuid=editoria_id))
            except:
                pass
    if request.POST.get('permalink'):
        documento['permalink'] = request.POST.get('permalink')
    return documento if documento['titulo'] else []

def classify(request):
    materias = []
    words =[]
    selected = ""
    try:
        documento = extrair_dados_do_form(request) 
        if documento:
            # selected = request.POST.get('criterio') if request.POST.get('criterio') else 'todos'
            # if selected == 'todos':
            #     query, words = single_words_entities(documento)
            # else:
            #     query, words = words_relacionadas(selected)
            materiasSolr = relacionadas(doc=documento, comb='s', total=5)
            
            for (mSolr,v) in materiasSolr:
                idMateria = re.search('(?<=[a-z]/)[0-9]+', mSolr.identifier).group(0)
                try:
                    m = Materia.objects.get(id = idMateria)
                    m.thumbnail = alterar_path_imagens(m.obtem_caminho_absoluto_de_delivery_do_thumbnail_para_plantao())
                    materias += [m]
                except:
                    pass
        materias.sort(key=lambda m: m.ultima_publicacao)
        materias.reverse()
    except Exception:
        pass
    
    context = {'materias':materias, 'words':words, 'selected':selected,}
    return render_to_response('saibamais.html', context, RequestContext(request,context) )

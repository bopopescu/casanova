# coding: utf-8
import settings
import nltk
from django.template.loader import render_to_string
from globocore.materia.signals import materia_save
from globocore.signals import pre_extensible_area
from globocore.signals import ExtensibleArea

nltk.data.path = [settings.LOCAL_FILE()+"/textAnalysis/data/",]

def exibir_materias_recomendadas(sender, context, request, content, **kw):
    
    materia = context['form'].instance
    content.write(render_to_string('materias_recomendadas.html', {})) 
    
pre_extensible_area.connect(exibir_materias_recomendadas,
    sender=ExtensibleArea(area='materia-metadados', on='admin/materia/adicionar.html')
)
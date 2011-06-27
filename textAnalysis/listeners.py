# coding: utf-8
import os
from django.template.loader import render_to_string
from globocore.estrutura.signals import folder_save
from globocore.materia.signals import materia_save
from globocore.signals import pre_extensible_area
from globocore.signals import ExtensibleArea


# context is the folder! (fucking named parameters)
def generate_folder_cache(sender, context, request, **kwargs):
    context.generate_cache()

if os.environ.get('RUNNING_MODE', 'False').lower() != 'wsgi':
    folder_save.connect(generate_folder_cache)
    
def javascripts_adicionais(sender, context, request, content, **kw):
    content.write(render_to_string('admin/materia/materia/javascripts.html', {}))

pre_extensible_area.connect( javascripts_adicionais,
    sender=ExtensibleArea(area='javascript', on='admin/materia/adicionar.html')
)
    
def stylesheets_adicionais(sender, context, request, content, **kw):
    content.write(render_to_string('admin/materia/materia/stylesheets.html', {}))

pre_extensible_area.connect( stylesheets_adicionais,
    sender=ExtensibleArea(area='css', on='admin/materia/adicionar.html')
)



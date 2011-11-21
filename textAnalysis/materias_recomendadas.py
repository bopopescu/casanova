# coding: utf-8
from django.template.loader import render_to_string
from globocore.materia.signals import materia_save
from globocore.signals import pre_extensible_area
from globocore.signals import ExtensibleArea

def exibir_materias_recomendadas(sender, context, request, content, **kw):
    
    materia = context['form'].instance
    # input_title = '<input type="text" id="id_title" name="title" value="%s" maxlength="66">' % (materia.title or '')
    # input_description = '<input type="text" id="id_description" name="description" value="%s" maxlength="160">' % (materia.description or '')
    content.write(render_to_string('materias_recomendadas.html', {})) 
    
pre_extensible_area.connect(exibir_materias_recomendadas,
    sender=ExtensibleArea(area='materia-metadados', on='admin/materia/adicionar.html')
)

# def salvar_title_description_na_materia(sender, context, request, **kw):
#     materia = context['form'].instance
#     posted_title = request.POST.get('title')
#     posted_description = request.POST.get('description')
#     if posted_title:
#         materia.title = posted_title
#     else:
#         materia.title = None
#         
#     if posted_description:
#         materia.description = posted_description
#     else:
#         materia.description= None
# 
# materia_save.connect(salvar_title_description_na_materia)
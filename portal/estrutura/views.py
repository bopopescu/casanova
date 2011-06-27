# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
import datetime
from estrutura.models import Site, Elemento, Instancia
from django.db import models

def site(request, site):
    now = datetime.datetime.now()
    
    try:
        f = Site.objects.get(nome=site)
    except:
        raise Site.DoesNotExist('Este site <<%s>> nao esta cadastrado' % site)

    # to render a template you can do this way

    template = f.template.__unicode__().split('/')[-1]
    t = get_template(template)
    c = Context({"time":now,"site": site})
        

    from django.conf import settings
    ordem = 0
    for counter,node in enumerate(t.nodelist):
        for app in settings.INSTALLED_APPS:
            modulo = app.split('.')[-1]
            elemento = '<Variable Node: %s>' % modulo
            if node.__str__() == elemento:
                try:
                    e = Elemento.objects.get(nome=modulo)
                    ordem += 1
                except:
                    raise Elemento.DoesNotExist('O elemento <<%s>> nao esta cadastrado para o site <<%s>>' %  (modulo, site))

                try:
                    i = Instancia.objects.filter(elemento=e,ordem=ordem)
                    i = i[0]
                except:
                	pass
                    #raise Instancia.DoesNotExist('O elemento <<%s>> nao tem uma instancia cadastrada para a posicao<<%s>> no site <<%s>>' %  (modulo, ordem, site))

                """
                import httplib, simplejson
                conn = httplib.HTTPConnection("localhost" , "8001")
                h = {"Content-type": "application/json","Accept": "text/plain"}
                
                conn.request("GET", i.instancia.__str__(), headers=h)
                response = conn.getresponse()
                c = Context({"boxtexto":eval(response.read()),})
                conn.close()
                """

                obj = ""
                for item in models.get_app("estrutura").models.get_models():
                    if str(item).split(".")[-1].replace("'>","").lower() == e.nome:
                        obj = item
                
                dados = ""
                try:
                    dados = obj().get_instance(i.instancia)
                    c = Context({modulo: dados,})
                    # pega a template do elemento
                    template = e.template.__unicode__().split('/')[-1]
                    html = get_template(template)
                    t.nodelist[counter] = html.render(c)                    
                except:
                    pass
    
    c = Context({"time":now,"site": site})
    html = t.render(c)

    return HttpResponse(html)
    
    # or this way with shortcut render_to_response
    #return render_to_response('current_time.html',{"time":now})
    
def edit(request, site):
    now = datetime.datetime.now()
    
    try:
        f = Site.objects.get(nome=site)
    except:
        raise Site.DoesNotExist('Este site <<%s>> nao esta cadastrado' % site)

    # to render a template you can do this way

    template = f.template.__unicode__().split('/')[-1]
    t = get_template(template)
    c = Context({"time":now,"site": site})
        

    from django.conf import settings
    ordem = 0
    for counter,node in enumerate(t.nodelist):
        for app in settings.INSTALLED_APPS:
            modulo = app.split('.')[-1]
            elemento = '<Variable Node: %s>' % modulo
            if node.__str__() == elemento:
                try:
                    e = Elemento.objects.get(nome=modulo)
                    ordem += 1
                except:
                    raise Elemento.DoesNotExist('O elemento <<%s>> nao esta cadastrado para o site <<%s>>' %  (modulo, site))

                try:
                    i = Instancia.objects.filter(elemento=e,ordem=ordem)
                    i = i[0]
                except:
                	pass
                    #raise Instancia.DoesNotExist('O elemento <<%s>> nao tem uma instancia cadastrada para a posicao<<%s>> no site <<%s>>' %  (modulo, ordem, site))

                """
                import httplib, simplejson
                conn = httplib.HTTPConnection("localhost" , "8001")
                h = {"Content-type": "application/json","Accept": "text/plain"}
                
                conn.request("GET", i.instancia.__str__(), headers=h)
                response = conn.getresponse()
                c = Context({"boxtexto":eval(response.read()),})
                conn.close()
                """

                obj = ""
                for item in models.get_app("estrutura").models.get_models():
                    if str(item).split(".")[-1].replace("'>","").lower() == e.nome:
                        obj = item
                
                dados = ""
                template = e.template.__unicode__().split('/')[-1]
                html = get_template(template)
                try:
                    dados = obj().get_instance(i.instancia)
                    c = Context({modulo: dados,})
                    # pega a template do elemento
                    edit = """<div style='background-color: white !important; float: left;'>
                    		<div id='comandos' style='width: 100%; position: relative;'>
                    		<a style='float: right;' href=/portal/instancia/""" + site + "/"+ modulo + "/" + i.instancia+ "/"+ str(ordem) + """/delete>
                    			<img src='/portal/media/img/icon_deletelink.gif' /></a>
                    		</div>""" 
                except:
                	c = Context({modulo: "",})
                	edit = """<div style='background-color: #eee !important; float: left;'>
                    		<div id='comandos' style='width: 100%; position: relative;'>
                    		<a style='float: right;' href=/portal/instancia/""" + site + "/"+ modulo + "/"+ str(ordem) +  """/add>
                    			<img src='/portal/media/img/icon_addlink.gif' /></a>
                    		</div>"""

               	t.nodelist[counter] = edit                    
               	t.nodelist[counter] += html.render(c)                    
               	t.nodelist[counter] += "</div>"

    c = Context({"time":now,"site": site})
    html = t.render(c)

    return HttpResponse(html)
    
    # or this way with shortcut render_to_response
    #return render_to_response('current_time.html',{"time":now})
    
    
    
def add(request, modulo, site, ordem):
    obj = ""
    for item in models.get_app("estrutura").models.get_models():
    	if str(item).split(".")[-1].replace("'>","").lower() == modulo:
            obj = item
    dados = obj.objects.all()
    context = Context({
    	'site': site,
        'ordem': ordem,
        'instancias': dados,
        'elemento': modulo,
    })
    return render_to_response("instancia/add.html", context)

def save(request, site, modulo, instancia,ordem):
	f = Site.objects.get(nome=site)
	e = Elemento.objects.get(nome=modulo, site=f)
	Instancia.objects.create(elemento=e,instancia=instancia,ordem=ordem)
	return HttpResponseRedirect("/portal/edit/%s.html" % site)

def delete(request, modulo, site, instancia, ordem):
	i = Instancia.objects.filter(elemento__nome=modulo,instancia=instancia, ordem=ordem)
	i.delete()
	return HttpResponseRedirect("/portal/edit/%s.html" % site)


# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from globocore.materia.models import Materia
from django.conf import settings
import re
from textAnalysis.analytics import Feed 
from textAnalysis.models import Analytics


from testutils.database_cleaner import DatabaseCleaner

def remove_host(url):
    return re.sub(settings.BASE_URL,
                    "",
                    url)

def change_host(url):
    return re.sub('http://www.techtudo.com.br',
                    settings.BASE_URL,
                    url)
                    
class Command(BaseCommand): 
    
    def handle(self, *args, **options):
        # Analytics.objects.all().delete()
        
        total = 5000
        materias = Materia.objects.filter(corpo__icontains='saibamais')[:total]
        # materias = [Materia.objects.get(id=335)]
        i = 0
        analitycs = Feed()        
        for m in materias:
            try:
                jabaixado = Analytics.objects.filter(destino=m.permalink)
                if not jabaixado:
                    paginas = analitycs.get_paginas(m)
                    pageviews=0
                    for pagina in paginas:
                        try:
                            mr = Materia.objects.get(permalink=pagina.get_object('ga:previousPagePath').value)
                            Analytics.objects.create(origem=pagina.get_object('ga:previousPagePath').value,
                                                    destino=m.permalink,
                                                    pageviews=pagina.get_object('ga:pageviews').value)
                            pageviews += int(pagina.get_object('ga:pageviews').value)
                        except Exception, e:
                            pass
                i += 1
                print i, pageviews 
            except:
                print "materia nao encontrada"

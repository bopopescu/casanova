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
from django.conf import settings
import itertools

class Command(BaseCommand): 

    
    def handle(self, *args, **options):
        import time
        inicio = time.time()
        
        settings.CACHE = True

        materias = Materia.objects.filter(status='T')

        relacionadas = {}

        for m in materias:
            html = lhtml.fromstring(m.corpo.decode('utf-8'))
            rel = [ h.attrib['href'].lower() for h in html.cssselect('.saibamais ul li a')]
            for r in rel:
                if relacionadas.has_key(r):
                    relacionadas[r]+=1
                else:
                    relacionadas[r]=1
        
        for c in sorted_dict_by_value(relacionadas)[:10]:
            print c

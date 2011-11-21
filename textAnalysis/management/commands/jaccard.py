# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from globocore.materia.models import Materia
from django.db.models import Sum
from textAnalysis.models import Analytics

class Command(BaseCommand): 
    
    def handle(self, *args, **options):
        materias = Analytics.objects.values('destino').distinct()[:10]
        for m in materias:
            origens = Analytics.objects.filter(destino=m['destino']).exclude(origem=m['destino'])
            A = origens.aggregate(Sum('pageviews')).get('pageviews__sum')
            if not A:
                A=0
            
            jaccardMax = 0
            materia = ""
            for mm in origens:
                AB = mm.pageviews
                B = Analytics.objects.filter(destino=mm.origem).exclude(origem=mm.origem).aggregate(Sum('pageviews')).get('pageviews__sum')
                if not B:
                    B=0
                jaccard = round(AB*1.0 /(A+B-AB),2)
                
                if jaccardMax < jaccard:
                    jaccardMax = jaccard
                    materia = mm.origem
                
            print "DE:%s\nPARA:%s\n%s" % (materia, m['destino'], jaccardMax)

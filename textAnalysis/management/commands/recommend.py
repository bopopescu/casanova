# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import nltk
from random import *
from textAnalysis.models import *
from textAnalysis import recommendations
from numpy import * 
from django.db.models import Count

def time_features(atletas): 
    features = {}
    for atleta, pontuacao in atletas:
        if pontuacao > 2:
            features[atleta] = True 
    return features

def getPontos(id, rodada):
    atleta = AtletaRodada.objects.get(atleta_id = id, rodada_id = rodada)
    return atleta.pontos_num 

def getAtletas():
    times = {}
    for time in TimeRodada.objects.filter(rodada_id = 1)[:100]:
        atletas = TimeAtleta.objects.filter(time_id = time.time_id).values('atleta_id').annotate(Count('atleta_id'))
        times[int(time.time_id)]={}
        for atleta in atletas:
            times[time.time_id][atleta['atleta_id']]=float(atleta['atleta_id__count'])
    return times

                    
class Command(BaseCommand): 
    
    def handle(self, *args, **options):
        atletas = getAtletas()
        print recommendations.getRecommendations(atletas, atletas.keys()[0])[:12]      
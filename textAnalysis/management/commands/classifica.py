# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import nltk
from random import *
from textAnalysis.models import *
from textAnalysis.perceptron import Perceptron
from numpy import * 

def time_features(atletas): 
    features = {}
    for atleta, pontuacao in atletas:
        if pontuacao > 2:
            features[atleta] = True 
    return features

def getPontos(id, rodada):
    atleta = AtletaRodada.objects.get(atleta_id = id, rodada_id = rodada)
    return atleta.pontos_num 

def getStatus(val):
    return "Bom" if val > 50 else "Ruim"
  
def getStatusBinario(val):
    return 1 if val > 50 else -1
          
def getTimesComPontuacaoDeAtleta():
    times = []
    for time in TimeRodada.objects.all()[:10]:
        atletas = TimeAtleta.objects.filter(rodada_id=time.rodada_id, time_id=time.time_id)
        times+= [([(atleta.atleta_id, getPontos(atleta.atleta_id,time.rodada_id)) for atleta in atletas],getStatus(time.pontos_num))]
    return times
    
def getTimesNumPy():
    times = []
    for time in TimeRodada.objects.all()[:50]:
        atletas = TimeAtleta.objects.filter(rodada_id=time.rodada_id, time_id=time.time_id)
        times+= [(array([atleta.atleta_id for atleta in atletas]),getStatusBinario(time.pontos_num))]
    return times

def getTimesNumPyForSVM():
    times = []
    for time in TimeRodada.objects.all()[:100]:
        atletas = TimeAtleta.objects.filter(rodada_id=time.rodada_id, time_id=time.time_id)
        times+= [([atleta.atleta_id for atleta in atletas],getStatusBinario(time.pontos_num))]
    return times

                    
class Command(BaseCommand): 
    
    def handle(self, *args, **options):
        
        # NaiveBayes
        # times = getTimesComPontuacaoDeAtleta()
        # shuffle(times)
        # featuresets = [(time_features(atletas), pontos) for (atletas,pontos) in times]
        # train_set, test_set = featuresets[:len(times)*80/100], featuresets[len(times)*80/100:]
        # classificador = nltk.NaiveBayesClassifier.train(train_set)
        # print 'accuracy: ', nltk.classify.util.accuracy(classificador, test_set)
        # print classificador.prob_classify(time_features(times[0][0])).prob('Bom')


        # Perceptron
        # times = getTimesNumPy()
        # shuffle(times)
        # train, test = times[:len(times)*80/100], times[len(times)*80/100:]
        # kwargs = dict(event_size=len(times[0][0]), outcome_size=len(times))  
        # p = Perceptron(**kwargs)
        # 
        # for time in train:
        #     event, outcome = time
        #     p.learn(event, outcome)
        # 
        # correct = 0
        # 
        # for time in test:
        #     event, outcome = time
        #     prediction, _ = p.classify(event)
        #     if prediction is outcome:
        #         correct += 1
        # 
        # print '%f' % (correct*1.0/len(times))
        
        times = getTimesNumPyForSVM()
        shuffle(times)
        train, test = times[:len(times)*80/100], times[len(times)*80/100:]
        
        from libsvm.svm import *
        from libsvm.svmutil import *
        
        x = [b for (a,b) in train]
        y = [a for (a,b) in train]
        # x = [1,-1]
        # y = [[1,0,1],[-1,0,-1]]
        
        prob = svm_problem(x,y)
        param = svm_parameter()
        param.kernel_type = LINEAR
        param.C = 10

        m = svm_train(prob, param)
        
        correct = 0
        
        for (y,x) in test:
            x0, max_idx = gen_svm_nodearray(y)
            prediction = libsvm.svm_predict(m,x0)
            # print prediction, x
            if int(prediction) is x:
                correct += 1
        
        print '%f' % (correct*1.0/len(test))
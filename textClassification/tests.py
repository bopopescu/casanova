# -*- coding: utf-8 -*-
from unittest import TestCase
import time
from classifier import MultiBinaryClassifier
from models import materia_corpus
from datetime import *
from features import document_features_single
import random
import nltk

"""
f = Folder.objects.filter(relatedfolder__materia__isnull=False).annotate(qtd=models.Count('id')).order_by('-qtd')
for f in folder:
    m = Materia.objects.filter(relatedfolder_set__is_primary=True, relatedfolder_set__folder=f)
    if len(m) >= 1000:
        print len(m), f.name
        
60631 Mundo
38557 G1
32409 Economia e Negócios
17247 Brasil
9783 São Paulo
9327 Pop & Arte
8364 Rio de Janeiro
6759 Política
7011 Tecnologia e Games
5175 Economia
5139 Jornal Nacional
4027 Bom Dia Brasil
3784 Concursos e Emprego
3469 Eleições 2010
2462 Minas Gerais
2118 Vestibular e Educação
1558 Ciência e Saúde
2242 Jornal Hoje
2122 Planeta Bizarro
1566 Auto Esporte
1708 Jornal da Globo
"""


class MateriaModelTest(TestCase):
     def test_verifica_que_a_materia_e_da_editoria_certa(self):
        n=datetime.now()
        documents = []
        labels = ["Ciência e Saúde","Auto Esporte","Economia e Negócios","Eleições 2010","Tecnologia e Games", "Brasil"]
        
        for l in labels:
            documents += materia_corpus(l,total=10)

        random.shuffle(documents)
        featuresets = [(document_features_single(d), c) for (d,c) in documents]
        train_set, test_set = featuresets[:len(documents)*80/100], featuresets[len(documents)*80/100:]
        
        # classificador = nltk.NaiveBayesClassifier.train(train_set)
        classificador = MultiBinaryClassifier().train(labels, train_set)
        errors =0
        for d,c in test_set:
            probs_label = ''
            probs_valor = 0
            for l in labels:
                prob_temp = classificador[l].prob_classify(document_features_single(d)).prob(l)
                if prob_temp >= probs_valor:
                    probs_valor = prob_temp
                    probs_label = l
                # print probs_label, probs_valor
            if probs_label != c:
                # print 'Probabilidade de ser %s, quando a real é %s' % (probs_label,c)
                errors += 1
        print "total de materias testadas", len(test_set), "total de erros", errors 

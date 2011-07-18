# -*- coding: utf-8 -*-
# import collections 
# from nltk import metrics
# from nltk.probability import FreqDist, ConditionalFreqDist
# import re, htmlentitydefs
# import os
# from datetime import *
# from models import Dicionario
# import nltk
# from nltk.metrics import BigramAssocMeasures


def document_features_single(document): 
    features = {}
    for word in document:
        features[word] = True
    return features

# def best_word_feats(document):
#     features = dict([(word, True) for word in set(document) if word in bestwords])
#     return features
# 
# def document_mostinformativefeatures(document):
#     features = dict([(word, True) for word in set(document) if word in mostinformativewords])
#     return features
# 
# def document_features_wordfreq(document): 
#     features = {}
#     wordfreq = nltk.FreqDist(w.lower() for w in document if w not in stopwords)
#     wordfreq = set(wordfreq.keys()[:3000])
#     for word in wordfreq:
#         features[word] = True
#     return features
#     
# def document_high_information_word(document):
#     features = {} 
#     for word in document:
#         if word in high_information_word:
#             features[word] = True
#     return features        
# 
# def document_features_single_set_sem_stop(document): 
#     features = {}
#     for word in set(document):
#         if word not in stopwords:
#             features[word] = True
#     return features
# 
# def best_bigram_word_feats(document):
#     bigram_finder = BigramCollocationFinder.from_words(best_word_feats(document))
#     score_fn=BigramAssocMeasures.chi_sq, n=200
#     bigrams = bigram_finder.nbest(score_fn, n)
#     features = dict([(bigram, True) for bigram in bigrams])
#     return features
#     
# def document_features_bigrams(document): 
#     features = {}        
#     filter_stops = lambda w: len(w) < 3 or w in stopwords
#     bigram_finder = BigramCollocationFinder.from_words(document) 
#     bigram_finder.apply_word_filter(filter_stops)
#     score_fn=BigramAssocMeasures.chi_sq
#     n=200
#     bigrams = bigram_finder.nbest(score_fn, n)
#     # bigrams = bigram_finder.nbest(BigramAssocMeasures.likelihood_ratio, 4)
#     for bigram in bigrams:
#         features[bigram] = True
#     return features
#     
# def document_features_trigrams(document): 
#     features = {}        
#     trigram_finder = TrigramCollocationFinder.from_words(document)
#     trigram_finder.apply_freq_filter(3)
#     score_fn=TrigramAssocMeasures.chi_sq
#     n=200
#     trigrams = trigram_finder.nbest(score_fn, n)
#     for trigram in trigrams:
#         features[trigram] = True
#     return features
# 
# 
# def buildbestwordfeats(corpus,stopwords):
#     try:
#         bestwords = set(Dicionario.objects.get(nome='bestwordfeats').valor.split())
#     except Dicionario.DoesNotExist:
#         word_fd = FreqDist()
#         label_word_fd = ConditionalFreqDist()
#         categorias=set()
#         total_word_count=0
#         word_scores = {}
#         
#         for d in corpus:
#             words = set(d[0])
#             categoria = d[1]
#             for word in words:
#                 if word not in stopwords:
#                     word_fd.inc(word.lower())
#                     label_word_fd[categoria].inc(word.lower())
#                     total_word_count += 1
#             categorias.add(categoria) 
# 
#         for word, freq in word_fd.iteritems():
#             word_scores[word]=0
#             for c in categorias: 
#                 word_scores[word] += BigramAssocMeasures.chi_sq(label_word_fd[c][word],(freq, label_word_fd[c].N()), total_word_count)
# 
#         best = sorted(word_scores.iteritems(), key=lambda (w,s): s, reverse=True)[:10000]
#         bestwords = set([w for w, s in best])
#         Dicionario.objects.create(nome='bestwordfeats', valor=" ".join(bestwords))        
#     return bestwords
# 
# def buildHighInformationWord(corpus, stopwords):
#     try:
#         high_information_word = set(Dicionario.objects.get(nome='highinformationword').valor.split())
#     except Dicionario.DoesNotExist:
#         all_words = words(corpus)
#         all_words = nltk.FreqDist(w.lower() for w in all_words if w not in stopwords)
#         high_information_word = set(all_words.keys()[:10000])
#         Dicionario.objects.create(nome='highinformationword', valor=" ".join(high_information_word))        
#     return high_information_word
#             
    
# def buildStopWords():
#     try:
#         words = Dicionario.objects.get(nome='stopwords').valor
#     except Dicionario.DoesNotExist:
#         stwordfile = os.path.abspath(os.path.dirname('.'))+"/textClassification/stopwords.txt"  
#         words = open(stwordfile,'r').read()
#         Dicionario.objects.create(nome='stopwords', valor=words)
#     ignored_words = words.split()
#     return set(ignored_words)
#         

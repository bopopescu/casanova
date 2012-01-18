# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from globocore.materia.models import Materia
from textAnalysis.estrategia_consulta import *
from textAnalysis.utils import *


                    
class Command(BaseCommand): 
    
    def handle(self, *args, **options):
        big_text = ""
        ngram = " ".join(args)
        query = "(%s)" % ngram
        materiasSolr = querySolr(query, total=100)
        for materiaSolr in materiasSolr:
            mSolr = MateriaDoSolr(materiaSolr)
            big_text += (" " + mSolr.body) 
        words = tf(big_text)
        words = sorted_dict_by_value(words)
        print "\n********unigrams\n"
        # for (word,fq) in words[:11]:
        #     if not word == ngram:
        #         print word
        _unigrams = better_words(words)

        words = bag_of_words(big_text, remove_stopwords=True, remove_verbos=False)
        words = bigrams(words)
        print "\n*******bigrams\n"
        # for (word,fq) in words[:11]:
        #     if not " ".join(word) == ngram:
        #         print " ".join(word)
        _bigrams = better_words(words)

        words = bag_of_words(big_text, remove_stopwords=False)
        words = trigrams(words)
        print "\n******trigrams\n"
        # for (word,fq) in words[:11]:
        #     if not " ".join(word) == ngram:
        #         print " ".join(word)
        _trigrams = better_words(words)
        
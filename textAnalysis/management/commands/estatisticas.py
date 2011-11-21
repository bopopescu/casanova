# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from globocore.materia.models import Materia
from textAnalysis.utils import *
                        
class Command(BaseCommand): 
    
    def handle(self, *args, **options):
        id = args[0]
        materia = Materia.objects.get(id=id)
        text = "%s %s %s" % (materia.titulo,materia.subtitulo,materia.corpo)

        words = tf(text)
        words = sorted_dict_by_value(words)
        print "unigrams"
        words = better_words(words)
        print words
        print "\n"
        
        words = bag_of_words(text, remove_stopwords=True)
        words = bigrams(words)
        print "bigrams"
        words = better_words(words)
        print words
        print "\n"

        words = bag_of_words(text)
        words = trigrams(words)
        print "trigrams"
        words = better_words(words)
        print words
        print "\n"
        
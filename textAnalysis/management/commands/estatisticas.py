# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from globocore.materia.models import Materia
from textAnalysis.utils import *
from textAnalysis.ner import *
from textAnalysis.management.commands import nerbayes

class Command(BaseCommand): 
    
    def handle(self, *args, **options):
        if args:
            id = args[0]
            materia = Materia.objects.get(id=id)
            text = "%s. %s. %s" % (materia.titulo,materia.subtitulo,extract_text_from_p(materia.corpo))
        else:
            text = """
            A Polícia Federal informou que foi instaurado um inquérito, após uma denúncia para o DNPM 
            de crime de usurpação de bens públicos decorrentes da exploração ilegal de pedras-sabão.
            Rogério Castro, responsável pela agência de recursos naturais do Ibama que atuava em Minas Gerais, 
            foi destituído do cargo. 
            """

        # words = tf(text)
        # words = sorted_dict_by_value(words)
        # print "unigrams"
        # words = better_words(words)
        # print words
        # print "\n"
        # _text += " ".join(words)+ " "
        # 
        # words = bag_of_words(text, remove_stopwords=True)
        # words = bigrams(words)
        # print "bigrams"
        # words = better_words(words)
        # print words
        # print "\n"
        # _text += " ".join(words)+ " "
        # 
        # words = bag_of_words(text)
        # words = trigrams(words)
        # print "trigrams"
        # words = better_words(words)
        # print words
        # print "\n"
        # _text += " ".join(words)+ " "
        
        methods = []
        # methods.append(ltask)
        # methods.append(yahoo)
        # methods.append(nltk)
        # methods.append(zemanta)
        methods.append(my_fastercts)
        
        for method in methods: 
            print "\n", method.func_name 
            ner = NER(method)
            entidades = ner.processa(text)
            for entidade in entidades:
                print entidade

        

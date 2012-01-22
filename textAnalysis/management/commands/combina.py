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

class Command(BaseCommand): 
    
    def handle(self, *args, **options):

        sequential_constructors = {
        	's': affix_constructor,
        	'h': ngram_constructor(nltk.tag.UnigramTagger),
            'c': ngram_constructor(nltk.tag.BigramTagger),
            'e': ngram_constructor(nltk.tag.TrigramTagger)
        }

        if args.sequential:
        	for c in args.sequential:
        		if c not in sequential_constructors:
        			raise NotImplementedError('%s is not a valid sequential backoff tagger' % c)

        		constructor = sequential_constructors[c]
        		tagger = constructor(train_sents, backoff=tagger)
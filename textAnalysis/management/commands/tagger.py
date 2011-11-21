# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from globocore.materia.models import Materia
from textAnalysis.utils import *


                    
class Command(BaseCommand): 
    
    def handle(self, *args, **options):
        tag = args[0]
        tagger = nltk.data.load("taggers/mac_morpho_aubt.pickle")
        print tagger.tag([tag])
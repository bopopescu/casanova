#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Import system modules
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

# Import local modules
from globocore.materia.models import Materia



class Command(BaseCommand):
    option_list = BaseCommand.option_list
    help = "Executa a consolidacao"
    args = '[]'

    def indexar_materias(self, materias):
    	pass

    def materia_to_solr(self, materia):
    	return {}

    def handle(self, *argss, **options):
        print "======================"
        print "Iniciando Consolidacao"
        print "======================"

        materias = []
        for materia in Materia.objects.all():
        	materias.append(materias_to_solr(materia))

        	if len(materias_to_solr) > 1000:
        		self.indexar_materias(materias)
        		materias_to_solr = []



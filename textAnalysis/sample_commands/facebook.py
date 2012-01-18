# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from globocore.materia.models import Materia
from textAnalysis.facebook import *


class Command(BaseCommand): 
    
    def handle(self, *args, **options):
        materias = Materia.objects.all().order_by('-criado_em')[:50]
        for m in materias:
            like = LikesDaMateria(m)
            dados = like.html()
            print dados['total_count'], m.titulo
#!/usr/bin/python
from globocore.materia.models import Materia
from textAnalysis.facebook import *

m = Materia.objects.all()[0]

like = LikesDaMateria(m)
print like.html()

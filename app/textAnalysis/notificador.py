# -*- coding: utf-8 -*-
from testutils.test_case import TestCaseTechTudo
from globocore.materia.models import Materia
import time

class TestCarga(TestCaseTechTudo):
            
    def testNotificaSolr(self):
        for materia in Materia.objects.all():
            if materia.id > 152870:
                materia.notifica_barramento("publicar")
                print ""
                print "materia %s publicada." % materia.id
                time.sleep(1)
            

# -*- coding: utf-8 -*-
from testutils.test_case import TestCaseTechTudo
from testutils.database_cleaner import DatabaseCleaner
from extensoescore.tests.utils import *
from textAnalysis.management.commands import notifica

class NotificaTest(TestCaseTechTudo):
    
    def after(self):
        pass
    
    def before(self):
        DatabaseCleaner.clean_solr()
        self.editoria = create_folder(slug='artigos',name='artigos')
 
    def test_notifica(self):
        i=1
        textos = ['a casa da moeda', 'o gato de botas', 'a rainha branca']
        for texto in textos:
            m = Materia.objects.create(slug="materia-%s"%i, titulo="materia %s"%i, corpo=texto, status='P', permalink="/noticias/materia-%s"%i)
            RelatedFolder.objects.create(materia=m,is_primary=True,folder=self.editoria)
            i+=1
        command = notifica.Command()
        command.handle()
        time.sleep(2)
        solr_connection = SolrConnection(settings.SOLRSERVER)
        consulta = solr_connection.query('publisher:Techtudo')
        solr_connection.close()
        
        assert len(consulta.results) == len(textos)
    

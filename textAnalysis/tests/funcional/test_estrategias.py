# -*- coding: utf-8 -*-
from testutils.test_case import TestCaseTechTudo
from testutils.database_cleaner import DatabaseCleaner
from extensoescore.tests.utils import *
from textAnalysis.estrategia_consulta import *
from django.http import HttpRequest
from entidade.tests.utils import criar_entidade
from datetime import datetime, timedelta


class EstrategiasTest(TestCaseTechTudo):
    
    def after(self):
        pass
    
    def before(self):
        DatabaseCleaner.clean_solr()
        self.editoria = create_folder(slug='artigos',name='artigos')
        
    def test_extract_entity(self):
        e = criar_entidade(slug='ipad', nome="Ipad")
        text = '<p>ipad é o tablet do sucesso</p>'
        assert e == extract_entity(text)


    def test_extract_entity_mais_usada(self):
        e1 = criar_entidade(slug='ipad', nome="Ipad")
        e2 = criar_entidade(slug='sony', nome="Sony")
        text = '<p>ipad é o tablet sony do sucesso sony</p>'
        assert e2 == extract_entity(text)
        
    def test_extract_entity_mais_usada_ngrams(self):
        e1 = criar_entidade(slug='ipad-3gs', nome="Ipad 3gs")
        e2 = criar_entidade(slug='ipad', nome="Ipad")
        e3 = criar_entidade(slug='sony', nome="Sony")
        text = '<p>ipad 3gs é o tablet sony do sucesso ipad 3gs</p>'
        assert e1 == extract_entity(text)
        
    def test_extract_entity_none(self):
        text = '<p>ipad 3gs é o tablet sony do sucesso ipad 3gs</p>'
        assert None == extract_entity(text)
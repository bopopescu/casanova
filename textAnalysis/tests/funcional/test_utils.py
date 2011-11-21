# -*- coding: utf-8 -*-
from testutils.test_case import TestCaseTechTudo
from textAnalysis.utils import *
from testutils.database_cleaner import DatabaseCleaner
from extensoescore.tests.utils import *
from entidade.tests.utils import criar_entidade


class UtilsTest(TestCaseTechTudo):
    
    def after(self):
        pass
    
    def before(self):
        DatabaseCleaner.clean_solr()
        self.editoria = create_folder(slug='artigos',name='artigos')
        
    def test_unescape(self):
        text = 'OL&#65;'
        assert unescape(text) == 'OLA'
        text = 'OL&#x;'
        assert unescape(text) == 'OL&#x;'
        text = 'OL&Aacute;'
        assert unescape(text) == 'OLÁ'
        text = 'OL&Aacurutte;'
        assert unescape(text) == 'OL&Aacurutte;'

    def test_clean(self):
        text = '<a href>teste de ol&aacute;</a>'
        assert clean(text) == 'teste de olá'
        
    def test_stopwords(self):
        words = stopwords()
        assert 'de' in words
        assert 'brasil' not in words

    def test_bigrams(self):
        words = ['congresso','nacional', 'brasileiro']
        bi = bigrams(words)
        assert (('congresso', 'nacional'), 1) in bi
        
    def test_trigrams(self):
        words = ['congresso','nacional', 'brasileiro']
        tri = trigrams(words)
        assert (('congresso', 'nacional', 'brasileiro'), 1) in tri

    def test_bag_of_words(texto):
        text = '<a href>teste de ol&aacute;</a>'
        words = bag_of_words(text)
        assert ['teste','de','olá'] == words
                
    def test_tf(self):
        text = '<p>teste de verificação de teste de ajuste</p>'
        words = tf(text)
        assert {u'teste': 2, u'ajuste': 1, u'verifica\xe7\xe3o': 1} == words

    def test_sorted_dict_by_value(self):
        text = '<p>teste de verificação de teste de ajuste</p>'
        words = tf(text)
        items = sorted_dict_by_value(words)
        assert [(u'teste', 2), (u'ajuste', 1), (u'verifica\xe7\xe3o', 1)] == items

    def test_all_words(self):
        tags={}
        tags1 = tf("o gato de botas")
        tags2 = tf("o gato fiel zatara")
        tags = all_words(tags1, tags)
        tags = all_words(tags2, tags)
        assert {u'gato': 2, u'botas': 1, u'fiel': 1,  u'zatara': 1,} == tags
     
    def test_vsm(self):
        vsm = VSM("dois textos iguais", "dois textos iguais")
        assert 1.0 == round(vsm,2)
        vsm = VSM("texto bem diferente", "carro para carvalho")
        assert 0 == round(vsm,2)

    def test_jaccard(self):
        jc = jaccard("dois textos iguais", "dois textos iguais")
        assert 1.0 == round(jc,2)
        jc = jaccard("texto bem diferente", "carro tal carvalho")
        assert round(jc,2) < 0.3

    def test_stemmer(self):
        from nltk.stem.rslp import RSLPStemmer
        lemmatizer = RSLPStemmer()
        text = 'policia'
        stem = lemmatizer.stem(text)
        assert stem == 'polic'

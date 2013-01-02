# -*- coding: utf-8 -*-
import StringIO
import pycurl
import logging
from django.conf import settings
import urllib, simplejson
from textAnalysis.utils import * 
from textAnalysis.management.commands import trainclassifier, newclassifier

_entities = entities()
classificador = loadClassifier()
# classificador2 = loadClassifier("classificador_texto")

def is_entity(tag):
    features = trainclassifier.features(tag)
    # print features, tag,  classificador.prob_classify(features).prob('sim')
    return True if classificador.prob_classify(features).prob('sim') > 0.80 else False    

def is_entity2(frase, tag):
    features = newclassifier.features(frase,tag)
    # print tag,  classificador.prob_classify(features).prob('sim')
    return True if classificador2.prob_classify(features).prob('sim') > 0.80 else False    


class HttpManeirao(object):
    def __init__(self,timeout=1):
        self.timeout = timeout
    def interna(self,url):
        return 'globoi.com' in url
    def config_proxy(self,curl,proxy):    
        if proxy:
            curl.setopt( pycurl.PROXY, proxy )
    def get(self,url, post=None):
        body = StringIO.StringIO()
        curl = pycurl.Curl() 
        curl.setopt( pycurl.URL, str(url) ) 
        # import pdb; pdb.set_trace();
        if post:            
            curl.setopt(pycurl.POST,1) 
            curl.setopt(pycurl.POSTFIELDS,post)
        curl.setopt( pycurl.WRITEFUNCTION, body.write ) 
        curl.setopt( pycurl.FOLLOWLOCATION, self.timeout ) 
        # curl.setopt( pycurl.TIMEOUT, self.timeout )
        try:
            curl.perform()
        except Exception, msg:
            print "erro!!!", url, msg
            logging.error("Nao foi possivel buscar [%s] - [%s]" % (url, msg))
            return None
        content = body.getvalue()
        body.close()
        return content

        
def html(url, dados):
    return HttpManeirao().get(url,urllib.urlencode(dados))
    

def ltask(text):
    dados = {}
    url = "http://api.ltasks.com/app/v0b/ner"
    dados['apikey'] = "b2c4cf5c-52d3-4fef-ac9b-67dbe6b5e52d"
    dados['text'] = text
    dados['output'] = "json"    
    response = html(url, dados)
    _entidades = []
    if response:
        itens = simplejson.loads(response)
        entidades = itens['value']['namedEntities']['namedEntity']
        for entidade in entidades:
            if entidade['type'] in ("PERSON", "PLACE", "ORGANIZATION"):
                _entidades += [entidade['text']]
    
    return _entidades 

def yahoo(text):
    dados = {}
    url = "http://search.yahooapis.com/ContentAnalysisService/V1/termExtraction"
    dados['appid'] = "TOYDGzfV34GRxsvf0M6.bhLJnPKekYwpY9x1kesdEh6o7yS35t7Zhf1KvrSjuNBjIBE_CSf8ww--"
    dados['context'] = text
    dados['output'] = "json"
    dados['query'] = ''
    response = html(url, dados)
    _entidades = []
    if response:
        itens = simplejson.loads(response)
        entidades = itens['ResultSet']['Result']
        for entidade in entidades:
            _entidades += [entidade]
    return _entidades 
        
def zemanta(text):
    dados = {}
    url = "http://api.zemanta.com/services/rest/0.0/"
    dados['method'] = "zemanta.suggest"
    dados['api_key'] = "w6dfcmc4dxmilh1adukwaqop"
    dados['text'] = text
    dados['return_categories'] = "dmoz"
    dados['format'] = "json"
    response = html(url, dados)
    _entidades = []
    if response:
        itens = simplejson.loads(response)
        entidades = itens['keywords']
        for entidade in entidades:
            _entidades += [entidade['name']]
    return _entidades
        
def nltk(text):
    dados = {}
    url = "http://text-processing.com/api/phrases/"
    dados['language'] = "english"
    dados['text'] = text
    response = html(url, dados)
    _entidades = []
    if response:
        itens = simplejson.loads(response)
        for entidade in ['PERSON','LOCATION','ORGANIZATION']:
            if entidade in itens.keys():
                _entidades += [dado for dado in itens[entidade]]
    return _entidades


def fastercts(text):
    words = []
    words = extrai_ngram(text)
    return [word for (word,i,f) in words if word in _entities]
    
def my_fastercts(text):
    words = []
    words = extrai_ngram(text)
    words = [(word,i,f) for (word,i,f) in words if is_entity(word) and is_valid_ngram(word)]
    words = sorted(words, key=lambda s: len(s[0].split()), reverse=True)

    # ws=[]
    # if words:
    #     ws = [words[0]] 
    #     inside = False
    # 
    # for (word,i,f) in words:
    #     inside = False
    #     for (w,s,e) in ws:
    #         if word in w:
    #             if (i>=s and f<=e) or word==w:
    #                 inside = True
    #                 break
    #     if not inside:
    #         ws.append((word,i,f))    

    return [w for w,i,f in words]

    
def my_fastercts2(text):
    words = []
    words = extrai_ngram(text)
    sentenca =  " ".join(clean(text).split())
    words = [(word,i,f) for (word,i,f) in words if is_entity2(sentenca,word) and is_valid_ngram(word)]
    words = sorted(words, key=lambda s: len(s[0].split()), reverse=True)
    
    # ws=[]
    # if words:
    #     ws = [words[0]] 
    #     inside = False
    # 
    # for (word,i,f) in words:
    #     inside = False
    #     for (w,s,e) in ws:
    #         if word in w:
    #             if (i>=s and f<=e) or word==w:
    #                 inside = True
    #                 break
    #     if not inside:
    #         ws.append((word,i,f))    

    return [w for w,i,f in words]


class NER(object):
    def __init__(self, func=None):
        if func:
             self.processa = func
             
    def processa(self, text):
        return None

    # def recortar_itens(self,response):
    #     itens = simplejson.loads(response)
    #     entidades = itens['value']['namedEntities']['namedEntity']
    #     _entidades = []
    #     for entidade in entidades:
    #         print entidade['text'], entidade['type']
    # 
    #         entidade['text'] = re.sub(r"[.,_+=)(*&\^/?><:;!@#$%\]\}\-\[\{\"\'\~\`]", r'', entidade['text'])
    #         if entidade['type'] in ("PERSON", "PLACE", "ORGANIZATION"):
    #             if not (entidade['text'],entidade['type']) in _entidades:
    #                 if is_valid_unigram(entidade['text']):
    #                     _entidades+= [(entidade['text'],entidade['type'])] 
    #     return _entidades 



        

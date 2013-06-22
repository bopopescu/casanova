from globocore.common.solr import SolrConnection
from django.conf import settings
from textAnalysis.utils import *
import itertools
import datetime
from globocore.materia.models import Materia
from textAnalysis.materia_do_solr import MateriaDoSolr 
from textAnalysis.ner import *  

from textAnalysis.cache import *
cache = CachedDict()


def periodo(doc, time=2000):
    if doc['permalink']:
        m = Materia.objects.get(permalink=doc['permalink'])
        dt_inicio = m.primeira_publicacao-datetime.timedelta(days=time)
        dt_fim = m.primeira_publicacao #+datetime.timedelta(days=time)
    else:
        dt_inicio = datetime.datetime.now()-datetime.timedelta(days=time)
        dt_fim = datetime.datetime.now()        
    periodo = " issued:[%sT00:00:00.000Z TO %sT23:59:59.000Z]" % (datetime.date.isoformat(dt_inicio), datetime.date.isoformat(dt_fim))
    return periodo 


class Estrategia:

    def __init__(self, func=None):
        if func:
             self.query = func

    def query(self, args=None):
        return []

    
def querySolr(words, editorias, total=50):
    materias = []
    solr_connection = SolrConnection(settings.SOLRSERVER)
    if not words:
        return materias
    query = [' OR '.join('(%s)' % tag for tag in words)]
    if editorias:
        query = ['((%s) %s)' % (query[0], editorias)]
    query = query[0].encode('utf-8')
    try:
        consulta = solr_connection.query(query + " isIssued:true type:texto publisher:G1 ", wt='json', start=0, rows=total,
                                   indent='on', sort='score desc, issued', sort_order='desc', )
        # print "materias ==>", len(consulta.results), query
        if consulta.results:
            # materias += [(materia, materia['score'] ) for materia in consulta.results]
            materias += consulta.results
    except Exception, e:
        print str(e)
        print "deu pau na query", query
        pass
    solr_connection.close()
    return materias


def _editorias(doc):
    queries=""
    editorias = doc['editorias']
    if editorias: 
        queries = [' OR '.join("editoria_principal_s:\"%s\" " % editoria.name for editoria in editorias)]
        queries = ' AND (%s) ' % queries[0]
    return queries


def b_ngram_freq(doc):
    text = "%s. %s. %s" % (doc['titulo'],doc['subtitulo'], extract_text_from_p(doc['texto']))    
    return ngram_frequency(text,n=2)

def t_ngram_freq(doc):
    text = "%s. %s. %s" % (doc['titulo'],doc['subtitulo'], extract_text_from_p(doc['texto']))    
    return ngram_frequency(text,n=3)

def caption(doc):
    text = ".".join(doc['caption'])    
    return ngram_frequency(text)

def html_tags(doc):
    text = ".".join(doc['html_tags'])   
    return ngram_frequency(text)
     
def u_ngram_freq(doc):
    text = "%s. %s. %s" % (doc['titulo'],doc['subtitulo'], extract_text_from_p(doc['texto']))    
    text = clean(text, separador=' ')
    words = text.split()
    stop = stopwords()
    tags={}
    for word in words:
        if word not in stop and len(word)>2 and not word.isdigit():
            if tags.has_key(word):
                tags[word]+=1
            else:
                tags[word]=1
    _unigrams = sorted_dict_by_value(tags)
    _unigrams = better_words(_unigrams) 
    return _unigrams

def my_entities(doc):
    text = "%s. %s. %s" % (doc['titulo'],doc['subtitulo'], extract_text_from_p(doc['texto']))
    return my_fastercts(text)

features = {
  't': t_ngram_freq,
  'b': b_ngram_freq,
  'u': u_ngram_freq,
  'h': html_tags,
  'c': caption,
  'e': my_entities,
}

def _combina(comb, doc):
    text = "%s. %s. %s" % (doc['titulo'],doc['subtitulo'], extract_text_from_p(doc['texto']))
    words = []
    if comb:
    	for c in comb:
    		if c not in features:
    			raise NotImplementedError('%s is not a valid sequential backoff tagger' % c)
    		constructor = features[c]
    		chave = "%s_%s" % (c, doc['permalink'])
    		if cache.get(chave):
    		    _words = cache.get(chave)
    		else:
    		    _words = constructor(doc)
    		    cache.set(chave,_words)
            # print _words
    		for word in _words:
    		    if word not in words:
    		        words.append(word)
    
    return words

def relacionadas(doc, comb='s',total=5, similaridade=True):
    materias = []
    words = _combina(comb,doc)
    editorias = _editorias(doc)
    materiasSolr = querySolr(words, editorias, total=25)
    for materiaSolr in materiasSolr:
        mSolr = MateriaDoSolr(materiaSolr)
        peso = materiaSolr['score']
        try:
            # remove a propria materia da lista 
            if doc['titulo'] != mSolr.title:
                # nao coloca materias duplicadas na lista
                if not any([m.title == mSolr.title for (m,vsm) in materias]):
                    vsm = 1
                    if similaridade:
                        chave = "%s_%s" % (doc['permalink'], mSolr.identifier)
                        if cache.get(chave):
                            vsm = cache.get(chave)
                        else:
                            vsm = VSM(extract_text_from_p(doc['texto']), extract_text_from_p(mSolr.body))
                            cache.set(chave, vsm)
                    
                    score = vsm*peso
                    materias += [(mSolr,score)]
        except:
            pass
    if materias:
        materias.sort(key=lambda x: -x[1])
    return materias[:total]
    

def words_relacionadas(ngram):
    big_text = ""
    query = "(%s)" % ngram
    materiasSolr = querySolr(query, total=50)
    for materiaSolr in materiasSolr:
        mSolr = MateriaDoSolr(materiaSolr)
        big_text += (" " + mSolr.body) 
    words = tf(big_text)
    words = sorted_dict_by_value(words)
    _unigrams = better_words(words)
    words = bag_of_words(big_text, remove_stopwords=True)
    words = bigrams(words)
    _bigrams = better_words(words)
    words = bag_of_words(big_text, remove_stopwords=False)
    words = trigrams(words)
    _trigrams = better_words(words)
    words = _unigrams + _bigrams + _trigrams
    query = [' OR '.join('(title:(%s) )'% tag for tag in words)]
    return query, words
from globocore.common.solr import SolrConnection
from django.conf import settings
from textAnalysis.utils import *
import itertools
import datetime

from globocore.materia.models import Materia
from textAnalysis.materia_do_solr import MateriaDoSolr 
from textAnalysis.ner import *  


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

    
def querySolr(query, total=50):
    
    materias = []
    solr_connection = SolrConnection(settings.SOLRSERVER)
    query = query.encode('utf-8')
    try:
        consulta = solr_connection.query(query + " isIssued:true type:texto publisher:G1 ", wt='json', start=0, rows=total,
                                   indent='on', sort='score desc, issued', sort_order='desc', )

        # print "materias ==>", len(consulta.results), query
        if consulta.results:
            # materias += [(materia, materia['score'] ) for materia in consulta.results]
            materias += consulta.results
    except:
        print "deu pau na query", query
        pass
            
    solr_connection.close()
    return materias


def consulta_editoria(doc):
    queries=""
    editorias = doc['editorias']
    if editorias: 
        queries = [' OR '.join("editoria_principal_s:\"%s\" " % editoria.name for editoria in editorias)]
        queries = ' AND (%s) ' % queries[0]
    return queries
        
def word_frequency(doc, editorias=True):
    text = "%s. %s. %s" % (doc['titulo'],doc['subtitulo'], extract_text_from_p(doc['texto']))
    q_editorias = ""
    # if editorias:
    #     q_editorias = consulta_editoria(doc)
        
    words = tf(text)
    words = sorted_dict_by_value(words)
    words = better_words(words) 

    # print words
    query = [' OR '.join('(title:(%s) %s)'% (tag,q_editorias) for tag in words)]

    return query, words



def entidades(doc, editorias=True):
    text = "%s. %s. %s" % (doc['titulo'],doc['subtitulo'], extract_text_from_p(doc['texto']))
    words = my_fastercts(text)
    q_editorias = ""
    if editorias:
        q_editorias = consulta_editoria(doc)
    query = [' OR '.join('(title:(%s) %s)'% (tag,q_editorias) for tag in words)]
    
    return query, words


def single_words_entities(doc, editorias=True):
    text = "%s. %s. %s" % (doc['titulo'],doc['subtitulo'], extract_text_from_p(doc['texto']))
    text = clean(text, separador=' ')
    q_editorias = ""
    if editorias:
        q_editorias = consulta_editoria(doc)
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
    words = _unigrams 
    
    text = "%s. %s. %s" % (doc['titulo'],doc['subtitulo'], extract_text_from_p(doc['texto']))
    entities = my_fastercts(text)
    
    # [it for it in itertools.combinations('ABCD',3)]

    # Aumento de 43% para 59%
    
    print words
    
    for ent in entities:
        if ent not in words:
            words.append(ent)
            
    print entities
    
    query = [' OR '.join('(%s)' % tag for tag in words)]
    
    if q_editorias:
        query = ['((%s) %s)' % (query[0], q_editorias)]
    
    return query, words

def relacionadas(documento, total, query):
    materias = []
    materiasSolr = querySolr(query)
    for materiaSolr in materiasSolr:
        mSolr = MateriaDoSolr(materiaSolr)
        peso = materiaSolr['score']
        # idMateria = re.search('(?<=[a-z]/)[0-9]+', materia.identifier).group(0)
        try:
            # m = Materia.objects.get(id = idMateria)
            # remove a propria materia da lista 
            if documento['titulo'] != mSolr.title:
                # nao coloca materias duplicadas na lista
                if not any([m.title == mSolr.title for (m,vsm) in materias]):
                    vsm = 1
                    # vsm = VSM(documento['titulo'], mSolr.title)*10
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
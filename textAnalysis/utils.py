import re
from htmlentitydefs import name2codepoint
from nltk import clean_html
import os
import nltk
from nltk.stem.rslp import RSLPStemmer
from numpy import zeros,dot
from numpy.linalg import norm
import itertools
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder
from nltk.metrics import BigramAssocMeasures, TrigramAssocMeasures
from lxml import html as lhtml
import unicodedata
import pickle

# python train_tagger.py mac_morpho --sequential au --fraction 0.8 --filename macmorpo_sed_tagger.pickle
# 51397 tagged sents, training on 41118
# training AffixTagger with affix -3 and backoff <DefaultTagger: tag=-None->
# training <class 'nltk.tag.sequential.UnigramTagger'> tagger with backoff <AffixTagger: size=5232>
# evaluating UnigramTagger
# accuracy: 0.865133
# dumping UnigramTagger to macmorpo_sed_tagger.pickle

tagger = nltk.data.load("taggers/macmorpo_sed_tagger.pickle")

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            try:
                text = unichr(name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def clean(text): 
    text = clean_html(text)
    text = unescape(text)
    text = normalize(text)
    text = re.sub(r"[.,?:;!\|_+=)(*&\^/><@#%\]\}\[\{\"\'\~\`]", r'.', text)
    text = re.sub(r"[\n\t\r]", r'', text)
    text = re.sub(r"[0-9]", r' 000 ', text)
    return text

def colocation(text,n, ini, fim):
    x = text.split()
    vec1 = []
    offset_ini_word=0
    for i in range(len(x)):
        vec2 = []
        for j in range(n):
            if i+n <= len(x):
                word = x[i+j]
                offset_ini_word = text[offset_ini_word:len(text)].index(word)+offset_ini_word
                offset_fim_word=offset_ini_word + len(word)
                vec2.append((word,offset_ini_word+ini,offset_fim_word+ini))
                offset_ini_word=vec2[0][2]-ini +1
        if vec2:
            vec1.append(vec2)
    return vec1
    
def normalize(text):
    if type(text) != unicode:
        try: 
            text = str(text).decode("UTF-8")
        except:
            text = str(text).decode("iso8859-1")
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore")
    return text.lower()

def extrai_ngram(text,n=4):
    words = []
    text = clean(text)
    
    for i in range(1,n+1):
        offset_ini_frase=0
        for frase in text.split("."):
            offset_fim_frase=offset_ini_frase + len(frase)
            ngrams = colocation(frase,i,offset_ini_frase,offset_fim_frase)
            for ngram in ngrams:
                word = ""
                ini = 999999
                fim = 0
                for (w,s,e) in ngram:
                    word += w if not word else " %s" % w
                    ini = s if ini > s else ini 
                    fim = e if fim < e else fim
                words.append((word,ini,fim))
            offset_ini_frase=offset_fim_frase+1
    return words


def extract_text_from_p(html):
    text = ""
    html = lhtml.fromstring(html)
    for pdata in html.cssselect('p'):
        if pdata.text:
            text += pdata.text
    return text

def stopwords():
    words = nltk.data.load("stopwords.txt", format='raw').decode("utf8").lower()  
    return set(words.split())

def entities():
    words = nltk.data.load("entidades", format='raw').decode("utf8")  
    return set([normalize(word) for word in words.split("\n") if not normalize(word) in stopwords()])

def bigrams(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    words = bigram_finder.ngram_fd.items()
    return [word for word in words if is_valid_bigram(word)]

def trigrams(words, score_fn=TrigramAssocMeasures.chi_sq, n=200):
    trigram_finder = TrigramCollocationFinder.from_words(words)
    words = trigram_finder.ngram_fd.items()
    return [word for word in words if is_valid_trigram(word)]

def bag_of_words(texto, remove_stopwords=False):
    words = clean(texto).split()
    if remove_stopwords:
        stop = stopwords()
        words = [word for word in words if word not in stop and len(word)>2 ]
    words = [word for word in words if not word.isdigit()]
    return words

def tf(texto):
    texto = texto.decode("utf-8")
    words = bag_of_words(texto, remove_stopwords=True)
    tagger = nltk.data.load("taggers/mac_morpho_aubt.pickle")
    tags = {}
    for word in words:
        if  is_valid_unigram(word):
            # word = word.lower()
            if tags.has_key(word):
                tags[word]+=1
            else:
                tags[word]=1
    return tags

def better_words(words):
    lista=[]
    media = (words[0][1]+words[len(words)-1][1])/2
    for (word, freq) in words:
        if type(word)==tuple:
            word=" ".join(word)
        if freq >= media and len(lista)<=10:
            # print word, freq, media
            lista.append(word)
    return lista

    # dist={}
    # for (word, freq) in words:
    #     if dist.has_key(freq):
    #         dist[freq]+=1
    #     else:
    #         dist[freq]=1
    # 
    # acum=0
    # for (word, freq) in words:
    #     acum+=freq*1.0/dist[freq]
    #     if type(word)==tuple:
    #         word=" ".join(word)
    #     print word, freq, acum
    #     lista.append([word])
    #     if acum >=80 or len(lista)>10:
    #         break


def lema(word):
    lemmatizer = RSLPStemmer()    
    return "%s*" % lemmatizer.stem(word)
    

def sorted_dict_by_value(tags):
    items = tags.items()
    items.sort( key=lambda tags:(-tags[1],tags[0]) )
    return items

def all_words(words, w_dict):
    for word in words:
        if w_dict.has_key(word):
            w_dict[word]+=words[word]
        else:
            w_dict[word]=words[word]
    return w_dict

def doc_vec(doc,key_idx):
    v=zeros(len(key_idx))
    for word in doc:
        keydata=key_idx.get(word, None)
        if keydata: 
            v[keydata[0]] = 1
    return v

def VSM(texto1, texto2):
    tags={}
    doc1 = tf(texto1)
    doc2 = tf(texto2)
    tags = all_words(doc1, tags)
    tags = all_words(doc2, tags)
    key_idx=dict()
    keys=tags.keys()
    keys.sort()
    for i in range(len(keys)):
        key_idx[keys[i]] = (i,tags[keys[i]])
    del keys
    del tags
    v1=doc_vec(doc1,key_idx)
    v2=doc_vec(doc2,key_idx)
    return float(dot(v1,v2) / (norm(v1) * norm(v2)))

def jaccard(texto1, texto2):
    tags={}
    doc1 = set(texto1)
    doc2 = set(texto2)
    docx = doc1.intersection(doc2)
    return float(len(docx)) / (len(doc1) + len(doc2) - len(docx))


def is_valid_trigram(t):
    if (tagger.tag([t[0][2]])[0][1]=='PCP' or tagger.tag([t[0][0]])[0][1]=='PCP' ):
        return False
    if (tagger.tag([t[0][2]])[0][1]=='ADV-KS-REL' or tagger.tag([t[0][0]])[0][1]=='ADV-KS-REL' ):
        return False
    if (tagger.tag([t[0][2]])[0][1]=='KS' or tagger.tag([t[0][0]])[0][1]=='KS' ):
        return False
    if (tagger.tag([t[0][0]])[0][1]=='KC' or tagger.tag([t[0][2]])[0][1]=='KC' ):
        return False
    if (tagger.tag([t[0][0]])[0][1]=='PREP' or tagger.tag([t[0][2]])[0][1]=='PREP' ):
        return False
    if (tagger.tag([t[0][0]])[0][1]=='V' or tagger.tag([t[0][2]])[0][1]=='V' ):
        return False
    if (tagger.tag([t[0][0]])[0][1]=='VAUX' or tagger.tag([t[0][2]])[0][1]=='VAUX' ):
        return False
    if (tagger.tag([t[0][0]])[0][1]=='ART' or tagger.tag([t[0][2]])[0][1]=='ART' ):
        return False
    if (tagger.tag([t[0][0]])[0][1]=='ADV' or tagger.tag([t[0][2]])[0][1]=='ADV' ):
        return False
    if (tagger.tag([t[0][0]])[0][1]=='NUM' or tagger.tag([t[0][2]])[0][1]=='NUM' ):
        return False          
    if (tagger.tag([t[0][0]])[0][0]=='no' or tagger.tag([t[0][2]])[0][0]=='na' ):
        return False
    if (tagger.tag([t[0][0]])[0][0]=='nos' or tagger.tag([t[0][2]])[0][0]=='nas' ):
        return False
    if (tagger.tag([t[0][0]])[0][0]=='do' or tagger.tag([t[0][2]])[0][0]=='da' ):
        return False
    if (tagger.tag([t[0][0]])[0][0]=='dos' or tagger.tag([t[0][2]])[0][0]=='das' ):
        return False
    if (tagger.tag([t[0][0]])[0][0]=='em' or tagger.tag([t[0][2]])[0][0]=='entre' ):
        return False
    if (tagger.tag([t[0][2]])[0][0]=='no' or tagger.tag([t[0][0]])[0][0]=='na' ):
        return False
    if (tagger.tag([t[0][2]])[0][0]=='nos' or tagger.tag([t[0][0]])[0][0]=='nas' ):
        return False
    if (tagger.tag([t[0][2]])[0][0]=='do' or tagger.tag([t[0][0]])[0][0]=='da' ):
        return False
    if (tagger.tag([t[0][2]])[0][0]=='dos' or tagger.tag([t[0][0]])[0][0]=='das' ):
        return False
    if (tagger.tag([t[0][2]])[0][0]=='em' or tagger.tag([t[0][0]])[0][0]=='entre' ):
        return False
    if (tagger.tag([t[0][2]])[0][0]=='nesta' or tagger.tag([t[0][0]])[0][0]=='nesta' ):
        return False
    if (tagger.tag([t[0][2]])[0][0]=='r' or tagger.tag([t[0][0]])[0][0]=='r' ):
        return False
    if (tagger.tag([t[0][1]])[0][1]=='V'): 
        return False
    if (tagger.tag([t[0][1]])[0][1]=='VAUX'):
        return False
    if (tagger.tag([t[0][1]])[0][1]=='ADV-KS-REL'):
        return False
    if (tagger.tag([t[0][1]])[0][1]=='PCP'):
        return False
    
    
    return True

def is_valid_bigram(t):
    if (tagger.tag([t[0][0]])[0][1]=='PREP' or tagger.tag([t[0][1]])[0][1]=='PREP' ):
        return False
    if (tagger.tag([t[0][0]])[0][1]=='VAUX' or tagger.tag([t[0][1]])[0][1]=='VAUX' ):
        return False
    if (tagger.tag([t[0][0]])[0][1]=='V' or tagger.tag([t[0][1]])[0][1]=='V' ):
        return False
    if (tagger.tag([t[0][0]])[0][1]=='ART' or tagger.tag([t[0][1]])[0][1]=='ART' ):
        return False
    if (tagger.tag([t[0][0]])[0][1]=='PCP' or tagger.tag([t[0][1]])[0][1]=='PCP' ):
        return False
    if (tagger.tag([t[0][0]])[0][1]=='ADV' or tagger.tag([t[0][1]])[0][1]=='ADV' ):
        return False
    if (tagger.tag([t[0][0]])[0][1]=='NUM' or tagger.tag([t[0][1]])[0][1]=='NUM' ):
        return False          
    if (tagger.tag([t[0][0]])[0][0]=='no' or tagger.tag([t[0][1]])[0][0]=='na' ):
        return False
    if (tagger.tag([t[0][0]])[0][0]=='nos' or tagger.tag([t[0][1]])[0][0]=='nas' ):
        return False
    if (tagger.tag([t[0][0]])[0][0]=='do' or tagger.tag([t[0][1]])[0][0]=='da' ):
        return False
    if (tagger.tag([t[0][0]])[0][0]=='dos' or tagger.tag([t[0][1]])[0][0]=='das' ):
        return False
    if (tagger.tag([t[0][0]])[0][0]=='em' or tagger.tag([t[0][1]])[0][0]=='entre' ):
        return False
    if (tagger.tag([t[0][1]])[0][0]=='no' or tagger.tag([t[0][0]])[0][0]=='na' ):
        return False
    if (tagger.tag([t[0][1]])[0][0]=='nos' or tagger.tag([t[0][0]])[0][0]=='nas' ):
        return False
    if (tagger.tag([t[0][1]])[0][0]=='do' or tagger.tag([t[0][0]])[0][0]=='da' ):
        return False
    if (tagger.tag([t[0][1]])[0][0]=='dos' or tagger.tag([t[0][0]])[0][0]=='das' ):
        return False
    if (tagger.tag([t[0][1]])[0][0]=='em' or tagger.tag([t[0][0]])[0][0]=='entre' ):
        return False
    if (tagger.tag([t[0][1]])[0][0]=='sao'): 
        return False
    # if (tagger.tag([t[0][1]])[0][1]=='KS'):
    #     return False
    if (tagger.tag([t[0][1]])[0][1]=='PCP'):
        return False
        
    return True
    
def is_valid_unigram(word):
    if  tagger.tag([word])[0][1]=='V':
        return False
    if  tagger.tag([word])[0][1]=='VAUX':
        return False
    if  tagger.tag([word])[0][1]=='KS':
        return False
    if  tagger.tag([word])[0][1]=='PREP':
        return False   
    if  tagger.tag([word])[0][1]=='PROADJ':
        return False  
    if  tagger.tag([word])[0][1]=='PCP':
        return False
    if  tagger.tag([word])[0][1]=='ADV':
        return False
    if  tagger.tag([word])[0][1]=='NUM':
        return False
    if  tagger.tag([word])[0][0]=='nesta':
        return False
    if  tagger.tag([word])[0][0]=='pela':
        return False  
    if  tagger.tag([word])[0][0]=='sao':
        return False  
    if  len(tagger.tag([word])[0][0])==1:
        return False
        
    return True
    
def is_valid_ngram(word):
    
    stops = ['pelo','pela','pelos','pelos','nesta','neste']
    for w in stops:
        if w in word:
            return False

    word = word.split()
    if len(word) == 3:
        return is_valid_trigram([word])
    elif len(word) == 2:
        return is_valid_bigram([word])
    elif len(word) == 1:
        return is_valid_unigram(word[0])
            
    return True
    
def saveClassifier(classifier, name='BayesModel.pkl'): 
    fModel = open(name,"wb") 
    pickle.dump(classifier, fModel,1) 
    fModel.close() 
    os.system("rm %s.gz" % name) 
    os.system("gzip %s" % name) 

def loadClassifier(name='BayesModel.pkl'): 
    os.system("gunzip %s.gz" % name) 
    fModel = open(name,"rb") 
    classifier = pickle.load(fModel) 
    fModel.close() 
    os.system("gzip %s" % name) 
    return classifier

import nltk
from textAnalysis.utils import *

def extrair_tags(texto):
    # texto = texto.decode("utf-8")
    tags = []
    stop = stopwords()
    texto = clean(texto).split()
    tagger = nltk.data.load("taggers/mac_morpho_aubt.pickle")
    wordfreq = nltk.FreqDist(w.lower() for w in texto if w.lower() not in stop)
    for item in wordfreq:
        # removendo verbos de palarvar em destaque
        if tagger.tag([item])[0][1] != 'V':
            tags += [(item, wordfreq.get(item))]
            if (len(tags) > 2):
                break
    print tags
    return tags
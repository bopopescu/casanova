# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from globocore.materia.models import Materia
from lxml import html as lhtml
import nltk

from textAnalysis.utils import *
# import random
_tagger = tagger()
# accuracy:  0.940168934772Most Informative Features
#                   classe = u'PREP+N'        não : sim    =    151.7 : 1.0
#                     pre1 = u'VAUX'          não : sim    =     94.7 : 1.0
#                   classe = u'-None-+NPROP'    sim : não   =     58.0 : 1.0
#                   classe = u'PCP'           não : sim    =     42.9 : 1.0
#                   classe = '-None-'          sim : não   =     42.2 : 1.0
#                   classe = u'PREP+N+PREP'   não : sim    =     40.9 : 1.0
#                     pos1 = u'ADJ'           não : sim    =     32.0 : 1.0
#                   classe = u'KC'            não : sim    =     27.7 : 1.0
#                   classe = u'N+NPROP+NPROP'    sim : não   =     27.7 : 1.0
#                   classe = u'ADJ+PREP'      não : sim    =     26.3 : 1.0
#                     pos1 = u'NUM'           não : sim    =     22.8 : 1.0
#                   classe = u'NPROP+PREP'    não : sim    =     20.6 : 1.0
#                   classe = u'NPROP+NPROP'    sim : não   =     19.8 : 1.0
#                   classe = u'NPROP+PREP+N'    sim : não   =     19.2 : 1.0
#                   classe = u'NPROP+ADJ+NPROP'    sim : não   =     17.7 : 1.0
#                     pre1 = u'PCP'           não : sim    =     15.5 : 1.0
#                   classe = u'PREP+NPROP+NPROP'   não : sim    =     15.0 : 1.0
#                     pos1 = u'CUR'           não : sim    =     15.0 : 1.0
#                   classe = u'V+N'           não : sim    =     14.0 : 1.0
#                   classe = u'N+ADJ'         não : sim    =     13.9 : 1.0


def features(sentenca,word): 
    features = {}
    classe = "+".join([(_tagger.tag([w])[0][1]) for w in word.split()])
    features['classe'] = classe
    features["primeira_letra"] = 'UC' if word.split()[0][0].isupper() else 'LC'    
    features["tamanho"] = len(word.split())
    
    marcador = ' ABBABBABBABABBBABABA '
    sentenca = sentenca.replace(word, marcador)
    sentenca = [w for (w,i,f) in extrai_ngram(sentenca,n=1)]
    ponteiro = sentenca.index(marcador.strip())
    
    if ponteiro - 1 >=0:
        features["pre1"] = _tagger.tag([sentenca[ponteiro-1]])[0][1]
    
    if ponteiro - 2 >=0:
        features["pre2"] = _tagger.tag([sentenca[ponteiro-2]])[0][1]
    
    if ponteiro + 1 <= len(sentenca)-1:
        features["pos1"] = _tagger.tag([sentenca[ponteiro+1]])[0][1]
    
    if ponteiro + 2 <= len(sentenca)-1:
        features["pos2"] = _tagger.tag([sentenca[ponteiro+2]])[0][1]

    return features

                    
class Command(BaseCommand): 
    
    def handle(self, *args, **options):
        import pdb; pdb.set_trace();
        materias = Materia.objects.filter(corpo__icontains='automatic-premium-tip-semantico')[:15000]
        # import pdb; pdb.set_trace();
        featuresets = []
        for m in materias:

            html = lhtml.fromstring(m.corpo.decode('utf-8'))
            tag = [ tag.text for tag in html.cssselect('.automatic-premium-tip-semantico') if tag.text]
            if tag:
                tag = tag[0]
                texto = unescape(clean_html(m.corpo))
                posicao = texto.find(tag)
                ini = texto[:posicao].rfind('.')+1 if texto[:posicao].rfind('.') > -1 else 0 
                final = posicao+len(tag)
                fim = texto[final:].find('.')+final+1 if texto[final:].find('.') > -1 else len(texto)
                featuresets.append((features(texto[ini:fim].strip(),tag), 'sim'))
            
                sentenca_titulo = " ".join(clean(m.titulo).split())
                ngram = extrai_ngram(sentenca_titulo)
                random.shuffle(ngram)
                featuresets.append((features(sentenca_titulo,ngram[0][0]), 'não'))
 
        random.shuffle(featuresets)
        
        # print featuresets
        train_set, test_set = featuresets[:len(featuresets)*80/100], featuresets[len(featuresets)*80/100:]
        classificador = nltk.NaiveBayesClassifier.train(train_set)
        print 'accuracy: ', nltk.classify.util.accuracy(classificador, test_set)
        print classificador.show_most_informative_features(20)
        saveClassifier(classificador, name='classificador_texto')

        # print classificador.prob_classify(time_features(times[0][0])).prob('Entidade')


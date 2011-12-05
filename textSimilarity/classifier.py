# -*- coding: utf-8 -*-
import nltk
import collections, random

def precision_recall(self, classifier, testfeats): 
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)
    for i, (feats, label) in enumerate(testfeats): 
        refsets[label].add(i)
        observed = classifier.classify(feats)
        testsets[observed].add(i)

    precisions = {}
    recalls = {}

    for label in classifier.labels():
        precisions[label] = nltk.metrics.precision(refsets[label],testsets[label])
        recalls[label] = nltk.metrics.recall(refsets[label], testsets[label])
    return precisions, recalls


def SaveClassifier(classifier): 
    fModel = open('BayesModel.pkl',"wb") 
    pickle.dump(classifier, fModel,1) 
    fModel.close() 
    os.system("rm BayesModel.pkl.gz") 
    os.system("gzip BayesModel.pkl") 

def LoadClassifier(): 
    os.system("gunzip BayesModel.pkl.gz") 
    fModel = open('BayesModel.pkl',"rb") 
    classifier = pickle.load(fModel) 
    fModel.close() 
    os.system("gzip BayesModel.pkl") 
    return classifier
        

def main(args):
    times = getTimesComPontuacaoDeAtleta()
    shuffle(times)
    featuresets = [(time_features(atletas), pontos) for (atletas,pontos) in times]
    train_set, test_set = featuresets[:len(times)*80/100], featuresets[len(times)*80/100:]
    classificador = nltk.NaiveBayesClassifier.train(train_set)
    print 'accuracy: ', nltk.classify.util.accuracy(classificador, test_set)
    print classificador.prob_classify(time_features(times[0][0])).prob('Bom')

if __name__ == '__main__':
    main(sys.argv)
    
        
# Probabilidade, Precision e Recall por Categoria
# category = set()
# for (d,c) in documents:
#     category.add(c)
# 
# 
# probs = classifier.prob_classify(test_set[0][0])
# for c in category:
#     print 'Probabilidade de ser de %s: %s' % (c,probs.prob(c))
#         
# 
# precisions, recalls = self.precision_recall(classifier, test_set)
# for c in category:
#     print 'Precision %s e Recall %s para %s:' % (precisions[c],recalls[c],c)
#         
# recuperando as melhores words segundo naive bayes
# self.mostinformativewords = set([(word) for word, val in classifier.most_informative_features(10000)])
# classifier.show_most_informative_features()
# print 'statics:', classifier.show_most_informative_features()

# -*- coding: utf-8 -*-
# import time
# from classifier import MultiBinaryClassifier
# from models import materia_corpus, Materia
# from datetime import *
# from features import document_features_single
# import random
# import nltk
# from textClassification.utils import *
# 
# from nltk.collocations import BigramCollocationFinder
# from nltk.metrics import BigramAssocMeasures
# from nltk.collocations import TrigramCollocationFinder
# from nltk.metrics import TrigramAssocMeasures
# from nltk.probability import FreqDist


"""
f = Folder.objects.filter(relatedfolder__materia__isnull=False).annotate(qtd=models.Count('id')).order_by('-qtd')
for f in folder:
    m = Materia.objects.filter(relatedfolder_set__is_primary=True, relatedfolder_set__folder=f)
    if len(m) >= 1000:
        print len(m), f.name
        
60631 Mundo
38557 G1
32409 Economia e Negócios
17247 Brasil
9783 São Paulo
9327 Pop & Arte
8364 Rio de Janeiro
6759 Política
7011 Tecnologia e Games
5175 Economia
5139 Jornal Nacional
4027 Bom Dia Brasil
3784 Concursos e Emprego
3469 Eleições 2010
2462 Minas Gerais
2118 Vestibular e Educação
1558 Ciência e Saúde
2242 Jornal Hoje
2122 Planeta Bizarro
1566 Auto Esporte
1708 Jornal da Globo
"""
# class MateriaModelTest(TestCaseTechTudo):
#     def setUp(self):
#         self.texto = """
#             O presidente da Costa do Marfim, Laurent Gbagbo, foi preso nesta segunda-feira (11) em sua casa em Abidjan, confirmaram o embaixador da França no país africano, Jean-Marc Simon, e a ONU.
#             A prisão foi feita por forças leais ao presidente eleito, o oposicionista Alassane Ouattara, e teve o apoio de tropas francesas e da ONU.
#             Os oposicionistas confirmaram a informação e informaram que Gbagbo e a esposa foram levados ao hotel que serve de QG à oposição.
#             
#             Desde domingo, às 17h locais, até 1h, a missão da ONU na Costa do Marfim (Onuci), e as forças francesas dispararam mísseis na direção do prédio em que Gbagbo está entrincheirado e contra o palácio presidencial.
#             A ONU explicou que o objetivo é "neutralizar o armamento pesado" do campo de Gbagbo para proteger os civis. Os combatentes de Alassane Ouattara, presidente reconhecido pela comunidade internacional, não conseguiu acabar com os redutos de seus adversários.
#             
#             """.decode("utf-8")
# 

    # def tearDown(self):
    #     pass
    # 
    # def test_word_frequency_dist(self):
    #     from textClassification.statistics import extrair_tags
    #     tags = extrair_tags(self.materia)
    #     print tags
    #     
    # def test_separa_tags_duplas_from_materia(self):
    #     self.materia = clean(self.materia).split()
    #     words = [w.lower() for w in self.materia]
    #     
    #     bcf = BigramCollocationFinder.from_words(words)
    #     tagger = nltk.data.load("taggers/mac_morpho_aubt.pickle")
    #     stop = stopwords()
    # 
    #     filter_stops = lambda w: len(w) < 3 or w in stop or tagger.tag([w])[0][1] == 'V'
    #     bcf.apply_word_filter(filter_stops)
    #     
    #     # print bcf.nbest(BigramAssocMeasures.likelihood_ratio, 10)
    #     print bcf.score_ngrams(BigramAssocMeasures.likelihood_ratio)
    #     

     # def test_verifica_que_a_materia_e_da_editoria_certa(self):
     #    n=datetime.now()
     #    documents = []
     #    labels = ["Ciência e Saúde","Auto Esporte","Economia e Negócios","Eleições 2010","Tecnologia e Games", "Brasil"]
     #    
     #    for l in labels:
     #        documents += materia_corpus(l,total=10)
     # 
     #    random.shuffle(documents)
     #    featuresets = [(document_features_single(d), c) for (d,c) in documents]
     #    train_set, test_set = featuresets[:len(documents)*80/100], featuresets[len(documents)*80/100:]
     #    
     #    # classificador = nltk.NaiveBayesClassifier.train(train_set)
     #    classificador = MultiBinaryClassifier().train(labels, train_set)
     #    errors =0
     #    for d,c in test_set:
     #        probs_label = ''
     #        probs_valor = 0
     #        for l in labels:
     #            prob_temp = classificador[l].prob_classify(document_features_single(d)).prob(l)
     #            if prob_temp >= probs_valor:
     #                probs_valor = prob_temp
     #                probs_label = l
     #            # print probs_label, probs_valor
     #        if probs_label != c:
     #            # print 'Probabilidade de ser %s, quando a real é %s' % (probs_label,c)
     #            errors += 1
     #    print "total de materias testadas", len(test_set), "total de erros", errors 

        # def test_separa_tags_triplas_from_materia(self):
        #     materia = Materia.objects.create(titulo="materia-1", slug="materia-1", corpo="""
        #     O presidente da Costa do Marfim, Laurent Gbagbo, foi preso nesta segunda-feira (11) em sua casa em Abidjan, confirmaram o embaixador da França no país africano, Jean-Marc Simon, e a ONU.
        #     A prisão foi feita por forças leais ao presidente eleito, o oposicionista Alassane Ouattara, e teve o apoio de tropas francesas e da ONU.
        #     Os oposicionistas confirmaram a informação e informaram que Gbagbo e a esposa foram levados ao hotel que serve de QG à oposição.
        # 
        #     Desde domingo, às 17h locais, até 1h, a missão da ONU na Costa do Marfim (Onuci), e as forças francesas dispararam mísseis na direção do prédio em que Gbagbo está entrincheirado e contra o palácio presidencial.
        #     A ONU explicou que o objetivo é "neutralizar o armamento pesado" do campo de Gbagbo para proteger os civis. Os combatentes de Alassane Ouattara, presidente reconhecido pela comunidade internacional, não conseguiu acabar com os redutos de seus adversários.
        # 
        #     """)
        #     materia = clean(materia.corpo).split()
        #     words = [w.lower() for w in materia]
        #     import pdb; pdb.set_trace()
        #     tcf = TrigramCollocationFinder.from_words(words)
        #     # print tcf.nbest(TrigramAssocMeasures.likelihood_ratio, 4)
        #     print tcf.ngram_fd

            
            
            
            


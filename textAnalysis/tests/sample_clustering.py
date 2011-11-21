# For real applications, you would use a decent tokenizer, 
# use integers instead of token-strings and don't calc a O(n^2) distance-matrix...

import sys
from math import log, sqrt
from itertools import combinations

def cosine_distance(a, b):
    cos = 0.0
    a_tfidf = a["tfidf"]
    for token, tfidf in b["tfidf"].iteritems():
        if token in a_tfidf:
            cos += tfidf * a_tfidf[token]
    return cos

def normalize(features):
    norm = 1.0 / sqrt(sum(i**2 for i in features.itervalues()))
    for k, v in features.iteritems():
        features[k] = v * norm
    return features

def add_tfidf_to(documents):
    tokens = {}
    for id, doc in enumerate(documents):
        tf = {}
        doc["tfidf"] = {}
        doc_tokens = doc.get("tokens", [])
        for token in doc_tokens:
            tf[token] = tf.get(token, 0) + 1
        num_tokens = len(doc_tokens)
        if num_tokens > 0:
            for token, freq in tf.iteritems():
                tokens.setdefault(token, []).append((id, float(freq) / num_tokens))

    doc_count = float(len(documents))
    for token, docs in tokens.iteritems():
        idf = log(doc_count / len(docs))
        for id, tf in docs:
            tfidf = tf * idf
            if tfidf > 0:
                documents[id]["tfidf"][token] = tfidf

    for doc in documents:
        doc["tfidf"] = normalize(doc["tfidf"])

def choose_cluster(node, cluster_lookup, edges):
    new = cluster_lookup[node]
    print node
    if node in edges:
        seen, num_seen = {}, {}
        for target, weight in edges.get(node, []):
            print node, target, seen.get(cluster_lookup[target], 0.0), weight
            seen[cluster_lookup[target]] = seen.get(
                cluster_lookup[target], 0.0) + weight
        # print seen
        for k, v in seen.iteritems():
            num_seen.setdefault(v, []).append(k)
        # print num_seen
        new = num_seen[max(num_seen)][0]
        print new,"\n"
    return new

def majorclust(graph):
    cluster_lookup = dict((node, i) for i, node in enumerate(graph.nodes))
    print cluster_lookup.values()
    
    count = 0
    movements = set()
    finished = False
    while not finished:
        finished = True
        for node in graph.nodes:
            new = choose_cluster(node, cluster_lookup, graph.edges)
            move = (node, cluster_lookup[node], new)
            # print move
            # print movements
            if new != cluster_lookup[node] and move not in movements:
                movements.add(move)
                cluster_lookup[node] = new
                finished = False

    clusters = {}
    # print cluster_lookup.values()
    for k, v in cluster_lookup.iteritems():
        clusters.setdefault(v, []).append(k)
    
    # print clusters.values()
    return clusters.values()

def get_distance_graph(documents):
    class Graph(object):
        def __init__(self):
            self.edges = {}

        def add_edge(self, n1, n2, w):
            self.edges.setdefault(n1, []).append((n2, w))
            self.edges.setdefault(n2, []).append((n1, w))

    graph = Graph()
    doc_ids = range(len(documents))
    graph.nodes = set(doc_ids)
    for a, b in combinations(doc_ids, 2):
        graph.add_edge(a, b, cosine_distance(documents[a], documents[b]))
    return graph

def get_documents():
    texts = [
        "foo blub baz",
        "foo bar baz",
        "asdf bsdf csdf",
        "foo bab blub",
        "csdf hddf kjtz",
        "123 456 890",
        "321 890 456 foo",
        "123 890 uiop",
    ]
    texts=[u'500 mil celulares com Android s\xe3o ativados por dia, diz cofundador do sistema da Google', u'Ghosttown, aplicativo para descobrir m\xfasicas chega na Android Market\n', u'Fish Bowl, uma nova galeria de imagens no seu smartphone com Android', u'Programa tira screenshots em smartphones Android ou tablets com Honeycomb', u'Presidente da Nokia diz que \u201cApple criou o Android\u201d\n', u'Atualiza\xe7\xe3o no Twitter para Android tem suporte a m\xfaltiplas contas e push notifications', u'Google Maps para Android aprende a andar de \xf4nibus', u'Google mostra lista de compatibilidade nos aplicativos do Android Market', u'Infobar, um smartphone Android com sotaque japon\xeas', u'BlueStacks: rode aplicativos do Android no Windows', u'Android TV promete praticidade e bons recursos \xe0queles que querem somente se divertir\n', u'Equalizador gratuito para telefones com Android 2.3 j\xe1 dispon\xedvel na Android Market\n', u'Usu\xe1rios de Android consomem mais dados que os outros', u'Skype atualiza app para Android e inclui videochamada via WiFi e 3G', u'Como deixar o Android em portugu\xeas do Brasil', u'ZTE Libra, um celular com Android Gingerbread ', u'Demonstre seu amor pelo Android com este pen drive\n', u'Modifique seu Android e deixe com a apar\xeancia do Ubuntu', u'Player de m\xfasica para Android tem visual id\xeantico ao do Windows Phone 7', u'Google promete corrigir falha de seguran\xe7a no Android', u'Aumente sua produtividade com o aplicativo Taskos', u'Gerenciando suas tarefas com a vers\xe3o Android do Remember The Milk', u'N\xe3o esque\xe7a mais de suas tarefas: adicione notas e listaas de tarefas na tela do seu Android', u'Mantenha suas tarefas em dia com o Wunderlist', u'Descubra uma maneira f\xe1cil de usar a fun\xe7\xe3o multitarefas no seu Android', u'Nextbook Next6, mais um tablet com Android\n', u'Troque a interface do seu Android, com efeitos, widgets e um menu personalizado', u'Aprenda como instalar ou mover aplicativos para o cart\xe3o SD no Android 2.2 Froyo', u'CM1, um celular b\xe1sico do tamanho de um cart\xe3o de cr\xe9dito', u'Vazam novas informa\xe7\xf5es sobre as fun\xe7\xf5es do Windows Phone 7.5', u'Controle o seu tempo de trabalho facilmente', u'Adicione widgets personaliz\xe1veis no seu Android', u'Aplicativo online te ajuda a gerenciar tarefas e projetos usando o GTD, de gra\xe7a', u'Como remover a barra de tarefas do Windows 7', u'Adicione o \xedcone do "Meu Computador" \xe0 barra de tarefas do Windows 7', u'Kompai, um rob\xf4 criado especialmente para ajudar idosos\n', u'Weave, um aplicativo que colabora com a sua produtividade', u'Windows: como for\xe7ar o encerramento de programas travados', u'Family Farm, jogo de fazenda para Linux, Mac OS X e Windows', u'Configure a exibi\xe7\xe3o das miniaturas da barra de tarefas do Windows 7', u'Mans\xe3o Misteriosa promete levar aventura e racioc\xednio para o Orkut', u'Prisioneiros chineses podem ter sido for\xe7ados a jogar MMOs', u'Configure o Windows 7 para desligar mais r\xe1pido', u'Mafia Wars: Aprenda como jogar esse sucesso do Facebook', u'Computador da IBM pode ser usado no lugar de atendentes de suporte e telemarketing', u'Nova atualiza\xe7\xe3o do Skype chega a usu\xe1rios Mac', u'Organize suas ideias com o app oficial da Moleskine ', u'Como eliminar todos os chefes de God of War 3', u'Escaneie documentos com a c\xe2mera do iPhone', u'Google+: Guia de comandos e atalhos', u'Anime qualquer festa com o ohDisco! Free para iPad, iPhone e iPod Touch', u'Como remover o Ubuntu?', u'Gerencie seu DropBox em smartphones Nokia com Symbian^3', u'Mouse serial no Ubuntu: Como habilitar?', u'Desinstale programas a partir do menu de contexto do Windows', u'Windows 7 n\xe3o inicializa direito? Aprenda como recuperar', u'Aprendendo a criar linhas luminescentes no Photoshop', u'Como jogar no seu Android com o Wii Remote', u'Como funciona o modo de compatibilidade do Windows 7?', u'Acesse os dados do Google Analytics no seu Android', u'Criando uma aurora colorida no Photoshop', u'Programe seus posts no Facebook com o Postcron', u'Volte no tempo nas\ntransmiss\xf5es ao vivo da TV Globo', u'Saiba como manusear o iPod Nano no Ubuntu']
    
    return [{"text": text, "tokens": text.split()}
             for i, text in enumerate(texts)]

def main(args):
    documents = get_documents()
    add_tfidf_to(documents)
    dist_graph = get_distance_graph(documents)
    for cluster in majorclust(dist_graph):
        print "========="
        print cluster
        for doc_id in cluster:
            print documents[doc_id]["text"]

if __name__ == '__main__':
    main(sys.argv)
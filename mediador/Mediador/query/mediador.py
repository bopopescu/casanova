#!/usr/local/bin/python
# -*- coding: utf-8 -*-


def recupera_palavras_chave_relacionadas_do_repo_de_futebol(palavras_chave):
    palavras = ["jogador", "flamengo" , "fluminense", "vasco", "romario", "campeonato",
     "carioca","brasileiro", "copa", "2005", "1995", "gols", "gol", "campeao",
      "gremio" , "brasil", "psv", "barcelona", "artilheiro", "mil"]
    return palavras
    
def recupera_urls_google_com_palavras_chave(palavras_chave):
    # urls = ["http://pt.wikipedia.org/wiki/Romário",
    # "http://www.romario11.com.br/",
    # "http://globoesporte.globo.com/ESP/Home/0,,8168,00.html",
    # "http://desciclo.pedia.ws/wiki/Romário",
    # "http://www.youtube.com/watch?v=gR8YwdzVaDg",
    # "http://www.youtube.com/watch?v=2wIC36KT97E",
    # "http://en.wikipedia.org/wiki/Romário",
    # "http://ego.globo.com/Gente/Celebridades/0,,LEA936-9805,00-ROMARIO.html",
    # "http://www.romario4011.com.br/",
    # "http://www.romario11.110mb.com/",]
    
    return urls
    
def recupera_palavras_chave_unicas_da_url(url):
    # lynx http://pt.wikipedia.org/wiki/Romário -dump -dont_wrap_pre -nolist -nonumbers -underscore >> foo.txt
    import os
    unixcmd = "lynx %s -dump -dont_wrap_pre -nolist -nonumbers -underscore | tr A-Z a-z | tr áéíóúàèìòùâêîôûçãõ aeiouaeiouaeioucao | tr -c a-z0-9 '\n' | sort -u | awk 'length($0) > 2'" % url
    f=os.popen(unixcmd)
    palavras = f.read().split('\n')
    #palavras = ["craque", "gols", "1000", "campeao", "romario", "flamengo"]
    return palavras
    
def compara_palavras_chave(palavras_chave_do_banco, palavras_chave_da_url):
    occurrency = 0
    for word_db in palavras_chave_do_banco:
        for word_web in palavras_chave_da_url:
            if word_db == word_web:
                occurrency += 1
                break
    proximidade = (occurrency * 1.0) #/ len(palavras_chave_da_url))
    return proximidade
    
def mediador(palavras_chave):
    palavras_chave_do_banco = recupera_palavras_chave_relacionadas_do_repo_de_futebol(palavras_chave)
    # urls = recupera_urls_google_com_palavras_chave(palavras_chave_do_banco)
    urls = recupera_urls_google_com_palavras_chave(palavras_chave)
    urls_avaliadas=[]
    for url in urls:
        palavras_chave_da_url = recupera_palavras_chave_unicas_da_url(url)
        proximidade = compara_palavras_chave(palavras_chave_do_banco, palavras_chave_da_url)
        t = (url,proximidade)  
        urls_avaliadas.append(t)
        
    return urls_avaliadas
    
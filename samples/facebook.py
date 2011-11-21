# -*- coding: utf-8 -*-
import logging
from lxml import etree
from django.conf import settings
from farofus.http_maneirao import HttpManeirao
import urllib, urllib2
import re






class user_likes(object):
    fql  = """ https://api.facebook.com/method/fql.query?
            query=
            SELECT url FROM url_like 
            WHERE user_id = me() and strpos(url,'/noticia/') >=0 
            &access_token=2227470867|2.AQChVZugrhUv-dqZ.3600.1318100400.0-1349825566|dHsIB7K39qc4OAP62WTf9Va52uc
            """
            
            # amigos
            #https://api.facebook.com/method/fql.query?query=SELECT url FROM url_like WHERE user_id in %28select uid2 from friend where uid1 = me%28%29 limit 10%29 and strpos%28url,%27http://www.techtudo.com.br/curiosidades/%27%29 %3E=0  limit 50 &access_token=2227470867|2.AQChVZugrhUv-dqZ.3600.1318100400.0-1349825566|dHsIB7K39qc4OAP62WTf9Va52uc
            
            #todos
            # http://developers.facebook.com/tools/explorer?method=GET&path=1349825566
            
            # SELECT id FROM object_url where url="http://www.techtudo.com.br/noticias/noticia/2011/10/e-mail-completa-40-anos-de-vida-neste-mes-de-outubro.html"
            

class Likes(object):


    def change_host(self, url):
        return re.sub(settings.BASE_URL,
                        'http://www.techtudo.com.br',
                        url)
    
    
    def url(self,url):        
        args = {}
        args['query'] = 'SELECT like_count, total_count, share_count, click_count from link_stat where url="%s"' % self.change_host(url)
        url = "https://api.facebook.com/method/fql.query?" + urllib.urlencode(args)
        return url
        
    def recortar_itens(self,response):
        xml = etree.XML(response)
        fcb = {
            'like_count':xml[0][0].text,
            'total_count':xml[0][1].text,
            'share_count':xml[0][2].text,
            'click_count':xml[0][3].text,
        }
        return fcb
    
    def _html(self,url):
        response = urllib2.urlopen(url)
        if not response:
            return ''
        return self.recortar_itens(response.read())

    def html(self):
        return self._html(self.url())

class LikesDaMateria(Likes):
    
    def __init__(self,materia):
        self.materia = materia
    
    def url(self):
        return super(LikesDaMateria, self).url(self.materia.get_full_url())
        
#         
# def lerfacebook():
# args = {}
# token = '&access_token=AAACEdEose0cBAIwC1vC5ZAsm61EHUp3LRZCbcZCFV0iuJKjfHrYE2xV5iuJ3fTyHq7z1SAL3I3ph83yr5l6b2mdEJrlL3p8AXbWYMIDoLH31gU0oKul'
# args['query'] = 'select uid2 from friend where uid1 = me()'
# url = "https://api.facebook.com/method/fql.query?" + urllib.urlencode(args) + token
# response = urllib2.urlopen(url)
# xml = etree.XML(response.read())
# critics = {}
# for i in range(len(xml)):
#     args['query'] = "SELECT name FROM user WHERE uid = %s" % xml[i][0].text
#     url = "https://api.facebook.com/method/fql.query?" + urllib.urlencode(args) + token
#     response = urllib2.urlopen(url)
#     xml_nome = etree.XML(response.read())
#     # print xml_nome[0][0].text
#     
#     args['query'] = "SELECT url FROM url_like WHERE user_id=%s and strpos(url, 'techtudo.com.br') >=0" % xml[i][0].text
#     url = "https://api.facebook.com/method/fql.query?" + urllib.urlencode(args) + token
#     response = urllib2.urlopen(url)
#     xml_urls = etree.XML(response.read())
#     # print len(xml_urls)
#     
#     if len(xml_urls):
#         critics[xml_nome[0][0].text] = {}
#         for j in range(len(xml_urls)):
#             # print xml_urls[j][0].text
#             critics[xml_nome[0][0].text][xml_urls[j][0].text]=1    
# print critics
# 
# search.twitter.com/search.json?q=http://www.techtudo.com.br/noticias/noticia/2011/10/net-claro-e-embratel-se-juntam-para-concorrer-contra-oi-conta-total.html
    
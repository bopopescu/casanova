from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.shortcuts import render_to_response
from lxml import etree,html
import urllib
import urllib2

# def busca(request):
#     now = datetime.datetime.now()
#     html = "It is now %s.<br>" % now
#     html+= "%s=%s<br>" % ("q",request.GET.get('q'))
#     
#     from lxml import etree,html
#     import urllib
#     import urllib2
#     google_url = "http://www.google.com/search?q=flamengo+cruzeiro+2009" #+ request.GET.get('q')  
#     req = urllib2.Request(google_url)
#     user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
#     req.add_header('User-Agent', user_agent)
#     response = urllib2.urlopen(req)    
#     content = response.read()
#     googlepage = etree.HTML(content)
#     xpatheval = etree.XPathEvaluator(googlepage)
#     urls = xpatheval("//a")
#     for url in urls:
#         html += url.text + " <br> "
#     
#     return HttpResponse(html)

def google(request):
    return render_to_response("busca.html")
    
def mediador(request):
    import mediador
    urls = mediador.mediador("romario")
    urls = sorted(urls, key=lambda proximidade: proximidade[1], reverse=True)
    html = "<table border=1>"
    for url in urls:
        html += "<tr><td>%s</td><td><a href='%s'>%s</a></td></tr>" % (url[1],url[0],url[0])
    html += "</table>"
    return HttpResponse(html)    

def recupera_urls(url, lista_urls):
    req = urllib2.Request(url)
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    req.add_header('User-Agent', user_agent)
    try:
        response = urllib2.urlopen(req)
        content = response.read()
        googlepage = etree.HTML(content)
        xpatheval = etree.XPathEvaluator(googlepage)
        urls = xpatheval("//a")
        try:
            host = response.url[0:response.url.index("/",8)]
        except:
            host = response.url
        
        for url in urls:
            lnk = str(url.get('href'))
            if lnk:
                if not (lnk.startswith('mailto') or lnk.startswith('#') or lnk.startswith('www')):
                    if (lnk.find("#")==-1 and lnk.find("..")==-1 and lnk.find("@")==-1 and lnk.find("none")==-1):
                        if (lnk.startswith('http')):
                            pass
                        else:
                            if (not lnk.startswith('/')):
                                host = response.url[0:response.url.rindex("/")] + "/"
                            else:
                                host = response.url[0:response.url.index("/",8)]
                            page = host + lnk                    
                            req2 = urllib2.Request(page)
                            response2 = urllib2.urlopen(req2)
                            if not (response2.code == 404):
                                url={}
                                url['url']=page
                                prx = textCompare(response2.read())
                                #prx = 0
                                url['prx']=prx
                                try:
                                    lista_urls.index(url)
                                except:
                                    lista_urls.append(url)
    except:
        print "error"
        pass

def busca(request,template_name='crawler.html'):
    q = request.GET.get('q') 
    n = request.GET.get('n')
    url={}
    url['url']=q
    url['prx']=0
    lista_urls=[url]
    i=0
    for url in lista_urls:
        links_antes = len(lista_urls)        
        if len(lista_urls)>int(n):
            break
        recupera_urls(url['url'], lista_urls)
        links_depois = len(lista_urls)
        i+=1
        print "total:%s atual:%s links:%s, url:%s" % (len(lista_urls),i,links_depois-links_antes,url['url'])

    html = ""
    for url in lista_urls:
        html += "<a href='%s'>%s</a> <b>%s</b><br>" % (url['url'],url['url'],url['prx'])
    
    return HttpResponse(html)    

# def busca(request,template_name='busca.html'):
#     return render_to_response(template_name)
    
    
def textCompare(str):     
    f = open('/tmp/corpus.txt', 'r')
    import Levenshtein
    import pdb; pdb.set_trace()
    r = Levenshtein.ratio(str,f.read())
    return r
    
    
    
    

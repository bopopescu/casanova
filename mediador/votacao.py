import urllib
import urllib2
#from lxml import etree

urlUruguai = 'http://www.simuladorcopadomundo.com.br/registra_palpite?palpiteTime1=3&palpiteTime2=0&partida_id=61&rodada_id=semifinais'
urlParaguai = 'http://www.simuladorcopadomundo.com.br/registra_palpite?palpiteTime1=1&palpiteTime2=4&partida_id=62&rodada_id=semifinais'

urlKorea = 'http://www.simuladorcopadomundo.com.br/registra_palpite?palpiteTime1=0&palpiteTime2=4&partida_id=49&rodada_id=oitavas'
urlJapao = 'http://www.simuladorcopadomundo.com.br/registra_palpite?palpiteTime1=1&palpiteTime2=3&partida_id=55&rodada_id=oitavas'

url= 'http://www.simuladorcopadomundo.com.br/registra_palpite?palpiteTime1=5&palpiteTime2=3&partida_id=58&rodada_id=quartas'



for i in range(50):
    if i%2==0:
        url = url
    else:
        url = url
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    print response.code
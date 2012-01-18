from django.core.management.base import BaseCommand
from globocore.materia.models import Materia
import time
from globocore.common.solr import SolrConnection
from django.conf import settings
import time, datetime

class Command(BaseCommand): 
    
    def handle(self, *args, **options):
        inicio =0
        total=1000
        solr_connection = SolrConnection(settings.SOLRSERVER)
        
        for i in range(50):
            # materias = Materia.objects.filter(corpo__icontains='saibamais')[inicio:total]
            datainicio = datetime.datetime(day=1,month=6,year=2011)
            datafim = datetime.datetime(day=1,month=2,year=2012)
            materias = Materia.objects.filter(ultima_publicacao__gt=datainicio, ultima_publicacao__lt=datafim)[inicio:total]
            
            erros = 0
            for m in materias:
                consulta = solr_connection.query('identifier:"%s"'%m.obtem_url_visao_de_busca(search_type='solr'))
                if not consulta.results:
                    try:
                        m.notifica_barramento("publicar")
                    except:
                        print "erro ao notificar %s" % m.id
                        erros +=1
                    # time.sleep(0.1)
                else:
                    # print "notificada %s" % m.id
                    pass
            print inicio, total
            print "total de erros=>",erros
            time.sleep(10)
            incremento = total - inicio
            inicio += incremento
            total += incremento
            solr_connection.close()
        
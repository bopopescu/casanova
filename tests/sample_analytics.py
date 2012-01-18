#!/usr/bin/python
# (CC-by) 2010 Copyleft Michal Karzynski, GenomikaStudio.com
import datetime
import gdata.analytics.client
import gdata.sample_util
 
email="demetrius.rapello@gmail.com"  # Set these values
password="ddd9409"
table_ids = (
            'ga:37399310',          # TABLE_ID for first website
            )
 
SOURCE_APP_NAME = 'TechTudo'
client = gdata.analytics.client.AnalyticsClient(source=SOURCE_APP_NAME)
client.client_login(email, password, source=SOURCE_APP_NAME, service=client.auth_service)
 
end = datetime.date.today()
start = end - datetime.timedelta(days=100)

origem='/noticias/noticia/2011/08/adolescente-divulga-festa-no-facebook-e-tem-mansao-invadida-por-100-desconhecidos.html'
destino='/noticias/noticia/2011/08/noiva-se-enforca-apos-escrever-no-facebook-que-seu-casamento-havia-sido-cancelado.html'

for table_id in table_ids:  
    data_query = gdata.analytics.client.DataFeedQuery({
            'ids': table_id,
            'start-date': start.isoformat(),
            'end-date': end.isoformat(),
            'dimensions': 'ga:visitCount',
            'metrics': 'ga:visits',
            'sort': 'ga:visits',
            # 'filters': 'ga:previousPagePath==%s;ga:pagePath==%s' % (origem , destino)
            'filters': 'ga:pagePath==%s' % (destino)
            }) 
    feed = client.GetDataFeed(data_query)
    import pdb; pdb.set_trace();              

    for e in feed.entry:
        print e.get_object('ga:visitCount').value

    # print "%s : %s" % (feed.data_source[0].table_name.text, feed.entry[0].metric[0].value)
import datetime
import gdata.analytics.client
import gdata.sample_util

class Feed(object):

    def __init__(self):
        SOURCE_APP_NAME = 'TechTudo'
        self.client = gdata.analytics.client.AnalyticsClient(source=SOURCE_APP_NAME)
        email="demetrius.rapello@gmail.com"
        password="ddd9409"
        self.table_id ='ga:37399310'
        self.end = datetime.date.today()
        self.start = self.end - datetime.timedelta(days=30)
        self.client.client_login(email, password, source=SOURCE_APP_NAME, service=self.client.auth_service)

    def get_pageviews(self, origem, destino):
        data_query = gdata.analytics.client.DataFeedQuery({
             'ids': self.table_id,
             'start-date': origem.primeira_publicacao.date().isoformat(),
             'end-date': (origem.primeira_publicacao + datetime.timedelta(days=30)).date().isoformat(),
             'dimensions': 'ga:pagePath,ga:previousPagePath,ga:nextPagePath',
             'metrics': 'ga:pageViews',
             'sort': '-ga:pageViews',
             'filters': 'ga:previousPagePath==%s;ga:pagePath==%s' % (origem.permalink , destino.permalink)
             }) 
        feed = self.client.GetDataFeed(data_query)
        
        if feed.entry:
            return feed.entry[0].get_object('ga:pageviews').value

        return 0
        
    def get_paginas(self, origem):
        data_query = gdata.analytics.client.DataFeedQuery({
             'ids': self.table_id,
             'start-date': origem.primeira_publicacao.date().isoformat(),
             'end-date': (origem.primeira_publicacao + datetime.timedelta(days=30)).date().isoformat(),
             'dimensions': 'ga:pagePath,ga:previousPagePath,ga:nextPagePath',
             'metrics': 'ga:pageViews',
             'sort': '-ga:pageViews',
             'filters': 'ga:previousPagePath=@noticia;ga:pagePath==%s' % (origem.permalink)
             }) 
        feed = self.client.GetDataFeed(data_query)
        
        return feed.entry if feed.entry else []  
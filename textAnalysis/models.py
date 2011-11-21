# -*- coding: utf-8 -*-
from django.db import models
      
class Analytics(models.Model):
    origem = models.CharField(u'origem', max_length=1000)
    destino = models.CharField(u'destino', max_length=1000)
    pageviews = models.IntegerField()

    def __str__(self):
        return "%s - %s" % (self.pageviews, self.destino)
    

class TimeRodada(models.Model):
    class Meta:
        db_table = 'time_rodada'

    time_rodada_id = models.IntegerField(primary_key=True)
    rodada_id = models.IntegerField()
    time_id = models.IntegerField()
    esquema_id = models.IntegerField()
    pontos_num = models.IntegerField()
    patrimonio_num = models.IntegerField()


class TimeAtleta(models.Model):
    class Meta:
        db_table = 'time_atleta'

    time_atleta_id = models.IntegerField(primary_key=True)
    rodada_id = models.IntegerField()
    time_id = models.IntegerField()
    atleta_id = models.IntegerField()

class AtletaRodada(models.Model):
    class Meta:
        db_table = 'atleta_rodada'
        
    atleta_rodada_id = models.IntegerField(primary_key=True)
    atleta_id = models.IntegerField()
    rodada_id = models.IntegerField()
    clube_id = models.IntegerField()
    posicao_id = models.IntegerField()
    status_id = models.IntegerField()
    pontos_num = models.IntegerField()
    preco_num = models.IntegerField()
    variacao_num = models.IntegerField()
    media_num = models.IntegerField()
    jogos_num = models.IntegerField()
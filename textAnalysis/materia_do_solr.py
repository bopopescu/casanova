# -*- coding: utf-8 -*-
import logging
from datetime import date
from django.conf import settings
from django.utils.datastructures import SortedDict
from globocore.common.solr import SolrConnection
from globocore.materia.models import Materia
import re


class MateriaDoSolr(object):
    
    def __init__(self, resultado_solr):
        for nome_atributo in resultado_solr:
            setattr(self, nome_atributo, resultado_solr[nome_atributo])
    
    def get_materia_original(self):
        try:
            materia_id = re.search('\d+',re.search('/\d+/solr',self.identifier).group()).group()
            return Materia.objects.get(id=materia_id)
        except:
            return None

    @property
    def chapeu(self):
        return self.editoria_principal_s
        
    @staticmethod
    def criar_query(editoria):
        query = u'(type:texto) AND (species:Matéria) AND (isIssued:True)'
        query += u'  AND (publisher:"%s")' % (settings.PORTAL_SOLR_PUBLISHER)
        if editoria:
            query += u' AND (section:"%s")' % editoria.name
        return str(query)
    


from django.core.management.base import BaseCommand
from globocore.materia.models import Materia
import time
from globocore.common.solr import SolrConnection
from django.conf import settings
import time, datetime
from farofus.materia_do_solr import MateriaDoSolr 
import re

class Command(BaseCommand): 
    
    def handle(self, *args, **options):
        solr_connection = SolrConnection(settings.SOLRSERVER)
        solr_connection.delete_query('publisher:Techtudo')
        solr_connection.close()

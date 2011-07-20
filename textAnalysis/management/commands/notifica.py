from django.core.management.base import BaseCommand
from globocore.materia.models import Materia
import time

class Command(BaseCommand): 
    
    def handle(self, *args, **options):
        materias = Materia.objects.all().order_by('-id')
        for m in materias:
            m.notifica_barramento("publicar")
            time.sleep(0.1)
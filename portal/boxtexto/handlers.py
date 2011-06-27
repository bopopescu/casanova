from piston.handler import BaseHandler
from boxtexto.models import BoxTexto
from django.http import Http404 

class BoxTextoHandler(BaseHandler):
   allowed_methods = ('GET',)
   model = BoxTexto
   fields = ('id', 'title',)
   
   def read(self, request, boxtexto_id):
   	if boxtexto_id == 'todos':
   		return BoxTexto.objects.all()
   	else:
   		return BoxTexto.objects.get(id=boxtexto_id) 


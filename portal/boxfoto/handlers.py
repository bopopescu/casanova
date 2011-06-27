from piston.handler import BaseHandler
from boxfoto.models import BoxFoto
from django.http import Http404 

class BoxFotoHandler(BaseHandler):
   allowed_methods = ('GET',)
   model = BoxFoto
   fields = ('id', 'title',)
   
   def read(self, request, boxfoto_id):
   	if boxfoto_id == 'todos':
   		return BoxFoto.objects.all()
   	else:
   		return BoxFoto.objects.get(id=boxfoto_id) 


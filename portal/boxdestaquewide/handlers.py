from piston.handler import BaseHandler
from boxdestaquewide.models import BoxDestaqueWide
from django.http import Http404 

class BoxDestaqueWideHandler(BaseHandler):
   allowed_methods = ('GET',)
   model = BoxDestaqueWide
   fields = ('id', 'title',)
   
   def read(self, request, boxdestaquewide_id):
   	if boxdestaquewide_id == 'todos':
   		return BoxDestaqueWide.objects.all()
   	else:
   		return BoxDestaqueWide.objects.get(id=boxdestaquewide_id) 


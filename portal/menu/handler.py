from piston.handler import BaseHandler
from menu.models import Menu
from django.http import Http404 

class MenuHandler(BaseHandler):
   allowed_methods = ('GET',)
   model = Menu
   fields = ('id', 'title',)
   
   def read(self, request, menu_id):
   	if menu_id == 'todos':
   		return Menu.objects.all()
   	else:
   		return Menu.objects.get(id=menu_id) 


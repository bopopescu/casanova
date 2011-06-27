from django.conf.urls.defaults import *
from piston.resource import Resource
from portal.menu.handlers import MenuHandler

menu_handler = Resource(MenuHandler)

urlpatterns = patterns('',
   url(r'^menu/(?P<menu_id>[^/]+).js$', menu_handler, { 'emitter_format': 'json' }),
)

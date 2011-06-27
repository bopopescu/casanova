from django.conf.urls.defaults import *
from piston.resource import Resource
from portal.boxfoto.handlers import BoxFotoHandler

boxfoto_handler = Resource(BoxFotoHandler)

urlpatterns = patterns('',
   url(r'^boxfoto/(?P<boxfoto_id>[^/]+).js$', boxfoto_handler, { 'emitter_format': 'json' }),
)

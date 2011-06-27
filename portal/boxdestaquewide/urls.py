from django.conf.urls.defaults import *
from piston.resource import Resource
from portal.boxdestaquewide.handlers import BoxDestaqueWideHandler

boxdestaquewide_handler = Resource(BoxDestaqueWideHandler)

urlpatterns = patterns('',
   url(r'^boxdestaquewide/(?P<boxdestaquewide_id>[^/]+).js$', boxdestaquewide_handler, { 'emitter_format': 'json' }),
)

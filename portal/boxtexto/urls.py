from django.conf.urls.defaults import *
from piston.resource import Resource
from portal.boxtexto.handlers import BoxTextoHandler

boxtexto_handler = Resource(BoxTextoHandler)

urlpatterns = patterns('',
   url(r'^boxtexto/(?P<boxtexto_id>[^/]+).js$', boxtexto_handler, { 'emitter_format': 'json' }),
)

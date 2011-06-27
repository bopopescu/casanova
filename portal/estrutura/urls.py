from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    # Example:
   ('edit/(?P<site>[0-9A-Za-z_]+)\.html$', edit), 
   ('(?P<site>[0-9A-Za-z_]+)\.html$', site),
   
   ('instancia/(?P<site>[0-9A-Za-z_]+)/(?P<modulo>[0-9A-Za-z_]+)/(?P<instancia>[0-9]+)/(?P<ordem>[0-9]+)/delete$', delete), 
   ('instancia/(?P<site>[0-9A-Za-z_]+)/(?P<modulo>[0-9A-Za-z_]+)/(?P<ordem>[0-9]+)/add$', add),
   ('instancia/(?P<site>[0-9A-Za-z_]+)/(?P<modulo>[0-9A-Za-z_]+)/(?P<instancia>[0-9]+)/(?P<ordem>[0-9]+)/save$', save), 
   
)

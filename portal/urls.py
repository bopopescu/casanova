from django.conf.urls.defaults import *
import os
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf import settings


urlpatterns = patterns('',
    # Example:
    (r'^portal/', include('portal.estrutura.urls')),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
	(r'^portal/media/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_PATH, 'media')}),

)


proibidos = ['django.contrib.contenttypes',
    'django.contrib.sessions',
    'portal.estrutura', 
    'django.contrib.admin']

for app in settings.INSTALLED_APPS:
    if not proibidos.__contains__(app):
        modulo = app.split('.')[-1]
        urlpatterns += patterns('',(r'^portal/'+modulo+'/api/', include('portal.'+modulo+'.urls')),)


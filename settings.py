# -*- coding: utf-8 -*-

from os.path import join, dirname, abspath, exists

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)
LOCAL = True

MANAGERS = ADMINS

DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    'NAME': 'g1',                      # Or path to database file if using sqlite3.
    'USER': 'u_g1',                      # Not used with sqlite3.
    'PASSWORD': 'u_g1',                  # Not used with sqlite3.
    'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
    'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
}
}

LOCAL_FILE = lambda *x: abspath(join(dirname(__file__), *x))

SERVER_NAME = '127.0.0.1'

BASE_URL = "http://%s:8000" % SERVER_NAME

#Url de backend
BASE_BE_URL = BASE_URL
STATIC_URL = '/static/'
PUBLISHING_STATIC_PATH = LOCAL_FILE('editoria')

STATIC_FLASH_PATH = LOCAL_FILE('flash')
PHOTO_STATIC_PATH = LOCAL_FILE('fotos')
STATIC_PHOTOS_URL = LOCAL_FILE('fotos')

BROKER = 'stomp://%s:61613/' % SERVER_NAME
#BROKER = 'tcp://riovld87.globoi.com:61616?wireformat=openwire'

#Solr que processa as notificaes
# SOLRSERVER = 'http://%s:8983/solr' % SERVER_NAME #'http://solr.portal.qa01.globoi.com/solr'
# SOLRSERVER = 'http://solr.portal.globoi.com/solr'
SOLRSERVER = 'http://localhost:8983/solr'

# URL da fast usada para gera dos feeds de noticia/foto/video usados na
# edi de homegit
#FAST_URL = "http://jornalismo1.glb.com:15100"
#FAST_URL = "http://fastqr.dev.globoi.com:15100"
# FAST_URL = "http://cms.plataformas.glb.com:15100"

# 159  PHOTO_URL_PATH = '/photo_static/'
# 160  PHOTO_ALLOWED_TYPES = ['jpeg', 'jpg', 'gif', 'png']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = LOCAL_FILE('media')

PHOTO_URL_PATH = '/photo_static/'
FLASH_URL_PATH = '/media/flash'
PUBLISHING_URL_PATH = ''
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''
PORTAL = 'core'

#Nome do portal usado como Token da Fast
PORTAL_TOKEN_FAST = 'core'

#Titulo no portal usado nos Titles das páginas
PORTAL_TITLE = 'core'

#uuid do root folder do seu projeto
ROOT_ID = '55729699-b9c0-4052-8ad3-16bd0cb52b32'

#Nome de publisher usado na indexação do solr
PORTAL_SOLR_PUBLISHER = 'globocore'


#Universo de conteúdo de acordo com a barra da Globo.com. Usado no solr e fast.
MACROTEMA = 'Noticias'

#Nome da coleção na Fast
FAST_COLLECTION = ''

#Nome da visao na Fast
FAST_VIEW = 'coresppublished'

#Campo da Fast usado no filtro de navegadores/busca
FAST_FIELD_GALERIA = 'subeditorias'
FAST_FIELD_MATERIA = 'subeditorias'
FAST_FIELD_VIDEO = 'programa'

#Local dos arquivos 'copia' do vignette usadaos em widgets para display local
VIGNETTE_FILES = LOCAL_FILE('templates', PORTAL, 'delivery')

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '$wr%h(k7d@6x0f7&csw681$pe2xc9-4)vkya!!qy4-558t3#yb'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

import os
WEBSITE_DIR = os.path.dirname(__file__)

PROJECT_ROOT = os.path.abspath(WEBSITE_DIR)
TEMPLATE_DIRS = (
    '%s/globocore/materia/templates' % PROJECT_ROOT,
    '%s/textAnalysis/templates' % PROJECT_ROOT,
    
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    # 'testutils',
    'textAnalysis',
    #'textSimilarity',
    'globocore',
    # 'globocore.estrutura',
    # 'globocore.materia',
    # Uncomment the next line to enable the admin:
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'importador',

)

EXCLUDE_TEST_APPS = (
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.sites',
'django.contrib.messages',
'django.contrib.admin',
'testutils',
)

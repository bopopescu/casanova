#-*- coding:utf-8 -*-
import imp
import os
from os.path import dirname
from optparse import make_option
from subprocess import Popen, PIPE
import subprocess
from lxml import html as lhtml
import pytest
import coverage
from django.core.management.base import BaseCommand
from optparse import make_option
import sys
from django.conf import settings


class Command(BaseCommand):
    pasta_dos_testes = []
    option_list = BaseCommand.option_list + (
    make_option('-p',
        action='store',
        dest='keyword_expr',
        default='',
        help='only run tests which match given keyword expression.'\
             'An expression consists of space-separated terms. Each'\
             'term must match. Precede a term with "-" to negate.'\
             'Terminate expression with ":" to make the first match'\
             'match all subsequent tests (usually file-order).'),
    make_option('-a', '--app',
        action='store',
        dest='app',
        default='',
        help=u'Roda os testes somente de uma aplicação')
    )

    help = 'Runs the test suite, creating a test db IF NEEDED and NOT DESTROYING the test db afterwards.  Otherwise operates exactly as does test.'
    args = '[appname ...]'

    requires_model_validation = False
            
    def pre_handle(self, *args, **options):
        pass

    def include_files_to_coverage(self):
        diretorios = []
        for arquivo in self.arquivos_para_cobertura():
            arquivo_modulo = arquivo.replace("/",".").replace(".py","")
            exec("import %s" % arquivo_modulo)

    def handle(self, *args, **options):
        self.pre_handle(*args, **options)
        self.app = options.get('app')
        pastas = self._coleta_pastas()
        if not pastas:
            print "Nenhum teste encontrado"
            raise SystemExit(0)

        cov = coverage.coverage(include=self.arquivos_para_cobertura(), branch=True, auto_data=False)
        cov.start()
        self.include_files_to_coverage()
        ret = self.roda_testes(options, pastas)
        cov.stop()

        raise SystemExit(ret)

    def roda_testes(self, options, pastas):
        pytest_argv = ['--capture=no']

        if options.get('keyword_expr'):
            pytest_argv.append('-k %s' % options['keyword_expr'])

        pytest_argv.extend(pastas)

        return pytest.main(pytest_argv)

    def arquivos_para_cobertura(self):
        arquivos = []
        for app in self.apps_para_cobertura():
            p = Popen(['find', app, '-name', '*.py'], stdout=PIPE)
            pys = p.communicate()[0].split('\n')
            pys = [f for f in pys if f and 'test' not in f]
            arquivos.extend(pys)            
        return arquivos

    def apps_para_cobertura(self):
        if self.app:
            return [self.app]
        apps = []
        exclude_apps = getattr(settings, 'EXCLUDE_TEST_APPS', [])
        for app in settings.INSTALLED_APPS:
            if app not in exclude_apps: 
                apps.append(app)
        return apps

    def _coleta_pastas(self):
        pastas = []
        for app in self.apps_para_cobertura():
            caminhos = self._pega_pastas_de_testes(app)
            if not caminhos:
                continue
            pastas.extend(caminhos)
        return pastas

    def _pega_pastas_de_testes(self,app):
        caminhos = []
        # for pasta in self.pasta_dos_testes:
        # caminho_testes = '%s.tests.%s' % (app, pasta)
        caminho_testes = '%s.tests' % (app)
        try:
            mod = __import__(caminho_testes)
            caminhos.append(mod.tests.__file__.replace('.pyc', '.py'))
        except (ImportError, AttributeError):
            pass
        return caminhos


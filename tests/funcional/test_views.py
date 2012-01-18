# -*- coding: utf-8 -*-
from testutils.test_case import TestCaseTechTudo
from testutils.database_cleaner import DatabaseCleaner
from extensoescore.tests.utils import *
from textAnalysis.views import *
from django.http import HttpRequest
from entidade.tests.utils import criar_entidade
from datetime import datetime, timedelta


class ViewsTest(TestCaseTechTudo):
    
    def after(self):
        pass
    
    def before(self):
        DatabaseCleaner.clean_solr()
        self.editoria = create_folder(slug='artigos',name='artigos')

    def test_alterar_path_de_imagem_pra_prod(self):
        imagem = 'http://anotherdomain.localhost:8000/po/tt/f/90x68/2011/06/29/mw3-bf3_620x258.jpg'
        imagem_prod = 'http://s.glbimg.com/po/tt/f/90x68/2011/06/29/mw3-bf3_620x258.jpg'
        assert alterar_path_imagens(imagem) == imagem_prod
        
    def test_config_nao_existe_nao_retorna_materias(self):
        self.editoria = create_folder(slug='root',uuid='bafad413-9835-4ae9-aa82-6c8a17aa83df')
        params = {
        'colaborador':'79',
        'editorias':  'bafad413-9835-4ae9-aa82-6c8a17aa83df',
        'entidades':  '1035',
        'permalink':  '/xpto/noticia/2011/07/site.html',
        'titulo':     "titulo",
        'subtitulo':  "subtitulo",
        'texto':      "texto", 
        }
        response = self.browser().post('/classify/',params)
        li= self.to_html(response.content).cssselect('li')
        assert response.status_code == 200
        assert len(li) == 1
        assert li[0].text_content().strip() == ''
        
    def test_config_e_false_nao_retorna_materias(self):
        Item.objects.create(nome='usar_saibamais_automatico', valor='False')
        self.editoria = create_folder(slug='root',uuid='bafad413-9835-4ae9-aa82-6c8a17aa83df')
        params = {
        'colaborador':'79',
        'editorias':  'bafad413-9835-4ae9-aa82-6c8a17aa83df',
        'entidades':  '1035',
        'permalink':  '/xpto/noticia/2011/07/site.html',
        'titulo':     "titulo",
        'subtitulo':  "subtitulo",
        'texto':      "texto", 
        }
        response = self.browser().post('/classify/',params)
        li= self.to_html(response.content).cssselect('li')
        assert response.status_code == 200
        assert len(li) == 1
        assert li[0].text_content().strip() == ''

    def test_nao_retorna_materias_porque_nao_tem_materias(self):
        Item.objects.create(nome='usar_saibamais_automatico', valor='True')
        self.editoria = create_folder(slug='root',uuid='bafad413-9835-4ae9-aa82-6c8a17aa83df')
        params = {
        'titulo':     "titulo",
        }
        response = self.browser().post('/classify/',params)
        assert response.status_code == 200
        li= self.to_html(response.content).cssselect('li')
        assert response.status_code == 200
        assert len(li) == 1
        assert li[0].text_content().strip() == ''
    
    def test_retorna_materias_com_proximidade_de_texto(self):
        Item.objects.create(nome='usar_saibamais_automatico', valor='True')
        self.editoria = create_folder(slug='root',uuid='bafad413-9835-4ae9-aa82-6c8a17aa83df')
        i=1
        for texto in ['o gato de botas', 'principe da persia', 'super liga da justiça']:
            m = Materia.objects.create(slug="materia-%s"%i, titulo="materia %s"%i, corpo=texto, status='P', permalink="/noticias/materia-%s"%i)
            RelatedFolder.objects.create(materia=m,is_primary=True,folder=self.editoria)
            m.notifica_barramento("publicar")
            time.sleep(1)
            i+=1
    
        params = {
        'titulo': "super da liga justiça",
        }
        response = self.browser().post('/classify/',params)
        li= self.to_html(response.content).cssselect('li')
        assert response.status_code == 200
        assert len(li) == 1
        assert li[0].text_content().strip() == 'materia 3'
        
        
    def test_extrair_bold_do_form(self):
        post = {
        'titulo': "super herois da liga justiça",
        'texto': "super herois da <p><strong>liga da justiça</strong></p>",
        }
        request = HttpRequest()
        request.POST = post
        documento = extrair_dados_do_form(request)
        assert documento['bold_text'] == ["liga da justiça"]
        
    def test_extrair_editorias_do_form(self):
        editoria1 = create_folder(slug='a',name='a')
        editoria2 = create_folder(slug='b',name='b')
        post = {
        'titulo': "super herois da liga justiça",
        'editorias': '%s,%s' % (editoria1.uuid, editoria2.uuid),
        }
        request = HttpRequest()
        request.POST = post
        documento = extrair_dados_do_form(request)
        assert documento['editorias'] == [editoria1, editoria2]
        
    def test_extrair_entidades_do_form(self):
        ent1 = criar_entidade(slug='a')
        ent2 = criar_entidade(slug='b')
        post = {
        'titulo': "super herois da liga justiça",
        'entidades': '%s,%s' % (ent1.id, ent2.id),
        }
        request = HttpRequest()
        request.POST = post
        documento = extrair_dados_do_form(request)
        assert documento['entidades'] == [ent1,ent2]
        
        
    def test_retorna_materias_com_proximidade_de_data_e_entidade_no_titulo(self):
        Item.objects.create(nome='usar_saibamais_automatico', valor='True')
        self.editoria = create_folder(slug='root',uuid='bafad413-9835-4ae9-aa82-6c8a17aa83df')
        
        m = Materia.objects.create(slug="o-gato-de-botas-1", 
                                    titulo="o gato de botas", 
                                    corpo="<p> esse era um gatinho </p>", 
                                    status='P',
                                    primeira_publicacao = datetime.now()-timedelta(days=5), 
                                    permalink="/noticias/materia-1")
                                    
        RelatedFolder.objects.create(materia=m,is_primary=True,folder=self.editoria)
        m.notifica_barramento("publicar")
        time.sleep(1)
        
        m = Materia.objects.create(slug="o-gato-amarelo-1", 
                                    titulo="o gato de amarelo", 
                                    corpo="<p> esse era um gatinho </p>", 
                                    status='P',
                                    primeira_publicacao = datetime.now()-timedelta(days=3), 
                                    permalink="/noticias/materia-2")
                                    
        RelatedFolder.objects.create(materia=m,is_primary=True,folder=self.editoria)
        m.notifica_barramento("publicar")
        time.sleep(1)

        m = Materia.objects.create(slug="o-sapo-verde-1", 
                                    titulo="o sapo de verde", 
                                    corpo="<p> o gato de azul </p>", 
                                    status='P',
                                    primeira_publicacao = datetime.now()-timedelta(days=1), 
                                    permalink="/noticias/materia-2")
                                    
        RelatedFolder.objects.create(materia=m,is_primary=True,folder=self.editoria)
        m.notifica_barramento("publicar")
        time.sleep(1)

        params = {
        'titulo': "gato",
        }
        response = self.browser().post('/classify/',params)
        li= self.to_html(response.content).cssselect('li')
        assert response.status_code == 200
        assert len(li) == 1
        assert li[0].text_content().strip() == 'o gato de amarelo'
        
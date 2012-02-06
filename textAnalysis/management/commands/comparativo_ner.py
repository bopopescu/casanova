# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from globocore.materia.models import Materia
from textAnalysis.utils import *
from textAnalysis.ner import *

class Command(BaseCommand): 
    
    def handle(self, *args, **options):

        methods = []
        # methods.append(ltask)
        # methods.append(yahoo)
        # methods.append(nltk)
        # methods.append(zemanta)
        methods.append(my_fastercts)
        methods.append(my_fastercts2)

        accuracy={}

        # entidades = [entidade for entidade in entities()][:200]
        
        materias = Materia.objects.filter(corpo__icontains='automatic-premium-tip-semantico')[:1000]
        sentencas = []
        
        for m in materias:
        
            html = lhtml.fromstring(m.corpo.decode('utf-8'))
            tag = [ tag.text for tag in html.cssselect('.automatic-premium-tip-semantico') if tag.text]
            if tag:
                tag = tag[0]
                if len(tag.split())<=3:
                    texto = re.sub(r'<a class="remover">x</a>', r'', m.corpo)
                    texto = unescape(clean_html(texto))
                    posicao = texto.find(tag)
                    ini = texto[:posicao].rfind('.')+1 if texto[:posicao].rfind('.') > -1 else 0 
                    final = posicao+len(tag)
                    fim = texto[final:].find('.')+final+1 if texto[final:].find('.') > -1 else len(texto)
                    sentencas.append((texto[ini:fim].strip(),tag))
        
        # import pdb; pdb.set_trace();

        for (frase,ent) in sentencas:
            ent = clean(ent).lower()
            for method in methods:
                ner = NER(method)
                entidades = []
                try:
                    entidades = ner.processa(frase)
                except:
                    pass
                entidades = [clean(e).lower() for e in entidades]

                if ent in entidades:
                    if accuracy.has_key(method.func_name):
                        accuracy[method.func_name]+=1
                    else:
                        accuracy[method.func_name]=1
                    
                # print "%s => %s - %s" % (method.func_name, ent ,entidades) 
                    
        
        print accuracy
        
        

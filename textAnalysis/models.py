# -*- coding: utf-8 -*-
from django.db import models
from utils import clean
import os
from django.template.defaultfilters import slugify
 
class Dicionario(models.Model):
    nome = models.CharField(max_length=50)
    valor = models.TextField(max_length=50000, null=True, blank=True)

    class Meta:
        verbose_name = u'dicionario'
        db_table = 'dicionario'    

class Folder(models.Model):
    id = models.AutoField(primary_key=True, db_column='folder_id')
    name = models.CharField(db_column='name_txt', unique=True, max_length=255)
    slug = models.CharField(db_column='slug_txt', unique=True, max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    
    class Meta:
        verbose_name = u'folder'
        db_table = 'folder'

    def __unicode__(self):
        return self.name
        
# class Tag(models.Model):
#     id = models.AutoField(primary_key=True, db_column='tag_id')
#     name = models.CharField(db_column='name_txt', unique=True, max_length=255)
# 
#     class Meta:
#         verbose_name = u'tag'
#         db_table = 'tag'
# 
#     def __unicode__(self):
#         return self.name
#         
# class Subject(models.Model):
#     id = models.AutoField(primary_key=True, db_column='subject_id')
#     name = models.CharField(db_column='name_txt', unique=True, max_length=255)
# 
#     class Meta:
#         verbose_name = u'subject'
#         db_table = 'subject'
# 
#     def __unicode__(self):
#         return self.name
# 
# 
# class Entity(models.Model):
#     id = models.AutoField(primary_key=True, db_column='entity_id')
#     name = models.CharField(db_column='name_txt', unique=True, max_length=255)
# 
#     class Meta:
#         verbose_name = u'entity'
#         db_table = 'entity'
# 
#     def __unicode__(self):
#         return self.name


class RelatedFolder(models.Model):
    id = models.AutoField(primary_key=True, db_column='materia_folder_id')
    materia = models.ForeignKey('Materia', related_name='relatedfolder_set')
    folder = models.ForeignKey(Folder)

    class Meta:
        verbose_name = u'folder relacionada'
        db_table = 'materia_folder'
        
# class RelatedTag(models.Model):
#     id = models.AutoField(primary_key=True, db_column='materia_tag_id')
#     materia = models.ForeignKey('Materia', related_name='relatedtag_set')
#     tag = models.ForeignKey(Tag)
#     class Meta:
#         verbose_name = u'tag relacionada'
#         db_table = 'materia_tag'
#                         
# class RelatedSubject(models.Model):
#     id = models.AutoField(primary_key=True, db_column='materia_subject_id')
#     materia = models.ForeignKey('Materia', related_name='relatedsubject_set')
#     subject = models.ForeignKey(Subject)
#     class Meta:
#         verbose_name = u'subject relacionado'
#         db_table = 'materia_subject'
# 
# class RelatedEntity(models.Model):
#     id = models.AutoField(primary_key=True, db_column='materia_entity_id')
#     materia = models.ForeignKey('Materia', related_name='relatedentity_set')
#     entity = models.ForeignKey(Entity)
#     class Meta:
#         verbose_name = u'entity relacionada'
#         db_table = 'materia_entity'


# class Saibamais(models.Model):
#     # materia = models.ForeignKey('Materia' , related_name='materias')
#     materia = models.ForeignKey(Materia , related_name='materias_relacionadas')

    # class Meta:
    #    verbose_name = u'materia relacionada'
    #    db_table = 'saibamais'
    
class Materia(models.Model):
    titulo = models.CharField(u'Título da matéria', max_length=255)
    subtitulo = models.CharField(u'Subtítulo', blank=True, max_length=1000)
    corpo = models.TextField()
    permalink = models.CharField(max_length=1000, blank=True)
    status = models.CharField(u'Status', default="R", max_length=1)
    origem = models.CharField(u'Origem', default="globo", max_length=255)
    fonte = models.CharField(u'Fonte', default="globo", max_length=255)
    slug = models.CharField(u'Slug', max_length=255)
    folders = models.ManyToManyField(Folder, through='RelatedFolder')
    saibamais = models.ManyToManyField('self')
    
    # saibamais = models.ForeignKey(Saibamais, related_name='saibamais')
    
    # tags = models.ManyToManyField(Tag, through='RelatedTag')
    # subject = models.ManyToManyField(Subject, through='RelatedSubject')
    # entity = models.ManyToManyField(Entity, through='RelatedEntity')
    tags = models.CharField(blank=True, max_length=1000)
    subject = models.CharField(blank=True, max_length=1000)
    entity = models.CharField(blank=True, max_length=1000)
    
    class Meta:
        verbose_name = u'materia'
        db_table = 'materia'
        
    def editoria_principal(self):
        return self.relatedfolder_set.get(is_primary=True).folder

    def editorias(self):
        return self.relatedfolder_set.all()
        
    def __str__(self):
        return self.titulo.encode('utf-8')


        
def materia_corpus(categoria, total=30):
    f = Folder.objects.get(name = categoria)
    materias = Materia.objects.filter(relatedfolder_set__is_primary=True, relatedfolder_set__folder=f)
    documents = []
    for materia in materias:
        if len(clean(materia.corpo).split()) > 10:
            documents += [(clean(materia.corpo).split(), categoria)]
        if len(documents) == total:
            break
    # save_to_corpora(categoria, materias)
    return documents
    
def save_to_corpora(categoria,materias):
    categoria = slugify(categoria)
    pasta = "/Users/demetrius/nltk_data/corpora/g1/%s" % categoria
    os.system("rm -rf %s" % pasta) 
    os.system("mkdir %s" % pasta) 
    for (counter, materia) in enumerate(materias):
        f = open('%s/%s.txt' % (pasta,counter),"w") 
        f.write(clean(materia.corpo).encode("utf-8"))
        f.close()
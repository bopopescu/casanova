from django.db import models

class Menu(models.Model):
    title = models.CharField(u'nome', max_length=100)
    def __unicode__(self):
       	return self.title
       	
    def get_instance(self,instancia):
    	return Item.objects.filter(menu=instancia)


class Item(models.Model):
    nome = models.CharField(u'nome', max_length=100)
    link = models.URLField(u'link', max_length=100)
    parent =  models.ForeignKey('self', blank=True, null=True)
    menu =  models.ForeignKey('Menu')
    
    def __unicode__(self):
        if self.parent:
        	return "%s > %s" % (self.parent.nome, self.nome)
        else:
        	return self.nome
    

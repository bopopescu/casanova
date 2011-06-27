from django.db import models

class BoxTexto(models.Model):
    title = models.CharField(u'title', max_length=100)
    texto = models.CharField(u'texto', max_length=400)
    link = models.URLField(u'link', max_length=255)
    leiamais = models.CharField(u'leia mais', max_length=255, blank=True, null=True)    
    link2 = models.URLField(u'link do leia mais', max_length=255, blank=True, null=True)

    def __unicode__(self):
        return u'%s|%s' % (self.id , self.title)

    def get_instance(self,instancia):
    	return BoxTexto.objects.filter(id=instancia)[0]


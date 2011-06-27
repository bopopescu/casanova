from django.db import models

class BoxDestaqueWide(models.Model):
    foto = models.ImageField(u'foto', upload_to='media/fotos', max_length=100, blank=True, null=True)    
    title = models.CharField(u'title', max_length=100)
    texto = models.CharField(u'texto', max_length=400)
    link = models.URLField(u'link', max_length=255)
    leiamais = models.CharField(u'1 leia mais', max_length=255, blank=True, null=True)    
    linkleiamais = models.URLField(u'link do 1 leia mais', max_length=255, blank=True, null=True)
    leiamais2 = models.CharField(u'2 leia mais', max_length=255, blank=True, null=True)    
    linkleiamais2 = models.URLField(u'link do 2 leia mais', max_length=255, blank=True, null=True)    

    def __unicode__(self):
        return u'%s|%s' % (self.id , self.title)

    def get_instance(self,instancia):
    	return BoxDestaqueWide.objects.filter(id=instancia)[0]


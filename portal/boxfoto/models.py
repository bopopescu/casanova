from django.db import models

class BoxFoto(models.Model):
    title = models.CharField(u'chapeu', max_length=100)
    texto = models.CharField(u'texto', max_length=400)
    link = models.CharField(u'link', max_length=255, blank=True, null=True)
    foto = models.ImageField(u'foto', upload_to='media/fotos', max_length=100, blank=True, null=True)    

    def __unicode__(self):
        return u'%s|%s' % (self.id , self.title)

    def get_instance(self,instancia):
    	return BoxFoto.objects.filter(id=instancia)[0]



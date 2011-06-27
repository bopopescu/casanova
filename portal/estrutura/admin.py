from django.contrib import admin
from models import *
from django import forms

modulo = (('',''),)



class ElementoAdmin(admin.ModelAdmin):
    #def formfield_for_dbfield(self, db_field, **kwargs):
    #    if db_field.name == 'nome':
    #        kwargs['widget'] = forms.Select(self,choices=modulo)
    #    return super(ElementoAdmin,self).formfield_for_dbfield(db_field,**kwargs)
    pass

class InstanciaAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'instancia':
            kwargs['widget'] = forms.Select(choices=modulo)
        return super(InstanciaAdmin,self).formfield_for_dbfield(db_field,**kwargs)
    class Media:
        js =['/portal/media/js/jquery-1.3.2.js',
            '/portal/media/js/admin.js',
        ]


admin.site.register(Site)
admin.site.register(Elemento, ElementoAdmin)
admin.site.register(Instancia, InstanciaAdmin)



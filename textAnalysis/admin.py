from django.contrib import admin
from models import *
from django import forms
from django.conf.urls.defaults import patterns, url
from django.http import HttpResponse


class FolderInline(admin.TabularInline):
    model = RelatedFolder

# class TagInline(admin.TabularInline):
#     model = RelatedTag
# 
# class SubjectInline(admin.TabularInline):
#     model = RelatedSubject
#     
# class EntityInline(admin.TabularInline):
#     model = RelatedEntity

class MateriaAdmin(admin.ModelAdmin):
    # form = MateriaAdminForm
    save_on_top = False
    list_display = ('titulo',)
    list_filter = ('folders', )  
    search_fields  = ('titulo','corpo',)
    exclude = ('status','origem','fonte','saibamais', 'subject','entity')
    prepopulated_fields = {'slug': ('titulo',)}

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(MateriaAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ['tags','subject','entity']:
            return forms.CharField(widget=forms.Textarea(), required=False)
        return field

    def classify(self,request):
        from textAnalysis.statistics import extrair_tags
        textos = request.POST.get('titulo') + ' ' + request.POST.get('subtitulo') + ' ' + request.POST.get('texto')
        tags = extrair_tags(textos)
        tags = [ "%s, " % tag for (tag, f) in tags]
        return HttpResponse(tags)
                    
    def get_urls(self):
        urls = super(MateriaAdmin, self).get_urls()
        urls.insert(0, url(r'^classify/$', self.classify))
        return urls

    class Media:
        js = [
            '/m/jquery-1.3.2.min.js',
            '/m/global.js',
        ]
        css = { 'all' : ('/m/global.css',) }
    
    
    # inlines = [
    #     FolderInline, TagInline, SubjectInline, EntityInline,
    # ]

admin.site.register(Materia, MateriaAdmin)


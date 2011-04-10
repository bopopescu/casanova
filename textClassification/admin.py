from django.contrib import admin
from models import *

class TagInline(admin.TabularInline):
    model = RelatedTag
    
class FolderInline(admin.TabularInline):
    model = RelatedFolder

class SubjectInline(admin.TabularInline):
    model = RelatedSubject
    
class EntityInline(admin.TabularInline):
    model = RelatedEntity

class MateriaAdmin(admin.ModelAdmin):
    save_on_top = False
    list_display = ('titulo',)
    list_filter = ('tags','folders', )  
    search_fields  = ('titulo','corpo',)
    exclude = ('status','origem','fonte',)
    prepopulated_fields = {'slug': ('titulo',)}
    
    inlines = [
        FolderInline, TagInline, SubjectInline, EntityInline,
    ]

admin.site.register(Materia, MateriaAdmin)


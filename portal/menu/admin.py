from django.contrib import admin
from models import *


class MenuInline(admin.TabularInline):
    model = Item
    exclude = ("parent",)
    extra = 15
    max_num = 15

class MenuAdmin(admin.ModelAdmin):
	inlines = [
        MenuInline,
    ]	

admin.site.register(Menu, MenuAdmin)


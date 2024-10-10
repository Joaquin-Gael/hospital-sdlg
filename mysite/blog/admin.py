from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title','created_at','subtitle')
    list_filter = ('created_at',)
    search_fields = ('title', 'subtitle')
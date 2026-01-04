from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CareCategory, CareItem

@admin.register(CareCategory)
class CareCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(CareItem)
class CareItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'pet', 'category')
    list_filter = ('category',)

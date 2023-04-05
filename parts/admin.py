from django.contrib import admin
from .models import MotorbikePart, Category, Company
from unidecode import unidecode

# Register your models here.

@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ['name_vn']

    def has_delete_permission(self):
        return False

@admin.register(Company)
class Company(admin.ModelAdmin):
    list_display = ['name_vn']

    def has_delete_permission(self):
        return False

@admin.register(MotorbikePart)
class MotorbikePartAdmin(admin.ModelAdmin):
    list_display = ['name_vn', 'barcode', 'category', 'company', 'price_engineer']
    list_filter = ['category']
    search_fields = ['barcode', 'name_vn', 'name_en']


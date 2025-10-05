from django.contrib import admin
from django import forms
from .models import Category,Product,SubCategory
admin.site.register(Category)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'subcategory', 'price', 'availability')
    list_filter = ('category', 'subcategory', 'availability')
    search_fields = ('name', 'description')

    class Media:
        js = ('js/admin_product_filter.js',)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'slug']  
    list_filter = ['category']  
    search_fields = ['name', 'category__name']  
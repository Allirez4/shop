from django.contrib import admin
from .models import Category,Product,SubCategory
admin.site.register(Category)
admin.site.register(Product)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'slug']  
    list_filter = ['category']  
    search_fields = ['name', 'category__name']  
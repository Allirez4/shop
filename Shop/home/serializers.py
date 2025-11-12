from .models import Product, Category, SubCategory
from rest_framework import serializers

class Catserializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']

class Subcatserializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['name', 'slug']

class Productserializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='subcategory.category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    
    class Meta:
        model = Product  
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'price',
            'count',
            'is_fake',
            'category_name',
            'subcategory_name',
        ]
import decimal
from time import timezone
from rest_framework import serializers
from .serializers import Productserializer
from rest_framework import viewsets,generics
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Product, Category, SubCategory
from .serializers import serializers, Catserializer, Subcatserializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
class custompag(PageNumberPagination):
    page_size=5
    page_query_param='page'
    max_page_size=25
    page_size_query_param='max'
    
class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Product CRUD operations with filtering capabilities.\n
    This ViewSet provides a complete set of CRUD operations for Product objects
    with advanced filtering options including price range and category-based filtering.\n
    Attributes:\n
        queryset: Base queryset with optimized database queries using select_related
                 for subcategory and category relationships.\n
        serializer_class: Serializer class used for Product serialization.\n
        pagination_class: Custom pagination class for controlling response pagination.\n
        permission_classes: Authentication requirement - users must be authenticated.\n
    Query Parameters:
        baseprice (decimal, optional): Minimum price filter for products.
        topprice (decimal, optional): Maximum price filter for products.
        category (str, optional): Filter products by category slug.
        subcategory (str, optional): Filter products by subcategory slug.
                                    Takes precedence over category filter.
    Returns:
        Filtered queryset of Product objects based on provided query parameters.
    Raises:
        ValidationError: When baseprice or topprice parameters contain invalid decimal values.
    Examples:
        GET /products/?baseprice=10.00&topprice=50.00
        GET /products/?category=electronics
        GET /products/?subcategory=smartphones
        GET /products/?baseprice=20.00&subcategory=books
    """
     
    queryset = Product.objects.select_related('subcategory__category')
    serializer_class = Productserializer
    pagination_class=custompag
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        baseprice=self.request.query_params.get('baseprice')
        topprice=self.request.query_params.get('topprice')
        cat=self.request.query_params.get('category')
        subcat=self.request.query_params.get('subcategory')
        queryset=self.queryset
        try:
            if baseprice:
                baseprice=decimal.Decimal(baseprice)
            if topprice:
                topprice=decimal.Decimal(topprice)
        except decimal.InvalidOperation:
            raise ValidationError({"error":"Invalid query parameters"})
        if baseprice and topprice:
            queryset= self.queryset.filter(price__gte=baseprice,price__lte=topprice)
        elif baseprice:
            queryset= self.queryset.filter(price__gte=baseprice)
        elif topprice:
            queryset= self.queryset.filter(price__lte=topprice)
        if subcat:
            queryset=queryset.filter(subcategory__slug=subcat)
        elif cat:
            queryset=queryset.filter(subcategory__category__slug=cat)
               
        return queryset
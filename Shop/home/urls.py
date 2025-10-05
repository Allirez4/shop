from django.urls import path
from . import views
app_name='home'
urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('product_detail/<slug:slug>/',views.ProductDetailView.as_view(),name='product_detail'),
    path('profile/',views.profileView.as_view(),name='profile'),
    path('get-subcategories/', views.get_subcategories, name='get_subcategories'),
    path('<slug:category>/<slug:subcategory>/', views.List_products, name='list_products'),
    path('shop/<slug:category_slug>/', views.List_products, name='name_of_your_product_list_view'),
]

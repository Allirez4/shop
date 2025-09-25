from django.urls import path
from . import views
app_name='home'
urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('product_detail/<slug:slug>/',views.ProductDetailView.as_view(),name='product_detail'),
    path('profile/',views.profileView.as_view(),name='profile'),
]

from django.urls import path
from . import views
app_name='order'
urlpatterns = [
    path('verify/', views.verify, name='verify'),
    path('shoppingcart/',views.View_Cart,name='cart'),
    path('add-to-cart/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/',views.RemoveFromCartView,name='remove_from_cart'),
    path('checkout/',views.CheckoutView.as_view(),name='checkout'),
    path('checkout/submit',views.CheckoutView.as_view(),name='submit'),
]

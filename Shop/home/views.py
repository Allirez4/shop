from django.shortcuts import render
from django.views import View
from .models import Product 
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect
class HomeView(View):
    def get(self,request):
        products=Product.objects.all()
        return render(request,'home/home.html',{'products':products})
class ProductDetailView(View):
    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        return render(request, 'home/product_detail.html', {'product': product})
@method_decorator(login_required, name='dispatch')

class profileView(View):
    def get(self,request):
        user=request.user
        return render(request,'home/profile.html',{'user':user})
    def post(self,request):
        user = request.user
        
        # Update user fields
        user.full_name = request.POST.get('full_name', user.full_name)
        user.email = request.POST.get('email', user.email)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.city = request.POST.get('city', user.city)
        user.address = request.POST.get('address', user.address)
        user.postal_code = request.POST.get('postal_code', user.postal_code)
        user.national_code = request.POST.get('national_code', user.national_code)
        
        try:
            user.save()
            messages.success(request, 'Profile updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
        
        return redirect('home:profile')
from django.shortcuts import render
from django.views import View
from .models import Product 
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse
from .models import Category, SubCategory
from django.core.paginator import Paginator
def get_subcategories(request):
    """
    This view is called by the JavaScript.
    It takes a category_id from the request's GET parameters,
    filters the SubCategory model, and returns the results as JSON.
    """
    category_id = request.GET.get('category_id')
    if category_id:
        subcategories = SubCategory.objects.filter(category_id=category_id).order_by('name')
        # We create a dictionary of {id: name} for the subcategories
        return JsonResponse({sc.id: sc.name for sc in subcategories})
    # If no category_id is provided, return an empty dictionary
    return JsonResponse({})
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
def List_products(request,category_slug,subcategory_slug=None):
    products = Product.objects.select_related('subcategory__category')
    if subcategory_slug:
       products=products.filter(subcategory__slug=subcategory_slug)
    else: 
        products=products.filter(subcategory__category__slug=category_slug)
    paginator = Paginator(products, 12)
    product_count = products.count()
    page_number = request.GET.get('page', 1) # Get page number from URL, default to 1
    page_obj = paginator.get_page(page_number)
    a=True
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        
        
        print(a)
        print('='*99)
        print(page_obj.has_next())
        print(page_obj.object_list)
        print(paginator.count)
        print(paginator.num_pages)
        
        return render(request,'home/products_partial.html',{'products':page_obj.object_list,'has_nextpage':page_obj.has_next()})
    print('aaavvvvvaaaa')    
    return render(request,'home/list_products.html',{'page_obj':page_obj,'products': page_obj.object_list,'products_count':product_count})        
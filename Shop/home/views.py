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
from .forms import profileUpdate as update_form
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
        form=update_form(instance=request.user)
        user=request.user
        return render(request,'home/profile.html',{'user':user,'form':form})
    def post(self,request):
       
        form=update_form(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('home:profile')
                
        else:
             
            messages.error(request, f'Error updating profile: {str(form.errors)}')
            return render(request,'home/profile.html',{'form':form})
        
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
        
        return render(request,'home/products_partial.html',{'products':page_obj.object_list,'has_nextpage':page_obj.has_next()})
    print('aaavvvvvaaaa')    
    return render(request,'home/list_products.html',{'page_obj':page_obj,'products': page_obj.object_list,'products_count':product_count})        
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
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin
from order.models import Order
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank

def search(request):
    user_input = request.GET.get('q', '').strip()
    
    if not user_input:
        return render(request, 'home/search_results.html', {
            'products': [],
            'query': '',
            'count': 0
        })
    
    vector = SearchVector('name', weight='A') + SearchVector('description', weight='B')
    query = SearchQuery(user_input, search_type='plain')
    rank = SearchRank(vector, query)
    
    result = Product.objects.annotate(rank=rank).filter(rank__gte=0.1).order_by('-rank')
    
    # Pagination
    paginator = Paginator(result, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'home/search_results.html', {
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'query': user_input,
        'count': result.count()
    })

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
        paginator=Paginator(products,12)
        page_number=request.GET.get('page',1)
        page_obj=paginator.get_page(page_number)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return render(request,'home/partial_home.html',{'products':page_obj.object_list,'has_nextpage':page_obj.has_next(),'user_id':request.user.id if request.user.is_authenticated else ''})
        
        return render(request,'home/home.html',{'products':page_obj.object_list,'page_obj':page_obj})
class ProductDetailView(View):
    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        return render(request, 'home/product_detail.html', {'product': product})


class profileView(View,LoginRequiredMixin):
    def get(self,request):
        form=update_form(instance=request.user)
        user=request.user
        orders=Order.objects.prefetch_related('items__item').filter(user=user)
        
        return render(request,'home/profile.html',{'user':user,'form':form,'orders':orders})
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
    """
    Display a paginated list of products filtered by category and optionally by subcategory.
    This view handles both regular HTTP requests and AJAX requests to display products.
    Products are filtered based on the provided category_slug and optional subcategory_slug.
    Results are paginated with 12 products per page.
    Args:
        request: The HTTP request object
        category_slug (str): The slug of the category to filter products by
        subcategory_slug (str, optional): The slug of the subcategory to filter products by.
                                        If provided, filters by subcategory instead of category.
    Returns:
        HttpResponse: 
            - For AJAX requests: Renders 'home/products_partial.html' with product list and pagination info
            - For regular requests: Renders 'home/list_products.html' with full page context including
              paginated products, product count, and pagination object
    Context variables:
        - products: List of product objects for the current page
        - page_obj: Paginator page object with pagination methods
        - products_count: Total count of products matching the filter
        - has_nextpage: Boolean indicating if there are more pages (AJAX only)
    """
    products = Product.objects.select_related('subcategory__category')
    if subcategory_slug:
       products=products.filter(subcategory__slug=subcategory_slug)
    else: 
        products=products.filter(subcategory__category__slug=category_slug)
    paginator = Paginator(products, 12)
    product_count = products.count()
    page_number = request.GET.get('page', 1) # Get page number from URL, default to 1
    page_obj = paginator.get_page(page_number)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        
        return render(request,'home/products_partial.html',{'products':page_obj.object_list,'has_nextpage':page_obj.has_next()})
    print('aaavvvvvaaaa')    
    return render(request,'home/list_products.html',{'page_obj':page_obj,'products': page_obj.object_list,'products_count':product_count})   

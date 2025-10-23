from django.shortcuts import render
from django.views import View
from django.contrib import messages
from home.models import Product
from django.shortcuts import redirect
from accounts.models import CustomUser
from .models import Order,OrderItems
from .forms import OrderForm
from django.db import transaction
from decimal import Decimal
from utils import sum_cart
import requests
import json
def add_to_cart(request, product_id):
    if request.method == 'POST':
        print(f"Adding product {product_id} to cart")
        try:
            product = Product.objects.get(id=product_id)
            print(f"Product found: {product.name}")
        except Product.DoesNotExist:
            messages.error(request, "Product not found")
            return redirect('home:home')
        
        cart = request.session.get('cart', {})
        print(f"Current cart before adding: {cart}")
        product_id_str = str(product_id)
        
        if product_id_str in cart:
            cart[product_id_str]['quantity'] += 1
        else:
            cart[product_id_str] = {
                'name': product.name,
                'image': product.image.url if product.image else None,
                'slug': product.slug,
                'unit_price': float(product.price),
                'quantity': 1,
            }
        
        request.session['cart'] = cart
        request.session.modified = True
        
        print(f"Cart after adding: {request.session['cart']}")
        
        messages.success(request, f'"{product.name}" was added to your cart.')
        return redirect(product.get_absolute_url())

def View_Cart(request):
    if request.method == 'GET':
        cart = request.session.get('cart', {})
        #print(f"Cart in View_Cart: {cart}")
        
        # Calculate total
        total = sum_cart(cart)
        
        print(f"Total: {total}")
        #user=dict(request.session)#<----------------------------
        #print(request.user)
        return render(request, 'order/cart.html', {
            'cart': cart,
            'total': total
        })
def RemoveFromCartView(request,product_id):
    product_id=str(product_id)
    if request.method=='POST':
        cart=request.session.get('cart')
        if request.POST.get('override_quantity'):
            cart[product_id]['quantity']=request.POST.get('quantity')
        elif product_id in cart and cart[product_id]['quantity']==1:
            messages.warning(request,f"you removed {cart[product_id]['name']}")
            del cart[product_id]
        else:
            q=int(cart[product_id]['quantity'])
            q-=1
            cart[product_id]['quantity']=str(q)
            messages.warning(request,f"you removed One {cart[product_id]['name']}")
        request.session['cart']=cart
        request.session.modified=True
        return redirect('order:cart')    
class CheckoutView(View):
    
    def get(self,request):
        
        user=request.user
        cart=request.session.get('cart')
        total = sum_cart(cart)
        if not user.address or  not user.national_code or not user.city:
            return redirect('home:profile')
        else:
            return render(request,'order/checkout.html',{'user':user,'itemss':cart,'total':total}) 
    def post(self,request):
        with transaction.atomic():
            
            cart=request.session.get('cart')
            user=request.user
            form=OrderForm(request.POST)
            #form['user']=user
            total = sum_cart(cart)
            if form.is_valid():
                order=form.save(commit=False)
                order.delivery_fee = 5
                order.user=user
                order.save()
                ids=cart.keys()
                products_qs=Product.objects.filter(id__in=ids)
                
                p={product.id : product for product in products_qs}
                for item_id,item_details in cart.items():
                    product=p[int(item_id)]
                    OrderItems.objects.create(order=order,item=product,price_at=int(item_details['unit_price']),quantity=int(item_details['quantity']))
                
                amount=float(total+int((total/10))+5)
                print(f"top amount is {amount}")
                zarin_data={
                    'merchant_id': '7bdcfef3-105c-4281-afbe-d03c06cad0fc',
                    'amount':amount,
                    'callback_url': 'http://127.0.0.1:8000/orders/verify/',
                    'description': f'paying for oder {order.id} by  {order.user.full_name}'
                }
                headers = {"accept": "application/json", "content-type": "application/json"}
                try:
                    response = requests.post(
                    "https://sandbox.zarinpal.com/pg/v4/payment/request.json", 
                    json=zarin_data, 
                    headers=headers, 
                    timeout=10
                    )
                    if response.status_code==200:
                        response_data = response.json()
                        print(f"Zarinpal response: {response_data}")
                        if response_data.get('data', {}).get('code') == 100:
                            authority = response_data.get('data', {}).get('authority')
                            # Save authority to appointment
                            order.authority = authority
                            order.save()
                            messages.success(
                                request,
                            f'going to pay'
                            )
                            
                            return redirect(f"https://sandbox.zarinpal.com/pg/StartPay/{authority}")
                        else:
                            error_code = response_data.get('data', {}).get('code', 'unkown')
                            error_message = response_data.get('data', {}).get('message', 'error unkown')
                            messages.error(
                            request,
                            f'payemnt error code : {error_code} - {error_message}'
                            )
                            raise
                    else:
                        messages.error(
                        request,
                        f'error connecting to payment : {response.status_code}'
                        )      
                except requests.Timeout:
                    messages.error(request,'the request is timed out')
                    raise
                except requests.ConnectionError:
                    messages.error(request,'check your internet connection error')
                    raise
                except Exception as e:
                    messages.error(request,f"unkown error {e}")
                    raise
                #del request.session['cart']         
                return redirect('order:checkout')  
            else:
                return render(request,'order/checkout.html',{'user':user,'itemss':cart,'total':total,'form':form},)
def verify(request):
   
    if request.method=='GET':
        authority=request.GET.get('Authority')
        status=request.GET.get('Status')
        if status and '?' in status:
            status = status.split('?')[0]
        print(status)
        print(authority)
        if status != 'OK' or not authority:
            print("sssssssssssssssssssssssssss")
            messages.error(
                request,
                'payment falied try againg'
            )
            return redirect('order:cart')
    with transaction.atomic():
        order=Order.objects.select_for_update().prefetch_related('items').get(authority=authority)
        items=order.items.all()
        amount=0
        for item in items :
            amount+=item.price_at*item.quantity
        amount=float(amount+int((amount/10))+5)    
            
        if order.is_paid==True:
            return render(request,'order/error.html')
        if not order:
            messages.error(request,'there is no order with this code tryagain')
            return redirect('order:cart')
        else:
            verify_data={
                'merchant_id': '7bdcfef3-105c-4281-afbe-d03c06cad0fc',
                'authority':order.authority,
                'amount':amount
            } 
            headers = {"accept": "application/json", "content-type": "application/json"}
        try:
            response = requests.post(
                "https://sandbox.zarinpal.com/pg/v4/payment/verify.json", 
                json=verify_data, 
                headers=headers)
            if response.status_code == 200:
                    result = response.json()
                    print(f"Verify response: {result}")
                    if result.get('data', {}).get('code') == 100:
                        
                        order.is_paid = True
                        order.save()
                        
                        # Clear the cart after successful payment
                        if 'cart' in request.session:
                            
                            del request.session['cart']
                            
                            request.session.modified = True
                        
                        ref_id = result.get('data', {}).get('ref_id', 'N/A')
                        
                        messages.success(
                        request,
                        'payment was successful'
                        )
                        return render(request, 'order/verify.html', {
                            'order': order,
                            'authority': authority,
                            'ref_id': ref_id,
                            'amount': amount,
                            'status': 'success'
                        })       
                    else:
                        error_message = result.get('errors', {}).get('message', 'unkown error ')
                        messages.error(request, f'payemnt was unsuccessful{error_message}') 
                        raise
            else:
                messages.error(request, f'error in payment varification: {response.status_code}')
                
                raise               
        except Exception as e:
            
            messages.error(request,f'{e} erorr')
            return render(request, 'order/error.html')

    
from django.shortcuts import render,redirect
from .models import Order,OrderItem,Transaction
from cart.models import Cart,CartItem
import json
from django.http import HttpResponse
import requests
from decimal import Decimal



def history(req):
    if req.user.is_superuser:
        order = Order.objects.all()
        transaction = Transaction.objects.all().order_by('timestamp').reverse()
        return render(req,'home/historypage.html',{'order':order,'transactions':transaction})

def customerorderpage(req):
    if req.user.is_authenticated:
        try:
            order = Order.objects.filter(user=req.user).last()
            order_item = OrderItem.objects.filter(order=order)
            if order_item.exists():
                context={'order':order_item}
            else:
                context={'noorder':'you have not order yet'}
        except:
            context={'noorder':'You Currently Have No Order'}
        return render(req,'pay/order.html',context)


def esewapayment(req):
    pass



def khalticheckout(request):
    # URL oF KHALTi
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    if request.method == "GET" and request.user.is_authenticated:
        # Ensure there's a current unpaid order or create a new one
        order, created = Order.objects.get_or_create(user=request.user, is_paid=False, defaults={'total_price': 0})
        
        # Retrieve user's cart and cart items
        cart, cart_created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
        
        if not cart_items:
            return HttpResponse("No items in the cart", status=400)
        
        # Transfer CartItems to OrderItems and calculate total price
        for cart_item in cart_items:
            order_item, item_created = OrderItem.objects.get_or_create(
             order=order,
             food_item=cart_item.food_item,
             defaults={'quantity': cart_item.quantity})
            if not item_created:
                OrderItem.objects.create(order=order, food_item=cart_item.food_item, quantity=cart_item.quantity)

        # Update Order's total_price
        order.total_price = cart.get_all_total
        total_price = float(cart.get_all_total)*100
        order.save()

        # Assuming you have defined return_url and purchase_order_id correctly
        return_url = "http://127.0.0.1:8000/verifyKhalti"  # Example return URL
        purchase_order_id = str(order.purchase_order_id)  # Convert UUID to string

        # Prepare payload for the request
        payload = json.dumps({
            "return_url": return_url,
            "website_url": return_url,
            "amount": total_price,
            "purchase_order_id": purchase_order_id,
            "purchase_order_name": "Order #" + str(order.id),
            "customer_info": {
                "name": 'lall',
                "email": "test@khalti.com",  # Use actual user email
                "phone": "9800000001"  # Use actual user phone
            }
        })
        headers = {
            'Authorization': 'Key live_secret_key_68791341fdd94846a146f0457ff7b455',
            'Content-Type': 'application/json'
        }

        print(payload)
        # Make the POST request to Khalti
        response = requests.post(url, headers=headers, data=payload)
        new_res = response.json()
        print(new_res)
        print(new_res.get('payment_url'))
    
        # Redirect to Khalti payment page
        return redirect(new_res.get('payment_url'))

    # Handle GET request or unauthenticated users
    return HttpResponse("Invalid request", status=400)


def verifyKhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    if request.method == 'GET':
        id = request.GET.get('purchase_order_id')
        status = request.GET.get('status')

        if status == 'Completed':

            headers = {
                'Authorization': 'key live_secret_key_68791341fdd94846a146f0457ff7b455',
                'Content-Type': 'application/json',
            }
            pidx = request.GET.get('pidx')
            print('pidx',pidx)
            data = json.dumps({
                'pidx':pidx
            })
            res = requests.request('POST',url,headers=headers,data=data)
            print('res',res)
            print('res text',res.text)
            new_res = res.json()
            print('new_res',new_res['total_amount'])
            total_amt = Decimal(new_res['total_amount']) / 100

            orderinstance = Order.objects.filter(user=request.user, is_paid=False,purchase_order_id=id).first()
            transaction = Transaction.objects.create(order=orderinstance,
            transaction_id=new_res['transaction_id']
            ,amount=total_amt
            ,status=new_res['status']
            ,paymentid=new_res['pidx'])
            transaction.save()

            if new_res['status']=='Completed':
                orderinstance.is_paid=True
                orderinstance.save()
            
            cart, cart_created = Cart.objects.get_or_create(user=request.user)
            cart_items = cart.items.all()
            cart.items.all().delete()
            
        if status == 'User canceled':
            pass
        return redirect('order')
        
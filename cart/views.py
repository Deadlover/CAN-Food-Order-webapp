from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from home.models import Fooditem,Category,Rating
from cart.models import Cart,CartItem
import json
import requests
from django.http import JsonResponse


@login_required(login_url='Loginpage')
def menupage(request):

    food = Fooditem.objects.all()
    context = {'foodcollection':food}
    return render(request,'home/menu.html',context)


def add_to_cart(request):
    # food_item_id = request.GET.get('id')  # GET
    # food_item_id = request.POST['food_item_id']  # POST

    data = json.loads(request.body)  # Parse JSON data from request body
    food_item_id = data['food_item_id']

    food_item = get_object_or_404(Fooditem, id=food_item_id)
    cart, created = Cart.objects.get_or_create(user=request.user.id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, food_item=food_item)

    if not created:
        cart_item.quantity += 1
        print(cart_item.quantity)

    if food_item.quantity !=0:
        food_item.quantity -=1
        food_item.save()
        cart_item.save()
    else:
        return JsonResponse({'msg':'out of stock'})

    # if food_item.quantity == 0:
    #     food_item.active=False

    return JsonResponse({'msg':'done'})


import uuid
import hashlib
import hmac
import hashlib
import base64

# for cart
@login_required(login_url='Loginpage')
def view_cart(request):
    if request.method=="GET":
        cart = Cart.objects.get(user = request.user.id)
        if CartItem.objects.filter(cart=cart).exists():
            cart_items = CartItem.objects.filter(cart=cart)
            id = uuid.uuid4()
            context = {'cart': cart, 'cart_items': cart_items,'uuid':id}
        else:
            # cart=None
            context={'cart': cart}
        return render(request, 'home/cart.html', context)


import base64


def esewacheckout(request):
    if request.method=="GET":
        # GETTING CART ITEMS
        cart = Cart.objects.get(user = request.user.id)
        cart_items = CartItem.objects.filter(cart=cart)

        # EXTRACTING VALUES
        total_amount = request.GET.get('total_amount')
        uuid = request.GET.get('transaction_uuid')
        amount = request.GET.get('amount')

        # SECRET KEY
        secret_key = "8gBm/:&EnhH.1/q"
        data = f"{total_amount},{uuid},EPAYTEST"
        # data = f"100,11-201-13,EPAYTEST"
        print(data)

# # Encode the hash in Base64
        

        hash = hmac.new(secret_key.encode(), data.encode(), hashlib.sha256).digest()
        result = base64.b64encode(hash).decode()

        print(type(result))

# Create an HMAC SHA256 hash
        print(result)
        context = {
            'cart_product':cart_items,
            'amount': amount,
            'total_amount':total_amount,
            'uuid': uuid,
            'signature': result
        }
        
        return render(request,'home/checkout.html',context)
    

# KHALTI INTEGRATION
  
def Khalticheckout(request):
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    return_url = request.POST.get('return_url')
    purchase_order_id = request.POST.get('purchase_order_id')
    amount = int(float(request.POST.get('amount')) * 100)
    print(return_url)
    print(amount)
    print(purchase_order_id)

    payload = json.dumps({
        "return_url": return_url,
        "website_url": return_url,
        "amount": amount ,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": "test",
        "customer_info": {
        "name": "Ram Bahadur",
        "email": "test@khalti.com",
        "phone": "9800000001"
        }
    })
    headers = {
        'Authorization': 'key live_secret_key_68791341fdd94846a146f0457ff7b455',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

    new_res = json.loads(response.text)

    return redirect(new_res['payment_url'])

def verifyKhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    if request.method == 'GET':
        headers = {
            'Authorization': 'key b885cd9d8dc04eebb59e6f12190ae017',
            'Content-Type': 'application/json',
        }
        pidx = request.GET.get('pidx')
        data = json.dumps({
            'pidx':pidx
        })
        res = requests.request('POST',url,headers=headers,data=data)
        print(res)
        print(res.text)

        new_res = json.loads(res.text)
        print(new_res)
        

        # if new_res['status'] == 'Completed':
        #     # user = request.user
        #     # user.has_verified_dairy = True
        #     # user.save()
        #     # perform your db interaction logic
        #     pass
        
        # # else:
        # #     # give user a proper error message
        # #     raise BadRequest("sorry ")

        # return redirect('home')
    

        


# END OF Integration

def deleteorder(request):
    data = json.loads(request.body)  # Parse JSON data from request body
    food_items = data['food_item_id']
    cartitem_id = data['item_id']
    cart = Cart.objects.get(user = request.user.id)
    food_item = get_object_or_404(Fooditem, id = food_items)
    cart_items = CartItem.objects.get(cart=cart,id=cartitem_id)     # id of cart to match that user and id of cartitem to delete that item only
    print(cart_items.quantity)
    food_item.quantity+=cart_items.quantity
    # food_item.active=True
    food_item.save()
    cart_items.delete()
    return JsonResponse({'msg':'order removed'})

def update_item(request):
    data = json.loads(request.body)  # Parse JSON data from request body
    food_id = data['food_item_id']

    food_item = get_object_or_404(Fooditem, id=food_id)
    cart, created = Cart.objects.get_or_create(id=request.user.id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, food_item=food_item)

    if food_item.quantity == 0:
        return JsonResponse({'msg':'out of stock'})
    
    if not created:
        food_item.quantity -=1
        cart_item.quantity += 1

        print(food_item.quantity)
        food_item.save()
        cart_item.save()
        return JsonResponse({'msg':'added','quantity':cart_item.quantity})

def remove_item(request):
    data = json.loads(request.body)  # Parse JSON data from request body
    food_id = data['food_item_id']
    food_item = get_object_or_404(Fooditem, id=food_id)
    cart, created = Cart.objects.get_or_create(user=request.user.id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, food_item=food_item)


    if not created:
        food_item.quantity +=1
        cart_item.quantity -= 1
        cart_item.save()

    if not created:
        if cart_item.quantity == 0:
            cart_item.delete()
        
    # if food_item.quantity == 1:
    #     food_item.active=True

    food_item.save()
    return JsonResponse({'msg':'subbed','quantity':cart_item.quantity})
    # return JsonResponse({'msg':'subbed','quantity':order_item.quantity,'price':food_item.price}) # to send price too but too much load so used js


def search(request):
    if request.method == 'GET':
        data = request.GET['search']
        try:
            food = Fooditem.objects.filter(Name__icontains=data).order_by('id')
            if food.exists():
                context = {'foodcollection':food}
            else:
                context = {'food':'Item Not found'}
        except:
            context = {'food':'Item Not  found'}
        print(food.exists())
        return render(request,'home/menu.html',context)
    


def filter(request,option):
    if request.method=='GET':
        try:
            category = Category.objects.get(name=option)
            food = Fooditem.objects.filter(category=category.id)
            context = {'foodcollection':food,'category':category.id}
        except:
            context ={'food':'There is no such items'}
        return render(request,'home/menu.html',context)


def fooddetail(req,foodid):
    if foodid is not None:
        food = Fooditem.objects.get(id=foodid)
        rating = Rating.objects.filter(food_item=food).order_by('-id')[:4]
        return render(req,'home/detailfoodpage.html',{'fooditem':food,'review':rating})
    
def review(req):
    if req.method=='POST':
        data = json.loads(req.body)
        rate = data['rating']
        comment = data['comment']
        foodid = data['foodid']
        food = Fooditem.objects.get(id=foodid)
        existuser = Rating.objects.filter(user=req.user, food_item=food).first()
        if existuser:
            if rate is not None:
                existuser.score= rate
            if comment is not None:
                existuser.review= comment
            existuser.save()
            return

        if rate or comment is not None:
            rating = Rating.objects.create(user=req.user,food_item=food,score=rate,review=comment)
            rating.save()

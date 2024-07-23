from django.shortcuts import render,HttpResponse,redirect
from .models import Fooditem,Rating
from cart.models import Cart
from .forms import CreateFood,CreateCategory
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash


# creating my own filter
from django.template.defaulttags import register
@register.filter
def get_range(value):
    return range(value)


# @login_required(login_url='Loginpage') #give name of url that u want to show when not logged in.
def homepage(request):
    if request.user.is_authenticated:
        cart,created = Cart.objects.get_or_create(user=request.user)
        food = Fooditem.objects.all()
        user =request.user
        name =request.user.first_name
        context = {'name':name,'foodcollection':food}
        return render(request,'home/home.html',context)
    else:
        return render(request,'home/home.html')


# CURD of Food item
def uploadpage(request):
    if request.user.is_superuser:
        
        return render(request,'home/addproduct.html')
    
def fooduploadpage(request):
    if request.user.is_superuser:
        insert=CreateFood()
        if request.method=='POST':
            insert = CreateFood(request.POST,request.FILES)
            if insert.is_valid():
                insert.save()
                return redirect('upload')
            else:
                return HttpResponse("pls fill value correctly")

        return render(request,'home/uploadform.html',{'insert':insert})
    else:
        return render(request,'home/no.html')


def categoryuploadpage(request):
    if request.user.is_superuser:
        insert=CreateCategory()
        if request.method=='POST':
            insert = CreateCategory(request.POST,request.FILES)
            if insert.is_valid():
                insert.save()
                return redirect('upload')
            else:
                return HttpResponse("pls fill value correctly")

        return render(request,'home/uploadform.html',{'insert':insert})
    else:
        return render(request,'home/no.html')



# FOR edit delete IN editmenu OF FOOD
def editmenupage(request):
    if request.user.is_superuser:
        food = Fooditem.objects.all()
        context = {'foodcollection':food}
        return render(request,'home/editmenu.html',context)
    else:
        return render(request,'home/no.html')


def update(request,food_id):
    food_id= int(food_id)
    try:
        food_shelf= Fooditem.objects.get(id=food_id)
    except Fooditem.DoesNotExist:
        return redirect('Home')
    food_form=CreateFood(request.POST or None,instance=food_shelf)
    if food_form.is_valid():
        food_form.save()
        return redirect('Home')
    return render(request,'home/uploadform.html',{'insert': food_form})


def Delete(request,food_id):
    food_id=int(food_id)
    try:
        food_shelf=Fooditem.objects.get(id=food_id)
    except Fooditem.DoesNotExist:
        return redirect('Home')
    food_shelf.delete()
    return redirect('Home')


# for contactpage
def contactpage(request):
    return render(request,'home/contact.html')


# for menu and to add item to cart         

def commentPage(req):
    if req.user.is_superuser:
        food = Fooditem.objects.all()
        rating = Rating.objects.all()
        return render(req,'home/commentpage.html',{'rating':rating,'food':food})
    


# Setting page

def Settingpage(request,Whatchange):
    if request.user.is_authenticated:
        if request.method=='GET':
            if Whatchange=='Name':
                context={'form':'Name'}

            if Whatchange=='Profile':
                context={'form':'Profile'}

            if Whatchange=='Email':
                context={'form':'Email'}

            if Whatchange=='Password':
                context={'form':'Password'}
            
            if Whatchange=='Delete':
                context={'form':'Delete'}
            
            context['id']= request.user.id

            return render(request,'home/Setting.html',context)
        
        if request.method=='POST':
            if Whatchange=='Name':
                fname = request.POST.get('firstname')
                lastname = request.POST.get('lastname')
                if fname and lastname:
                    user = request.user
                    user.first_name=fname
                    user.last_name=lastname
                    user.save()
                    return redirect('Home')


            elif Whatchange=='Profile':
                image = request.FILES.get('image')  # Get the uploaded image from the form data
                user = request.user
                if image:  # Check if an image was uploaded
                    user.profile_picture = image  # Update the profile_picture field
                    user.save()  # Save the changes to the database
                    messages.success(request, 'Profile picture updated successfully.')
                    return redirect('Home')  # Adjust as needed
                else:
                    messages.error(request, 'Please upload a valid image.')
                    return redirect('Home')

            elif Whatchange=='Email':
                user = request.user
                new_email = request.POST.get('email')  # Get the new email from the form data
                if new_email:  # Check if the new email is provided
                    user.email = new_email  # Update the email field
                    user.save()  # Save the changes to the database
                    messages.success(request, 'Email updated successfully.')
                    return redirect('Home')  # Adjust as needed
                else:
                    messages.error(request, 'Please provide a valid email.')

            elif Whatchange=='Password':
                current_password = request.POST.get('current_password')
                new_password = request.POST.get('new_password')
                confirm_new_password = request.POST.get('confirm_new_password')

                if not request.user.check_password(current_password):
                    # The current password is not correct
                    messages.error(request, 'Current password is incorrect.')
                    return redirect('Home')  # Adjust as needed

                if new_password != confirm_new_password:
                    # The new password and its confirmation do not match
                    messages.error(request, 'New passwords do not match.')
                    return redirect('Home')  # Adjust as needed

                # Everything's good; change the password
                user = request.user
                user.set_password(new_password)
                user.save()

                # Updating the session with the new password hash to keep the user logged in
                update_session_auth_hash(request, user)
                return redirect('Home')

        return render(request,'home/Setting.html',context)


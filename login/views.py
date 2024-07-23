from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from .models import CustomUser


def loginPage(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass']
        user = authenticate(request,email=email,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('Home')
        else:
            return  HttpResponse("Username or password is incorrect!!")
        
    return render(request, 'login/Loginpage.html')

def SignupPage(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lastname = request.POST['lname']
        email = request.POST['email']
        address = request.POST['add']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if pass1 != pass2:
            return HttpResponse("confirm password doesn't match")
        elif len(pass1)<4:
            return HttpResponse("password length should be atleast 8 or more character")
        else:
            newuser = CustomUser.objects.create_user(first_name=fname,last_name=lastname,email=email,address=address,password=pass1)
            newuser.save()
            return redirect('Loginpage')
        
    return render(request, 'login/SignUp.html')

def LogoutPage(request):
    logout(request)
    return redirect('Loginpage')

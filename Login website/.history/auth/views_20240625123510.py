from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
# Create your views here.
def home(request):
    return render(request, "auth/index.html")
def signup(request):
    
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        myuser = User.objects.create_user(username ,email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        
        myuser.save()
        
        messages.success(request ,"Your Account As Been Created Successfully")
        
        return redirect('signin')
    return render(request, "auth/signup.html")



def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(request, username=username, password=pass1)
        
        if user is None:
            login(request, user)
            messages.success(request, f"Welcome, {user.first_name}!")
            return redirect('')
        
        else:
            messages.error(request, "Bad credentials!")
            return redirect('signin')
    return render(request, "auth/signin.html")


def signout(request):
    return render(request, "auth/signin.html")
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
        name = request.POST['name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        myuser = User.objects.create_user(username ,email, pass1)
        myuser.first_name= name
        
        myuser.save()
        
        messages.success(request ,"Your Account As Been Created Successfully")
        
        return redirect('signin')
    return render(request, "auth/signup.html")
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is None:
            login(request,user)
            name = user.first_name
            return render(request, "auth/index.html", {'name': name})
        else:
            messages.error(request, "Bad credentials!")
            return redirect('home')
    return render(request, "auth/signin.html")
def signout(request):
    pass
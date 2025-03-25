from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
def home(request):
    return render(request, "auth/index.html")
def signup(request):
    if request.method == "POST":
        username = request.post['username']
        name = request.post['name']
        email = request.post['email']
        pass1 = request.post['pass1']
        pass2 = request.post['pass2']
        
        myuser = User.objects.create_user(username ,email, pass1)
        myuser.first_name= name
        
        myuser.save()
        
        messages.success(request ,"Your Account As Been Created Successfully")
        
        return redirect('signin')
    return render(request, "auth/signup.html")
def signin(request):
    return render(request, "auth/signin.html")
def signout(request):
    pass
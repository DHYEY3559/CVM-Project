from django.shortcuts import render
from django.http import HttpResponse
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
        
    
    
    
    
    
    
    
    
    
    
    
    
    return render(request, "auth/signup.html")
def signin(request):
    return render(request, "auth/signin.html")
def signout(request):
    pass
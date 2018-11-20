from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *

# Create your views here.
def index(request):
	context = {
	   "typesOfPizza": TypeOfPizza.objects.all(),
	   "pizzas": Pizza.objects.all(),
	   "pastas": Pasta.objects.all(),
	   "salads": Salad.objects.all(),
	   "dinners": Dinner.objects.all(),
	   "user": request.user.is_authenticated,
	   "subs": Sub.objects.all()
    }
    

	return render(request, "orders/index.html", context)
	

def auth_register(request):
	if request.method == "GET":
		return render(request, "orders/register.html")
	else:
		username = request.POST["username"]
		email = request.POST["email"]
		password = request.POST["password"]
		first_name = request.POST["first_name"]
		last_name = request.POST["last_name"]
		user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
		if request.user.is_authenticated:
			logout(request)
		return HttpResponseRedirect(reverse("login"))


def auth_login(request):
	if request.method == "GET":
		if not request.user.is_authenticated:
			return render(request, "orders/login.html")
		else:
			return HttpResponseRedirect(reverse("index"))
	if request.method == "POST":
		try:
			username = request.POST["username"]
			password = request.POST["password"]
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return HttpResponseRedirect(reverse("index"))
			else:
				return render(request, "orders/login.html", {"message": "Invalid credentials"})
		except Exception as e:
			return render(request, "orders/login.html", {"message": str(e)})
		

def auth_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

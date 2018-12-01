from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json

import pdb

from .models import *

# Create your views here.
def index(request):

	if not request.session.has_key('pizza'):
		request.session['pizza'] = []
	
	if not request.session.has_key('dinner'):
		request.session['dinner'] = []
	
	if not request.session.has_key('sub'):
		request.session['sub'] = []
	
	if not request.session.has_key('pasta'):
		request.session['pasta'] = []
	
	if not request.session.has_key('salad'):
		request.session['salad'] = []
	
	pizzas = []
	for dic in request.session['pizza']:
		pizzas.append(int(list(dic)[0]))
	
	dinners = []
	for dic in request.session['dinner']:
		dinners.append(int(list(dic)[0]))
	
	subs = []
	for dic in request.session['sub']:
		subs.append(int(list(dic)[0]))
	
	pastas = []
	for dic in request.session['pasta']:
		pastas.append(int(list(dic)[0]))
	
	salads = []
	for dic in request.session['salad']:
		salads.append(int(list(dic)[0]))

	items = {"pizza": pizzas, "dinner": dinners, "sub": subs, "pasta": pastas, "salad": salads }
	
	context = {
	   "typesOfPizza": TypeOfPizza.objects.all(),
	   "pizzas": Pizza.objects.all(),
	   "pastas": Pasta.objects.all(),
	   "salads": Salad.objects.all(),
	   "dinners": Dinner.objects.all(),
	   "user": request.user.is_authenticated,
	   "items": items,
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
			return render(request, "orders/login.html", {"user": request.user.is_authenticated})
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


@csrf_exempt
def add_item(request):
	try:
		price_id = request.GET["price_id"]
		item = request.GET["item"]
		# Saving the items added in the shopping cart in a tuple ItemId: Type(e.g. pizza)
		if not request.session.has_key(item):
			request.session[item] = []

		items = request.session[item][:]
		items.append({price_id: 1})
		request.session[item] = items;

		return HttpResponse(f"{item} - {request.session[item]}")
	
	except Exception as e:
		return HttpResponse("Failure!", {"success": False})


@csrf_exempt
def edit_quantity(request):
	try:
		price_id = request.GET["price_id"]
		item = request.GET["item"]
		old_quantity = request.GET["old_quantity"]
		new_quantity = request.GET["new_quantity"]
		# Saving the items added in the shopping cart in a tuple ItemId: Type(e.g. pizza)
		if not request.session.has_key(item):
			request.session[item] = []

		items = request.session[item][:]
		items.remove({price_id: int(old_quantity)})
		items.append({price_id: int(new_quantity)})
		request.session[item] = items;

		return HttpResponse(f"{item} - {request.session[item]}")
	
	except Exception as e:
		return HttpResponse("Failure!", {"success": False})

@csrf_exempt
def remove_item(request):
	try:
		price_id = request.GET["price_id"]
		item = request.GET["item"]
		# Saving the items added in the shopping cart in a tuple ItemId: Type(e.g. pizza)
		if not request.session.has_key(item):
			request.session[item] = []

		items = request.session[item][:]
		value = 0
		for i in range(len(items)):
			if list(items[i])[0] == price_id:
				quantity = items[i][list(items[i])[0]]
				del items[i]
				request.session[item] = items;
				return HttpResponse(quantity)

		return HttpResponse(f"{item} - {items}")
	
	except Exception as e:
		return HttpResponse(f"Failure! {str(e)} - {items}", {"success": False})


def cart(request):

	# Checking if the key item exist in the session 
	if not request.session.has_key('pizza'):
		request.session['pizza'] = []

	if not request.session.has_key('dinner'):
		request.session['dinner'] = []
	
	if not request.session.has_key('sub'):
		request.session['sub'] = []
	
	if not request.session.has_key('pasta'):
		request.session['pasta'] = []
	
	if not request.session.has_key('salad'):
		request.session['salad'] = []

	if not request.session.has_key('progress'):
		request.session['progress'] = "cart"
	
	if not request.session.has_key('address'):
		
		request.session['address'] = {
					"street_name": "",
					"street_number": "",
					"apartment": "",
					"reference": "",
					"postal_code": "",
					"neighborhoor": "",
					"state": "",
					"city": ""
		}

	pizzas_aux = {}
	for dic in request.session['pizza']:
		pizzas_aux[list(dic)[0]]=dic[list(dic)[0]]
	
	dinners_aux = {}
	for dic in request.session['dinner']:
		dinners_aux[list(dic)[0]]=dic[list(dic)[0]]
	
	subs_aux = {}
	for dic in request.session['sub']:
		subs_aux[list(dic)[0]]=dic[list(dic)[0]]
	
	pastas_aux = {}
	for dic in request.session['pasta']:
		pastas_aux[list(dic)[0]]=dic[list(dic)[0]]
	
	salads_aux = {}
	for dic in request.session['salad']:
		salads_aux[list(dic)[0]]=dic[list(dic)[0]]

	total = 0
	# Getting all elements of type pizzas 
	pizzas = []
	for pizza in list(pizzas_aux):
		try:
			order = PriceOfPizza.objects.get(pk=pizza)
			pizzas.append((order, pizzas_aux[pizza]))
			total += order.price * pizzas_aux[pizza]
		except PriceOfPizza.DoesNotExist:
			raise Http404("Item in the order does not exist")
	
	# Getting all elements of type dinner 
	dinners = []
	for dinner in dinners_aux:
		try:
			order = PriceOfDinner.objects.get(pk=dinner)
			dinners.append((order, dinners_aux[dinner]))
			total += order.price * dinners_aux[dinner]
		except PriceOfDinner.DoesNotExist:
			raise Http404("Item in the order does not exist")

	# Getting all elements of type sub 
	subs = []
	for sub in subs_aux:
		try:
			order = PriceOfSub.objects.get(pk=sub)
			subs.append((order, subs_aux[sub]))
			total += order.price * subs_aux[sub]
		except PriceOfSub.DoesNotExist:
			raise Http404("Item in the order does not exist")

	# Getting all elements of type pasta 
	pastas = []
	for pasta in pastas_aux:
		try:
			order = Pasta.objects.get(pk=pasta)
			pastas.append((order, pastas_aux[pasta]))
			total += order.price * pastas_aux[pasta]
		except Pasta.DoesNotExist:
			raise Http404("Item in the order does not exist")
	
	# Getting all elements of type salad 
	salads = []
	for salad in salads_aux:
		try:
			order = Salad.objects.get(pk=salad)
			salads.append((order, salads_aux[salad]))
			total += order.price * salads_aux[salad]
		except Salad.DoesNotExist:
			raise Http404("Item in the order does not exist")

	address = request.session['address']
	progress = request.session['progress']
	if progress == "finished":
		request.session['progress'] = "cart"
	context = {
				"pizzas": pizzas,
				"dinners": dinners,
				"subs": subs,
				"pastas": pastas,
				"salads": salads,
				"total": total,
				"toppings": Topping.objects.all(),
				"progress": progress,
				"address": address,
	   			"user": request.user.is_authenticated
			}
	return render(request, "orders/cart.html", context)

def update_progress(request):

	try:
		# Progress is Cart -> Place Order -> Details -> Payment
		
		#pdb.set_trace()
		operation = request.GET["operation"]
		progress = request.GET["progress"]
		if operation == "next":
			if progress == "cart":
				# Go to next step "place"
				request.session['progress'] = "place-order"

			if progress == "place-order":
				
				address = {
					"street_name": request.GET["street_name"],
					"street_number": request.GET["street_number"],
					"apartment": request.GET["apartment"],
					"reference": request.GET["reference"],
					"postal_code": request.GET["postal_code"],
					"neighborhoor": request.GET["neighborhoor"],
					"city": request.GET["city"],
					"state": request.GET["state"]
				} 
				request.session['address'] = address
				request.session['progress'] = "finish"

		if operation == "previous":
			if progress == "place-order":
				request.session['progress'] = "cart"

			if progress == "finish":
				request.session['progress'] = "place-order"
		#pdb.set_trace()
		return HttpResponse("success")

	except Exception as e:
		return HttpResponse(f"Failure! {str(e)} - {items}", {"success": False})


@csrf_exempt
def submit_order(request):

	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse("auth_login"))

	items = json.loads(request.POST.get('items'))
	items_order = []
	total = 0.0
	order = Order(status_order="SUBMITTED", user=request.user, total=total)
	for item in items:
		i = PriceOfPizza.objects.get(pk=item['key'])
		description = f"{i.pizza.name} - {i.sizeOfPizza.size.name} Size - Toppings: "
		for topping in item['value']:
			t = Topping.objects.get(pk=topping)
			description += f" | {t.name} |"
		total += float(i.price)
		item_order=  ItemOrder(description=description, quantity=1, price=i.price)
		items_order.append(item_order)

	if not request.session.has_key('dinner'):
		request.session['dinner'] = []
	
	if not request.session.has_key('sub'):
		request.session['sub'] = []
	
	if not request.session.has_key('pasta'):
		request.session['pasta'] = []
	
	if not request.session.has_key('salad'):
		request.session['salad'] = []
	
	
	for d in request.session['dinner']:
		i = PriceOfDinner.objects.get(pk=list(d)[0])
		total += float(i.price)*int(d[list(d)[0]])
		description = f"Dinner - {i.dinner.name} - {i.size.name} Size"
		item_order=  ItemOrder(description=description, quantity=d[list(d)[0]], price=i.price*int(d[list(d)[0]]))
		items_order.append(item_order)

	for d in request.session['pizza']:
		i = PriceOfPizza.objects.get(pk=list(d)[0])
		if not i.pizza.custom:
			total += float(i.price)*int(d[list(d)[0]])
			description = f"Pizza - {i.pizza.name} - {i.sizeOfPizza.size.name} Size"
			item_order=  ItemOrder(description=description, quantity=d[list(d)[0]], price=i.price*int(d[list(d)[0]]))
			items_order.append(item_order)

	for d in request.session['sub']:
		i = PriceOfSub.objects.get(pk=list(d)[0])
		total += float(i.price)*int(d[list(d)[0]])
		description = f"Sub - {i.sub.name} - {i.size.name} Size"
		item_order=  ItemOrder(description=description, quantity=d[list(d)[0]], price=i.price*int(d[list(d)[0]]))
		items_order.append(item_order)
	
	for d in request.session['pasta']:
		i = Pasta.objects.get(pk=list(d)[0])
		total += float(i.price)*int(d[list(d)[0]])
		description = f"Pasta - {i.name}"
		item_order=  ItemOrder(description=description, quantity=d[list(d)[0]], price=i.price*int(d[list(d)[0]]))
		items_order.append(item_order)

	for d in request.session['salad']:
		i = Salad.objects.get(pk=list(d)[0])
		total += float(i.price)*int(d[list(d)[0]])
		description = f"Salad - {i.name}"
		item_order=  ItemOrder(description=description, quantity=d[list(d)[0]], price=i.price*int(d[list(d)[0]]))
		items_order.append(item_order)


	order.total = total

	order.save()

	for i in items_order:
		i.order = order
		i.save()
	#pdb.set_trace()

	request.session['progress'] = "finished"
	
	request.session['dinner'] = []
	request.session['pizza'] = []
	request.session['sub'] = []
	request.session['salad'] = []
	request.session['pasta'] = []
	
	return HttpResponse("success")

def orders(request):

	orders = request.user.orders

	context = {
		"orders": orders
	}
	return render(request, "orders/orders.html", context)
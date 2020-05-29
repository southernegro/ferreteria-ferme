from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import json
import datetime
from .models import *
from .forms import CreateUserForm

def registerPage(request):
	form = CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, 'Cuenta creada con éxito para ' + user)
			return redirect('login')

	context = {'form':form}
	return render(request, 'accounts/register.html', context)

def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('')
		else:
			messages.info('Usuario o Contraseña incorrectos')
	context= {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('')


def store(request):
	if request.user.is_authenticated:
		tipo = request.user.profile.tipo
		if(tipo == 'Administrator' or tipo == 'Cliente' or tipo == 'Vendedor'):
			usuario = request.user.profile
			order, created = Order.objects.get_or_create(usuario=usuario, complete=False)
			items = order.orderitems_set.all()
			cartItems = order.get_cart_items
		elif(tipo == 'Empleado' or tipo == 'Proveedor'):
			items = []
			order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
			cartItems = order['get_cart_items']
	else:
		#Create Empty cart for now for none-logged in users
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']
	
	products = Producto.objects.all()
	context = {'products': products, 'cartItems': cartItems}
	return render(request, 'store/store.html', context)

def cart(request):

	if request.user.is_authenticated:
		usuario = request.user.profile
		order, created = Order.objects.get_or_create(usuario=usuario, complete=False)
		items = order.orderitems_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']
		
	context = {'items':items, 'order':order, 'cartItems': cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	if request.user.is_authenticated:
		usuario = request.user.profile
		order, created = Order.objects.get_or_create(usuario=usuario, complete=False)
		items = order.orderitems_set.all()
		cartItems = order.get_cart_items
	else:
		#Create Empty cart for now for none-logged in users
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	context = {'items':items, 'order':order, 'cartItems': cartItems}
	return render(request, 'store/checkout.html', context)

def updateItems(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	print('Action:', action)
	print('productId:', productId)

	usuario = request.user.profile
	product = Producto.objects.get(id=productId)
	order, created = Order.objects.get_or_create(usuario=usuario, complete=False)

	orderItems, created = OrderItems.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItems.quantity = (orderItems.quantity + 1)
	elif action == 'remove':
		orderItems.quantity = (orderItems.quantity - 1)
	
	orderItems.save()

	if orderItems.quantity <= 0:
		orderItems.delete()

	return JsonResponse('Producto agregado', safe=False)

def processOrder(request):
	#print('Data:', request.body)
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		usuario = request.user.profile
		order, created = Order.objects.get_or_create(usuario=usuario, complete=False)
		total  = float(data['form']['total'])
		order.transaction_id = transaction_id

		if total == order.get_cart_total:
			order.complete = True
		order.save()

		if order.shipping == True:
			ShippingAddress.objects.create(
				usuario=usuario,
				order=order,
				address=data['shipping']['address'],
				city=data['shipping']['city'],
				state=data['shipping']['state'],
				zipcode=data['shipping']['zipcode'],
			)
	else:
		print('Usuario no registrado')
	return JsonResponse('Pago realizado', safe=False)


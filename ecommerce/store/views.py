from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import json
import datetime
from .models import *
from django_tables2 import SingleTableView
from .tables import ProfileTable
from .forms import  ProfileForm, CustomUserForm, ClientForm, ProductoForm
from .utils import cookieCart, cartData, guestOrder

#def registerPage(request):
#    data = {
#        'form': CustomUserForm(),
#        'profile': ProfileForm()
#    }
#    if request.method == 'POST':
#        formulario = CustomUserForm(request.POST)
#        profile_form = ProfileForm(request.POST)
#        
#        if formulario.is_valid() and profile_form.is_valid():
#            new_user = formulario.save()
#            profile = profile_form.save(commit=False)
#            profile.user = new_user
#            profile.save()
#            #autenticar el usuario y redirigirlo
#            username=formulario.cleaned_data['username']
#            password=formulario.cleaned_data['password1']
#            #autentificamos credenciales del usuario
#            user = authenticate(username=username, password=password)
#            #logueamos el usuario
#            login(request, user)
#
#            return redirect('')
#            
#        data['form']=formulario
#        data['profile']=profile_form
#
#    return render(request, 'accounts/register.html', data) 


def users(request):
    users = Profile.objects.all()
    table_class = ProfileTable
    context = {'users':users, 'table':table_class}
    return render(request, 'admin/users.html', context)

def registerPage(request):
    data = {
       'form': CustomUserForm(),
        'profile': ProfileForm(),
        'client': ClientForm()
    }
    if request.method=='POST':
        form = CustomUserForm(request.POST)
        profile = ProfileForm(request.POST)
        client = ClientForm(request.POST)
        if form.is_valid() and profile.is_valid():
            new_user = form.save()
            profile = profile.save(commit=False)
            profile.user = new_user
            profile.save()
            #if client.is_valid():
            client = client.save(commit=False)
            client.profile = profile
            client.save() 
            #autenticar el usuario y redirigirlo
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            #autentificamos credenciales del usuario
            user = authenticate(username=username, password=password)
            #logueamos el usuario
            login(request, user)
            return redirect(to='store')
        data['form']=form
        data['profile']=profile
    return render(request, 'accounts/register.html', data)


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

    data = cartData(request)
    cartItems = data['cartItems']
    
    products = Producto.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
    context = {'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
        
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

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

def processOrder(request): #TODO: Revisar porque la orden de compra no se guarda como completada
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        usuario = request.user.profile
        order, created = Order.objects.get_or_create(usuario=usuario, complete=False)
        #order = Order.objects.create(
        #usuario=usuario,
        #complete=True,
        #transaction_id=transaction_id
        #)
        
        #VER LUEGO 
        #boleta = Boleta.objects.get_or_create(
        #order=order,
        #n_boleta=transaction_id
        #)
    else:
       usuario, order = guestOrder(request, data)

    total  = float(data['form']['total'])
    order.transaction_id = transaction_id
    print(order.transaction_id)

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
    #cart = {}
    return JsonResponse('Pago realizado', safe=False)

def adm_productos(request):
    return render(request, 'store/adm-producto.html', {})

def agregar_producto(request):
    data={
    'form': ProductoForm()
    }
    if request.method=='POST':
        formulario = ProductoForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            #formulario = formulario.save(commit=False)
            #formulario.user = request.user
            formulario.save()
            data['mensaje']='Producto agregado con éxito'
        data['form']=formulario
    return render(request, 'store/agregar-producto.html', data)


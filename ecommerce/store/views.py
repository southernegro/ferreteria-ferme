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
from .forms import  ProfileForm, CustomUserForm, ClientForm, ProductoForm, SellerForm, EmployeeForm, SupplierForm, BoletaForm, OrdenCompraForm
from .utils import cookieCart, cartData, guestOrder
import django_tables2 as tables



#Listado Usuarios
def listUser(request):
    users = Profile.objects.all()
    data={
        'users': users
    }
    return render(request, 'admin/listado_usuarios.html', data)

#Eliminar usuario desde tabla
def deleteUser(request, pk):
    user = User.objects.get(pk=pk)
    perfil = Profile.objects.get(user_id=pk)
    user.delete()
    perfil.delete()
    return redirect(to='listado_usuarios')

#Editar usuario desde tabla
def editUser(request, pk):
    usuario = User.objects.get(pk=pk)
    perfil = Profile.objects.get(user_id=pk)
    data = {
        'form': CustomUserForm(instance=usuario),
        'profile': ProfileForm(instance=perfil)
    }
    if request.method == 'POST':
        formulario = CustomUserForm(data=request.POST, instance=usuario)
        profile = ProfileForm(data=request.POST, instance=perfil)
        if formulario.is_valid():
            formulario.save()
            profile.save()
            data['mensaje']='Usuario modificado correctamente'
            login(request, usuario)
            return redirect(to='listado_usuarios')
        data['form']=CustomUserForm(instance=User.objects.get(pk=pk))
        data['profile']=ProfileForm(instance=perfil)
    return render(request,'admin/edit_user.html', data)

#Editar Producto
def editProductPage(request, id):
    producto = Producto.objects.get(id=id)
    data = {
        'form': ProductoForm(instance=producto)
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto)
        if formulario.is_valid():
            formulario.save()
            return redirect(to='adm-producto')
        data['form']=ProductoForm(instance=Producto.objects.get(id=id))
    return render(request,'admin/edit-product.html', data)

#Registrar Cliente desde Admin
def registerClient(request):
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
            client = client.save(commit=False)
            client.profile = profile
            client.save()
            #autenticar el usuario y redirigirlo
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            #autentificamos credenciales del usuario
            user = authenticate(username=username, password=password)
            return redirect(to='listado_usuarios')
        data['form']=form
        data['profile']=profile
    return render(request, 'accounts/register_client.html', data)

#Registrar Vendedor desde Admin
def registerSeller(request):
    data = {
       'form': CustomUserForm(),
        'profile': ProfileForm(),
        'seller': SellerForm()
    }
    if request.method=='POST':
        form = CustomUserForm(request.POST)
        profile = ProfileForm(request.POST)
        seller = SellerForm(request.POST)
        if form.is_valid() and profile.is_valid():
            new_user = form.save()
            profile = profile.save(commit=False)
            profile.user = new_user
            profile.save()
            #if client.is_valid():
            seller = seller.save(commit=False)
            seller.profile = profile
            seller.save()
            #autenticar el usuario y redirigirlo
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            #autentificamos credenciales del usuario
            user = authenticate(username=username, password=password)
            return redirect(to='listado_usuarios')
        data['form']=form
        data['profile']=profile
    return render(request, 'accounts/register_seller.html', data)

#Registrar Proveedor desde Admin
def registerSupplier(request):
    data = {
       'form': CustomUserForm(),
        'profile': ProfileForm(),
        'supplier': SupplierForm()
    }
    if request.method=='POST':
        form = CustomUserForm(request.POST)
        profile = ProfileForm(request.POST)
        supplier = SupplierForm(request.POST)
        if form.is_valid() and profile.is_valid():
            new_user = form.save()
            profile = profile.save(commit=False)
            profile.user = new_user
            profile.save()
            #if client.is_valid():
            supplier = supplier.save(commit=False)
            supplier.profile = profile
            supplier.save()
            #autenticar el usuario y redirigirlo
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            #autentificamos credenciales del usuario
            user = authenticate(username=username, password=password)
            return redirect(to='listado_usuarios')
        data['form']=form
        data['profile']=profile
    return render(request, 'accounts/register_supplier.html', data)

#Registrar Empleado desde Admin
def registerEmployee(request):
    data = {
       'form': CustomUserForm(),
        'profile': ProfileForm(),
        'employee': EmployeeForm()
    }
    if request.method=='POST':
        form = CustomUserForm(request.POST)
        profile = ProfileForm(request.POST)
        employee = EmployeeForm(request.POST)
        if form.is_valid() and profile.is_valid():
            new_user = form.save()
            profile = profile.save(commit=False)
            profile.user = new_user
            profile.save()
            #if client.is_valid():
            employee = employee.save(commit=False)
            employee.profile = profile
            employee.save()
            #autenticar el usuario y redirigirlo
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            #autentificamos credenciales del usuario
            user = authenticate(username=username, password=password)
            return redirect(to='listado_usuarios')
        data['form']=form
        data['profile']=profile
    return render(request, 'accounts/register_employee.html', data)

#Editar Cuenta de usuario que se encuentra logueado "EDITAR MI CUENTA"
def editLoggedUser(request, pk):
    usuario = User.objects.get(pk=pk)
    perfil = request.user.profile
    data = {
        'form': CustomUserForm(instance=usuario),
        'profile': ProfileForm(instance=perfil)
    }
    if request.method == 'POST':
        formulario = CustomUserForm(data=request.POST, instance=usuario)
        profile = ProfileForm(data=request.POST, instance=perfil)
        if formulario.is_valid():
            formulario.save()
            profile.save()
            data['mensaje']='Usuario modificado correctamente'
            #login(request, usuario) #NO ES NECESARIO
            return redirect(to='store')
        data['form']=CustomUserForm(instance=User.objects.get(pk=pk))
        data['profile']=ProfileForm(instance=perfil)
    return render(request,'admin/edit_user.html', data)

#Registro de usuario NORMAL
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

#Editar Usuario desde Admin
def editPage(request, id):
    usuario = User.objects.get(id=id)
    perfil = request.user.profile
    data = {
        'form': CustomUserForm(instance=usuario),
        'profile': ProfileForm(instance=perfil)
    }
    if request.method == 'POST':
        formulario = CustomUserForm(data=request.POST, instance=usuario)
        profile = ProfileForm(data=request.POST, instance=perfil)
        if formulario.is_valid():
            formulario.save()
            profile.save()
            data['mensaje']='Usuario modificado correctamente'
            login(request, usuario)
            return redirect(to='store')
        data['form']=CustomUserForm(instance=User.objects.get(id=id))
        data['profile']=ProfileForm(instance=perfil)
    return render(request,'accounts/edit.html', data)

#Eliminar Usuario desde Admin
def deletePage(request):
    user = request.user
    user.delete()
    return redirect(to='store')

    return render(request, 'accounts/delete.html', data)

#Log In
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

#Log Out
def logoutUser(request):
    logout(request)
    return redirect('')

#Pagina Principal
def store(request):

    data = cartData(request)
    cartItems = data['cartItems']

    products = Producto.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

#Carrito de Compra
def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

#Check Out
def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

#Actualizar productos del carro
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

#Generar Venta
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    total  = float(data['form']['total'])

    if request.user.is_authenticated:
        usuario = request.user.profile
        order, created = Order.objects.get_or_create(usuario=usuario, complete=False)
        if usuario.tipo == 'Vendedor':
            boleta = Boleta.objects.get_or_create(
            order=order,
            n_boleta=transaction_id,
            total=total,
            vendedor = usuario.name
        )
        else:
            boleta = Boleta.objects.get_or_create(
            order=order,
            n_boleta=transaction_id,
            total=total,
            vendedor = 'Tienda Ferme'
        )
    else:
       usuario, order = guestOrder(request, data)
       boleta = Boleta.objects.get_or_create(
        order=order,
        n_boleta=transaction_id,
        total=total,
        vendedor = 'Tienda Ferme'
        )

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
    return JsonResponse('Pago realizado', safe=False)

#Administracion de Productos (LISTADO)
def adm_productos(request):
    prods = Producto.objects.all()
    data={
        'prods': prods
    }
    return render(request, 'store/adm-producto.html', data)

#Agregar Productos
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
            return redirect(to='adm-producto')
        data['form']=formulario
    return render(request, 'store/agregar-producto.html', data)

# ---------------------TEMPLATES "EN PROCESO"-----------------------
#3Iteracion
def terceraIFacturas(request):
    data = {}
    return render(request, 'store/adm-factura.html', data)

def terceraIBoletas(request):
    data = {}
    return render(request, 'store/adm-factura.html', data)

def terceraIOrdenesCompra(request):
    data = {}
    return render(request, 'store/adm-factura.html', data)    
#-------------------------------------------------------------------

#Eliminar Producto
def eliminar_producto(request, pk):
    producto = Producto.objects.get(pk=pk)
    producto.delete()
    return redirect(to='adm-producto')

#Listado Boleta
def adm_boletas(request):
    bills = Boleta.objects.all()
    context={
        'bills': bills,
    }
    return render(request, 'store/adm-boleta.html', context)

#Eliminar/Anular Boleta desde tabla
def delete_bill(request, pk):
    bill = Boleta.objects.get(pk=pk)
    bill.delete()
    return redirect(to='adm-boleta')

#Editar boleta desde tabla
def edit_bill(request, pk):
    bill = Boleta.objects.get(pk=pk)
    data = {
        'form': BoletaForm(instance=bill),
    }
    if request.method == 'POST':
        formulario = BoletaForm(data=request.POST, instance=bill)
        if formulario.is_valid():
            formulario.save()
            data['mensaje']='Boleta modificado correctamente'
            return redirect(to='adm-boleta')
        data['form']=BoletaForm(instance=Boleta.objects.get(pk=pk))
    return render(request,'store/edit_bill.html', data)

#Check Out Factura
def checkoutfact(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, 'store/checkout-factura.html', context)

#Generar Venta Factura
def processOrderFact(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    total  = float(data['form']['total'])
    rut = data['factura']['rut']
    razon = data['factura']['razon']
    giro = data['factura']['giro']

    if request.user.is_authenticated:
        usuario = request.user.profile
        order, created = Order.objects.get_or_create(usuario=usuario, complete=False)
        if usuario.tipo == 'Vendedor':
            factura = Factura.objects.get_or_create(
            order=order,
            n_factura=transaction_id,
            total=total,
            vendedor = usuario.name,
            rut = rut,
            razon = razon,
            giro = giro
        )
        else:
            factura = Factura.objects.get_or_create(
            order=order,
            n_factura=transaction_id,
            total=total,
            vendedor = 'Tienda Ferme',
            rut = rut,
            razon = razon,
            giro = giro
        )
    else:
       usuario, order = guestOrder(request, data)
       factura = Factura.objects.get_or_create(
        order=order,
        n_factura=transaction_id,
        total=total,
        vendedor = 'Tienda Ferme',
        rut = rut,
        razon = razon,
        giro = giro
        )

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
    return JsonResponse('Pago realizado', safe=False)

#Listado Boleta
def adm_facturas(request):
    facts = Factura.objects.all()
    context={
        'facts': facts
    }
    return render(request, 'store/adm-factura.html', context)
#Eliminar Factura
def eliminar_factura(request, pk):    
    factura = Factura.objects.get(pk=pk)
    factura.delete()
    return redirect(to='adm-factura')    

#Listado Boleta
def adm_ordencompra(request):
    orden = OrdenCompra.objects.all()
    context={
        'orden': orden
    }
    return render(request, 'store/adm-ordencompra.html', context)

#Generar Orden de Compra
def orden_compra(request):
    remitente = request.user.profile
    data={
        'remitente': remitente, 'form': OrdenCompraForm()
    }
    if request.method=='POST':
        formulario = OrdenCompraForm(request.POST)
        if formulario.is_valid():
            formulario = formulario.save(commit=False)
            formulario.remitente = remitente
            if 'btnsend' in request.POST:
                formulario.enviado = True
            formulario.save()
            data['mensaje']='Producto agregado con éxito'
            return redirect(to='adm-ordencompra')
        data['form'] = formulario
    return render(request, 'store/generar-ordencompra.html', data)

#Eliminar Orden de Compra
def eliminar_orden_compra(request, pk):
    orden = OrdenCompra.objects.get(pk=pk)
    orden.delete()
    return redirect(to='adm-ordencompra')    

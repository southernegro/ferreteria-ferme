from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import csv
from django.http import HttpResponse
import json
import datetime
from .models import *
from .forms import  ProfileForm, CustomUserForm, ClientForm, ProductoForm, SellerForm, EmployeeForm, SupplierForm, BoletaForm, FacturaForm, OrdenCompraForm
from .utils import cookieCart, cartData, guestOrder



#Listado Usuarios
@login_required
def listUser(request):
    users = Profile.objects.all()
    data={
        'users': users
    }
    return render(request, 'admin/listado_usuarios.html', data)

#Eliminar usuario desde tabla
@login_required
def deleteUser(request, pk):
    user = User.objects.get(pk=pk)
    perfil = Profile.objects.get(user_id=pk)
    user.delete()
    perfil.delete()
    return redirect(to='listado_usuarios')

#Editar usuario desde tabla
@login_required
def editUser(request, pk):
    usuario = User.objects.get(pk=pk)
    perfil = Profile.objects.get(user_id=pk)
    data = {
        'form': CustomUserForm(instance=usuario),
        'profile': ProfileForm(instance=perfil),
        'perfil':perfil
    }
    if request.method == 'POST':
        formulario = CustomUserForm(data=request.POST, instance=usuario)
        profile = ProfileForm(data=request.POST, instance=perfil)
        if formulario.is_valid():
            formulario.save()
            profile.save()
            data['mensaje']='Usuario modificado correctamente'
            return redirect(to='listado_usuarios')
        data['form']=CustomUserForm(instance=User.objects.get(pk=pk))
        data['profile']=ProfileForm(instance=perfil)
    return render(request,'admin/edit_user.html', data)

#Editar Producto
@login_required
def editProductPage(request, id):
    producto = Producto.objects.get(id=id)
    data = {
        'form': ProductoForm(instance=producto), 'producto':producto
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto)
        if formulario.is_valid():
            formulario.save()
            return redirect(to='adm-producto')
        data['form']=ProductoForm(instance=Producto.objects.get(id=id))
    return render(request,'admin/edit-product.html', data)

#Registrar Cliente desde Admin
@login_required
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
            profile.tipo = 'Cliente'
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
@login_required
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
            profile.tipo = 'Vendedor'
            profile.save()
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
@login_required
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
            profile.tipo = 'Proveedor'
            profile.save()
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
@login_required
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
            profile.tipo = 'Empleado'
            profile.save()
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
@login_required
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
@login_required
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
            #login(request, usuario)
            return redirect(to='store')
        data['form']=CustomUserForm(instance=User.objects.get(id=id))
        data['profile']=ProfileForm(instance=perfil)
    return render(request,'accounts/edit.html', data)

#Eliminar Usuario desde Admin
@login_required
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
    string_total = data['form']['total']
    total  = float(string_total.replace(',','.'))

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
@login_required
def adm_productos(request):
    prods = Producto.objects.all()
    data={
        'prods': prods
    }
    return render(request, 'store/adm-producto.html', data)

#Agregar Productos
@login_required
def agregar_producto(request):
    data={
    'form': ProductoForm()
    }
    if request.method=='POST':
        formulario = ProductoForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            #formulario = formulario.save(commit=False)
            #formulario.sku = idproducto
            formulario.save()

            data['mensaje']='Producto agregado con éxito'
            return redirect(to='adm-producto')
        data['form']=formulario
    return render(request, 'store/agregar-producto.html', data)

def id_producto(request):
    productos = Producto.objects.all()
    sku = productos.skuProducto
    for i in productos:
        productos.sku = sku
    return redirect(to='agregar-producto')

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
@login_required
def eliminar_producto(request, pk):
    producto = Producto.objects.get(pk=pk)
    producto.delete()
    return redirect(to='adm-producto')

#Listado Boleta
@login_required
def adm_boletas(request):
    bills = Boleta.objects.all()
    context={
        'bills': bills,
    }
    return render(request, 'store/adm-boleta.html', context)

#Eliminar/Anular Boleta desde tabla
@login_required
def delete_bill(request, pk):
    bill = Boleta.objects.get(pk=pk)
    bill.delete()
    return redirect(to='adm-boleta')

#Editar boleta desde tabla
@login_required
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

#Editar factura
@login_required
def edit_receipt(request, pk):
    receipt = Factura.objects.get(pk=pk)
    data = {
        'form': FacturaForm(instance=receipt),
    }
    if request.method == 'POST':
        formulario = FacturaForm(data=request.POST, instance=receipt)
        if formulario.is_valid():
            formulario.save()
            data['mensaje']='Factura modificada correctamente'
            return redirect(to='adm-factura')
        data['form']=FacturaForm(instance=Factura.objects.get(pk=pk))
    return render(request,'store/edit_receipt.html', data)

#Editar Orden de compra
@login_required
def edit_order(request, pk):
    order = OrdenCompra.objects.get(pk=pk)
    data = {
        'form': OrdenCompraForm(instance=order), 'order':order
    }
    if request.method == 'POST':
        formulario = OrdenCompraForm(data=request.POST, instance=order)
        if formulario.is_valid():
            if 'btnsend' in request.POST:
                order.enviado = True
                formulario.save()
            formulario.save()
            data['mensaje']='Orden de compra modificada correctamente'
            return redirect(to='adm-ordencompra')
        data['form']=OrdenCompraForm(instance=OrdenCompra.objects.get(pk=pk))
    return render(request,'store/edit_order.html', data)

@login_required
def send_order(request, pk):
    orden = OrdenCompra.objects.get(pk=pk)
    if request.method=='POST':
        formulario = OrdenCompraForm(request.POST)
        if formulario.is_valid():
            formulario = formulario.save(commit=False)
            if 'btnsend' in request.POST:
                formulario.enviado = True
            formulario.save()
            data['mensaje']='Producto agregado con éxito'
        return redirect(to='adm-ordencompra')
    return redirect(to='adm-ordencompra')

#Revisión orden de compra
@login_required
def review_order(request, pk):
    orden = OrdenCompra.objects.get(pk=pk)
    context={
        'orden': orden
    }
    return render(request, 'store/review_order.html',context)

@login_required
def aprobarOrden(request, pk):
    orden = OrdenCompra.objects.get(pk=pk)
    orden.status='Aprobado'
    orden.save()
    return redirect(to='adm-ordencompra')

@login_required
def rechazarOrden(request, pk):
    orden = OrdenCompra.objects.get(pk=pk)
    orden.status='Rechazado'
    orden.save()
    return redirect(to='adm-ordencompra')

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
    string_total = data['form']['total']
    total  = float(string_total.replace(',','.'))
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
@login_required
def adm_facturas(request):
    facts = Factura.objects.all()
    context={
        'facts': facts
    }
    return render(request, 'store/adm-factura.html', context)

#Eliminar Factura
@login_required
def eliminar_factura(request, pk):    
    factura = Factura.objects.get(pk=pk)
    factura.delete()
    return redirect(to='adm-factura')    

#Listado Ordenes
@login_required
def adm_ordencompra(request):
    orden = OrdenCompra.objects.all()
    users = Profile.objects.filter(tipo='Proveedor')
    context={
        'orden': orden, 'users':users
    }
    return render(request, 'store/adm-ordencompra.html', context)

#Generar Orden de Compra
@login_required
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
@login_required
def eliminar_orden_compra(request, pk):
    orden = OrdenCompra.objects.get(pk=pk)
    orden.delete()
    return redirect(to='adm-ordencompra')

#Vista de proveedor, para consultar ordenes de compra
@login_required
def vista_proveedor(request):
    prov = request.user.profile.supplier
    orden = OrdenCompra.objects.all()
    context={
        'orden': orden, 'prov': prov
    }
    return render(request, 'store/proveedor-ordencompra.html', context)

#Consultar Orden de Compra
@login_required
def check_order(request, pk):
    order = OrdenCompra.objects.get(pk=pk)
    data = {
        'order':order
    }
    return render(request,'store/check_order.html', data)

#Pagina 404
def page_not_found(request):
    return render(request, 'store/page_not_found.html')

#exportacion de la tabla de profiles a formato csv
def exportar_usuarios(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_de_usuario.csv"'
    writer = csv.writer(response)
    writer.writerow(['Usuario', 'Nombre', 'Apellido', 'Teléfono', 'Correo', 'Tipo de Usuario'])
    users = Profile.objects.all().values_list('user', 'name', 'last_name', 'phone_number', 'email', 'tipo')
    for user in users:
        writer.writerow(user)
    return response
#exportacion de la tabla de producto a formato csv
def exportar_productos(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_de_productos.csv"'
    writer = csv.writer(response)
    writer.writerow(['Nombre', 'SKU', 'Precio', 'Despacho Disponible','Stock', 'Proveedor', 'Familia', 'Tipo de Producto'])
    productos = Producto.objects.all().values_list('name', 'sku', 'price', 'despacho', 'stock', 'critic_stock', 'proveedor', 'familia', 'tipo_producto')
    for producto in productos:
        writer.writerow(producto)
    return response 
#exportacion de la tabla de boleta a formato csv    
def exportar_boletas(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_de_boletas.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID de Venta', 'N° de Boleta', 'Vendedor','Total'])
    boletas = Boleta.objects.all().values_list('order', 'n_boleta', 'vendedor', 'total')
    for boleta in boletas:
        writer.writerow(boleta)
    return response  
#exportacion de la tabla de factura a formato csv    
def exportar_facturas(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_de_facturas.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID de Venta', 'N° de Factura', 'Vendedor', 'Rut', 'Razón Social', 'Giro', 'Total'])
    facturas = Factura.objects.all().values_list('order', 'n_factura', 'vendedor', 'rut', 'razon', 'giro', 'total')
    for factura in facturas:
        writer.writerow(factura)
    return response
#exportacion de la tabla de ordenes de compra a formato csv    
def exportar_ordenes(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_de_ordenes_de_compra.csv"'
    writer = csv.writer(response)
    writer.writerow(['Remitente', 'Fecha de Creacion', 'Enviada', 'Proveedor', 'Detalle'])
    ordenes = OrdenCompra.objects.all().values_list('remitente', 'fecha', 'enviado', 'proveedor', 'detalle')
    for orden in ordenes:
        writer.writerow(orden)
    return response              

#Filtro por Familia de Productos
def storeCategories(request, pk):

    data = cartData(request)
    cartItems = data['cartItems']

    products = Producto.objects.filter(familia_id=pk)
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

#Filtro por Tipo de Productos
def storeTypes(request, pk):

    data = cartData(request)
    cartItems = data['cartItems']

    products = Producto.objects.filter(tipo_producto_id=pk)
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

#Filtro Usuarios por Tipo --------------------------------------------------------------
def userClients(request):
    users = Profile.objects.filter(tipo='Cliente')
    data={
        'users': users
    }
    return render(request, 'admin/listado_usuarios.html', data)
def userEmployees(request):
    users = Profile.objects.filter(tipo='Empleado')
    data={
        'users': users
    }
    return render(request, 'admin/listado_usuarios.html', data)
def userSuppliers(request):
    users = Profile.objects.filter(tipo='Proveedor')
    data={
        'users': users
    }
    return render(request, 'admin/listado_usuarios.html', data)
def userSellers(request):
    users = Profile.objects.filter(tipo='Vendedor')
    data={
        'users': users
    }
    return render(request, 'admin/listado_usuarios.html', data)
import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        
    print('Cart:', cart)
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            product = Producto.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                    },
                'quantity':cart[i]['quantity'],
                'get_total':total,
            }
            items.append(item)

            if product.despacho == True:
                order['shipping'] = True
        except:
            pass
    return {'cartItems':cartItems, 'order':order, 'items':items}

def cartData(request):
    if request.user.is_authenticated:
        usuario = request.user.profile
        order, created = Order.objects.get_or_create(usuario=usuario, complete=False)
        items = order.orderitems_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems':cartItems, 'order':order, 'items':items}

def guestOrder(request, data):
    print('Usuario no registrado')
    print('COOKIES', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    usuario, created = Profile.objects.get_or_create(
        email=email,
        )
    usuario.name = name
    usuario.save()

    order = Order.objects.create(
        usuario=usuario,
        complete=False,
        )

    for item in items:
        product = Producto.objects.get(id=item['product']['id'])
        orderItem = OrderItems.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
            )
    return usuario, order
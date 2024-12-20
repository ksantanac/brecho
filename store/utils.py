import json
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_protect

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print(f"Cart: {cart}")
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']
        
    for i in cart:
        try:
            cartItems += cart[i]["quantity"]
                
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])
                
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]
                
            item = {
                'product':{
                    'id':product.id,
                    'name':product.name, 
                    'price':product.price, 
                    'imageURL':product.imageURL
                }, 
                'quantity':cart[i]['quantity'],
                'get_total':total,
            }
            items.append(item)
                
            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    
    return {'cartItems':cartItems ,'order':order, 'items':items}


def cartData(request):
    if request.user.is_authenticated:
        try:
            # Verifica se o usuário tem um Customer associado
            customer = request.user.customer
        except ObjectDoesNotExist:
            # Se o Customer não existir, cria um novo automaticamente
            customer = Customer.objects.create(user=request.user)

        # Busca pedidos incompletos relacionados ao Customer
        orders = Order.objects.filter(customer=customer, complete=False)
        
        # Se houver pedidos, pegar o primeiro (ou o mais recente se preferir)
        if orders.exists():
            order = orders.first()  # Pega o primeiro pedido da lista
        else:
            # Se não existir nenhum pedido, cria um novo pedido
            order = Order.objects.create(customer=customer, complete=False)
        
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # Para usuários não autenticados, usa os dados do cookie
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        
    return {'cartItems': cartItems, 'order': order, 'items': items}

def guestOrder(request, data):
    print("Usuario não logado...")
        
    print(f"COOKIES: {request.COOKIES}")
    name = data['form']['name']
    email = data['form']['email']
        
    cookieData = cookieCart(request)
    items = cookieData['items']
        
    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()
        
    order = Order.objects.create(
        customer=customer,
        complete=False
    )
        
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
            
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
           
    return customer, order








from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm
# from .forms import CustomAuthenticationForm

from django.contrib import messages
from .forms import CustomUserLoginForm  # Aqui você vai precisar criar um formulário customizado

from .models import *
from .utils import cookieCart, cartData, guestOrder

from django.views.decorators.csrf import csrf_protect

import json
import datetime


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()  # Corrigido a indentação
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

@login_required(login_url='/login/')
def cart(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

@login_required(login_url='/login/')
def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def search(request):
    query = request.GET.get("query", "")
    products = []

    if query:
        # Filtra os produtos pelo nome usando icontains para busca parcial (case-insensitive)
        products = Product.objects.filter(name__icontains=query)

    context = {"products": products, "query": query}
    return render(request, "store/search_results.html", context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print(f"Action: {action}")
    print(f"productId: {productId}")
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    # order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    # orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    # Usando filter para pegar todos os pedidos incompletos
    orders = Order.objects.filter(customer=customer, complete=False)

    if orders.exists():
        # Se houver pedidos incompletos, pega o primeiro (ou o mais recente se preferir)
        order = orders.first()
    else:
        # Se não existir nenhum pedido incompleto, cria um novo pedido
        order = Order.objects.create(customer=customer, complete=False)
    
    # Recupera ou cria o item do pedido
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == "add":
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)
        
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse("Item adicionado.", safe=False)

# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()
    
    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )  
    
    return JsonResponse("Pagamento concluído!", safe=False)

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Faz o login automaticamente após o registro
            return redirect('store')  # Redireciona para a página da loja
    else:
        form = UserRegistrationForm()
    
    return render(request, 'store/register.html', {'form': form})

@csrf_protect
def user_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        # Buscar usuário pelo email
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('store')  # Redirecionar para a página desejada após login
            else:
                messages.error(request, 'E-mail ou senha inválidos!')
        except User.DoesNotExist:
            messages.error(request, 'E-mail ou senha inválidos!')
    
    return render(request, 'store/login.html')
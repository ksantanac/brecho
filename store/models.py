from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    # Relacionamento um-para-um com o modelo User do Django, representando o cliente
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    # Nome do cliente
    name = models.CharField(max_length=200, null=True)
    # Email do cliente
    email = models.CharField(max_length=200)

    def __str__(self):
        # Retorna o nome do cliente ao chamar o modelo
        return self.name

class Product(models.Model):
    # Nome do produto
    name = models.CharField(max_length=200)
    # Preço do produto
    price = models.FloatField()
    # Indica se o produto é digital (exemplo: e-book, software)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        # Retorna o nome do produto ao chamar o modelo
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        
        return url


class Order(models.Model):
    # Relacionamento muitos-para-um com o modelo Customer, representando o cliente do pedido
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    # Data do pedido, definida automaticamente quando o pedido é criado
    date_ordered = models.DateTimeField(auto_now_add=True)
    # Indica se o pedido está completo
    complete = models.BooleanField(default=False)
    # ID da transação para o pedido
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        # Retorna o ID do pedido como string ao chamar o modelo
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    

class OrderItem(models.Model):
    # Relacionamento muitos-para-um com o modelo Product, representando o produto associado
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    # Relacionamento muitos-para-um com o modelo Order, representando o pedido associado
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    # Quantidade de itens do produto no pedido
    quantity = models.IntegerField(default=0, null=True, blank=True)
    # Data de adição do item ao pedido
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    

class ShippingAddress(models.Model):
    # Relacionamento muitos-para-um com o modelo Customer
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    # Relacionamento muitos-para-um com o modelo Order
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    # Endereço de entrega
    address = models.CharField(max_length=200, null=False)
    # Cidade do endereço de entrega
    city = models.CharField(max_length=200, null=False)
    # Estado do endereço de entrega
    state = models.CharField(max_length=200, null=False)
    # Código postal do endereço de entrega
    zipcode = models.CharField(max_length=200, null=False)
    # Data em que o endereço foi adicionado
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Retorna o endereço como string ao chamar o modelo
        return self.address

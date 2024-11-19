from django.contrib import admin
from .models import *

# Register your models here.

# Classe Inline para adicionar múltiplas imagens ao produto
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Número de campos adicionais para imagens ao editar/criar um produto

# Personalize o admin de Product para incluir imagens adicionais
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]  # Relacione com o Inline de ProductImage

# Registre os modelos no admin
admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)  # Use o ProductAdmin para personalizar
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(ProductImage)  # Também registre ProductImage
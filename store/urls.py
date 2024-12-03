from django.urls import path
from django.contrib.auth import views as auth_views  # Importa views padrão de autenticaç
from django.contrib.auth.views import LogoutView
from .import views

urlpatterns = [
    path("", views.store, name="store"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("search/", views.search, name="search"),  # Nova rota para pesquisa
    
    path("update_item/", views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    
    path("register/", views.register, name="register"),  # Nova rota para registro
    
    # Usando a view personalizada de login
    path("login/", views.user_login, name="login"),

    # Logout padrão
    path('logout/', LogoutView.as_view(next_page='store'), name='logout'),
]
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
    
    # Rotas para login e logout
    path("login/", auth_views.LoginView.as_view(template_name='store/login.html'), name="login"),
    path('logout/', LogoutView.as_view(next_page='store'), name='logout'),
]
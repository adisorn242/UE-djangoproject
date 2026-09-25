from django.urls import path
from .views import Home, About, AllProducts, ProductDetail, register, login, logout, profile

urlpatterns = [
    path('', Home, name='home'), #localhost:8000
    path('about/', About, name='about'), # localhost:8000/about/
    path('products/', AllProducts, name='all-products'),
    path('products/<int:id>/', ProductDetail, name='product-detail'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
]

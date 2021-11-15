from django.urls import path, include
from . views import HomeView, ItemDetailView, \
    ShopView, contact, Car, test, Services, Blog, About, Single, trip, Rent, cart, Search, remove, delete, signup, Product, Checkout, Shipping, thank
app_name = 'app'
urlpatterns = [
    path('', HomeView.as_view(), name='HomeView'),
    path('', ItemDetailView.as_view(), name='ItemDetailView'),
    path('', ShopView.as_view(), name='ShopView'),
    path('contact/', contact, name='contact'),
    path('cars/', Car.as_view(), name='cars'),
    path('test/', test, name='test'),
    path('services/', Services.as_view(), name='services'),
    path('blog/', Blog.as_view(), name='blog'),
    path('about/', About.as_view(), name='about'),
    path('blog/single/', Single.as_view(), name='single'),
    path('HomeView/single/', Single.as_view(), name='single'),
    path('HomeView/car/', Car.as_view(), name='car'),
    path('trip/', trip, name='trip'),
    path('cart/<slug>', cart, name='cart'),
    path('rent/', Rent.as_view(), name='rent'),
    path('search/', Search.as_view(), name='search'),
    path('remove/<slug>', remove, name='remove'),
    path('delete/<slug>', delete, name='delete'),
    path('signup/', signup, name='signup'),
    path('product/<slug>', Product.as_view(), name='product'),
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('payment/<payment_option>', Shipping.as_view(), name='payment'),
    path('thank/', thank, name='thank'),
]
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Category, Slider, Order, OrderItem, Contact, Trip, BillingAddress, ShippingAddress, Payment
from django.views.generic import View, DetailView
from .forms import PaymentForm, ShippingForm
from rest_framework import routers, viewsets, generics, serializers
from .serializers import UserSerializers,ItemSerializers, SliderSerializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
# Create your views here.


class BaseView(View):
    template_context = {
        'items': Item.objects.all()
    }


class HomeView(BaseView):
    def get(self, *args,**kwargs):
        self.template_context['category'] = Category.objects.all()
        self.template_context['slider'] = Slider.objects.all()
        self.template_context['new'] = Item.objects.filter(labels='new')
        self.template_context['popular'] = Item.objects.filter(labels='popular')
        self.template_context['sale'] = Item.objects.filter(labels='sale')

        return render(self.request, 'index.html', self.template_context)


class ItemDetailView(DetailView):
    model = Item
    template_name = 'single.html'


class ShopView(BaseView):
    def get(self, request):
        self.template_context['category'] = Category.objects.all()
        self.template_context['new'] = Item.objects.filter(labels='new')
        self.template_context['popular'] = Item.objects.filter(labels='popular')
        self.template_context['sale'] = Item.objects.filter(labels='sale')
        return render(request, 'car.html', self.template_context)


def contact(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        customer = Contact(
                first_name=first_name,
                last_name=last_name,
                email=email,
                subject=subject,
                message=message,
            )
        customer.save()
    return render(request, 'contact.html')


class Car(BaseView):
    def get(self, *args, **kwargs):
        self.template_context['item'] = Item.objects.all()
        self.template_context['new'] = Item.objects.filter(labels='new')
        self.template_context['sale'] = Item.objects.filter(labels='sale')
        self.template_context['popular'] = Item.objects.filter(labels='popular')
        return render(self.request, 'cars.html', self.template_context)


def test(request):
    return render(request,'test.html')


class Services(BaseView):
    def get(self, *args, **kwargs):

        return render(self.request, 'services.html')


class Blog(BaseView):
    def get(self, *args, **kwargs):

        return render(self.request, 'blog.html')


class About(BaseView):
    def get(self, *args, **kwargs):

        return render(self.request, 'about.html')


class Single(BaseView):
    def get(self, *args, **kwargs):

        return render(self.request, 'single.html')


def trip(request):
    if request.method == 'POST':
        pickup = request.POST['pickup']
        drop_off = request.POST['drop_off']
        journey_date = request.POST['journey_date']
        return_date = request.POST['return_date']
        costumer = Trip(
                user=request.user,
                pickup=pickup,
                drop_off=drop_off,
                journey_date=journey_date,
                return_date=return_date,
            )
        costumer.save()
    return render(request, 'test.html')


class Rent(BaseView):
    def get(self, *args, **kwargs):
        Order.objects.get_or_create(
            user=self.request.user,
            ordered=False
        )[0]
        try:
            if Order.objects.filter(user=self.request.user).exists():
                order = Order.objects.get(
                    user=self.request.user,
                    ordered=False, )
                self.template_context['object'] = order
            else:
                return ('/')

        except:
            return ('/')
        return render(self.request, 'rent.html', self.template_context)


def cart(request,slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )[0]
    orders = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if orders.exists():
        order = orders[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, "The quantity is updated")
            return redirect('app:rent')
        else:
            order.items.add(order_item)
            messages.success(request, 'The item is add in cart')
            return redirect('app:rent')
    else:
        order = Order.objects.create(
            user=request.user,
        )
        order.items.add(order_item)
        messages.success(request, "The item is added to your cart")
        return redirect('app:rent')
    return render(request, 'rent.html')


class Search(BaseView):
    def get(self,request, *args,**kwargs):
        query = request.GET.get('query',None)
        if not query:
            return redirect('/')
        self.template_context['item_search'] = Item.objects.filter(title__icontains=query)
        self.template_context['search_for'] = query
        return render(self.request, 'search.html',self.template_context)


def remove(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )[0]
    orders = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if orders.exists():
        order = orders[0]
        if order.items.filter(item__slug=item.slug).exists():
            if order_item.quantity>1:
                order_item.quantity -=1
                order_item.save()
                messages.success(request, "The quantity is updated")
                return redirect('app:rent')
            else:
                messages.error("Minimum quantity is 1")
                return redirect('/')
        else:
            order.items.add(order_item)
            messages.success(request, 'The item does not exist in cart')
            return redirect('app:rent')
    return render(request, 'rent.html')

def remove(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )[0]
    orders = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if orders.exists():
        order = orders[0]
        if order.items.filter(item__slug=item.slug).exists():
            if order_item.quantity>1:
                order_item.quantity -=1
                order_item.save()
                messages.success(request, "The quantity is updated")
                return redirect('app:rent')
            else:
                messages.error("Minimum quantity is 1")
                return redirect('/')
        else:
            order.items.add(order_item)
            messages.success(request, 'The item does not exist in cart')
            return redirect('app:rent')
    return render(request, 'rent.html')

def remove(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )[0]
    orders = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if orders.exists():
        order = orders[0]
        if order.items.filter(item__slug=item.slug).exists():
            if order_item.quantity>1:
                order_item.quantity -=1
                order_item.save()
                messages.success(request, "The quantity is updated")
                return redirect('app:rent')
            else:
                messages.error(request,"Minimum quantity is 1")
                return redirect('app:rent')
        else:
            order.items.add(order_item)
            messages.success(request, 'The item does not exist in cart')
            return redirect('app:rent')
    return render(request, 'rent.html')


def delete(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )[0]
    orders = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if orders.exists():
        order = orders[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.delete()
            messages.success(request, "Item deleted successfully")
            return redirect('app:rent')
        else:
            messages.success(request, 'The item does not exist in cart')
            return redirect('app:rent')
    return render(request, 'rent.html')


def signup(request):
    if request.method == 'POST':

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exist.')
                return redirect('app:signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'You have entered the used email.')
                return redirect('app:signup')
            else:
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password,
                )
            user.save()
        else:
            messages.error(request, 'Password do not match. Please enter Correctly')
            return redirect('app:signup')
    return render(request, 'signup.html')


class Product(DetailView):
    model = Item
    template_name = 'product.html'


class Checkout(BaseView):
    def get(self, *args,**kwargs):
        order = Order.objects.filter(user=self.request.user, ordered=False)
        form = PaymentForm()
        self.template_context['form'] = form
        self.template_context['object2'] = order
        return render(self.request, 'checkout.html', self.template_context)

    def post(self, *args, **kwargs):
        form = PaymentForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                address1 = form.cleaned_data.get('address1')
                address2 = form.cleaned_data.get('address2')
                phone = form.cleaned_data.get('phone')
                company = form.cleaned_data.get('company')
                email = form.cleaned_data.get('email')
                country = form.cleaned_data.get('country')
                order_notes = form.cleaned_data.get('order_notes')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    first_name=first_name,
                    last_name=last_name,
                    address1=address1,
                    address2=address2,
                    phone=phone,
                    company=company,
                    email=email,
                    country=country,
                    order_notes=order_notes,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                if payment_option == 'c':
                    return redirect('app:payment', payment_option='credit-card')
                elif payment_option == 'd':
                    return redirect('app:payment', payment_option='cash-on-delivery')
                else:
                    messages.error(self.request, 'Invalid Checkout!!!')
                    return redirect('app:checkout')
            messages.warning(self.request, 'Operation Failed!!!')
            return redirect('app:checkout')


        except:
            messages.warning(self.request,"Billing form in Working")
            return redirect("app:rent")


class Shipping(BaseView):
    def get(self, *args, **kwargs):
        order = Order.objects.filter(user=self.request.user, ordered=False)
        form = ShippingForm()
        self.template_context['form2'] = form
        self.template_context['object3'] = order
        return render(self.request, 'shipping.html', self.template_context)

    def post(self, *args, **kwargs):
        form = ShippingForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                address1 = form.cleaned_data.get('address1')
                address2 = form.cleaned_data.get('address2')
                phone = form.cleaned_data.get('phone')
                company = form.cleaned_data.get('company')
                email = form.cleaned_data.get('email')
                country = form.cleaned_data.get('country')
                order_notes = form.cleaned_data.get('order_notes')
                shipping_address = ShippingAddress(
                    user=self.request.user,
                    first_name=first_name,
                    last_name=last_name,
                    address1=address1,
                    address2=address2,
                    phone=phone,
                    company=company,
                    email=email,
                    country=country,
                    order_notes=order_notes,
                )
                shipping_address.save()
                order.shipping_address = shipping_address
                order.save()
                payment = Payment()
                payment.user = self.request.user
                payment.amount = order.all_total()
                payment.save()
                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()
                order.ordered = True
                order.payment = payment
                order.save()
                messages.success(self.request, 'Ordered Successful.')
                return redirect('app:thank')
            messages.warning(self.request,'Failed Operation!!!')
            return redirect('app:rent')

        except:
            messages.warning(self.request, "Shipping form in Working")
            return redirect("app:rent")


def thank(request):
    return render(request,'thankyou.html')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializers


class SliderViewSet(viewsets.ModelViewSet):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializers


class ItemFilterListView(generics.ListAPIView):
    serializer_class = ItemSerializers
    queryset = Item.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('id', 'title', 'price', 'description', 'labels', 'discounted_price')
    ordering_fields = ('price', 'title', 'id', 'labels')
    search_fields = ('title', 'description')


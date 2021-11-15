from django.db import models
from django.conf import settings
from django.urls import reverse
from django_countries.fields import CountryField
Status = (('active','active'),(' ','default'))
Transmission = (('automatic','Automatic'),('manual','Manual'))
Stock = (('in-stock','in-stock'),('out-stock','out-stock'))
Labels = (('new', 'new'), ('sale', 'sale'), ('popular', 'popular'))
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title


class Item(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    price = models.FloatField()
    discounted_price = models.FloatField()
    image = models.TextField()
    slug = models.TextField()
    labels = models.CharField(choices=Labels, blank=True, max_length=255)
    stock = models.CharField(choices=Stock, blank=True, max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=1)
    door = models.IntegerField()
    seat = models.IntegerField()
    transmission = models.CharField(choices=Transmission, blank=True, max_length=22)
    age = models.IntegerField()

    def __str__(self):
        return self.title

    def cart(self):
        return reverse("app:cart", kwargs={'slug': self.slug})

    def remove(self):
        return reverse("app:remove", kwargs={'slug': self.slug})

    def delete(self):
        return reverse("app:delete", kwargs={'slug': self.slug})

    def productlink(self):
        return reverse('app:product', kwargs={'slug': self.slug})


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=222)
    last_name = models.CharField(max_length=222)
    address1 = models.CharField(max_length=222)
    address2 = models.CharField(max_length=222)
    phone = models.IntegerField()
    company = models.CharField(max_length=222)
    email = models.EmailField()
    country = CountryField(multiple=False)
    order_notes = models.CharField(max_length=1000)

    def __str__(self):
        return self.address1


class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=222)
    last_name = models.CharField(max_length=222)
    address1 = models.CharField(max_length=222)
    address2 = models.CharField(max_length=222)
    phone = models.IntegerField()
    company = models.CharField(max_length=222)
    email = models.EmailField()
    country = CountryField(multiple=False)
    order_notes = models.CharField(max_length=1000)

    def __str__(self):
        return self.address1


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()

    def __str__(self):
        return self.user.username


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.item.title

    def get_total_price(self):
        return self.item.price*self.quantity

    def get_total_discounted_price(self):
        return self.item.discounted_price*self.quantity

    def get_actual_total(self):
        if self.item.discounted_price>0:
            return self.get_total_discounted_price()
        else:
            return self.get_total_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.SET_NULL, blank=True, null=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def total(self):
        total_price=0
        for orders in self.items.all():
            total_price += orders.get_actual_total()
        return total_price

    def all_total(self):
        all_total = self.total() +5
        return all_total


class Slider(models.Model):
    title = models.CharField(max_length=255)
    image = models.TextField()
    description = models.CharField(max_length=255, blank=True)
    rank = models.IntegerField()
    door = models.CharField(max_length=20)
    seat = models.CharField(max_length=20)
    transmission = models.CharField(choices=Transmission, blank=True, max_length=22)
    age = models.IntegerField()
    price = models.FloatField()
    status = models.CharField(choices=Status, max_length=255)

    def __str__(self):
        return self.title


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=1000)

    def __str__(self):
        return self.subject


class Trip(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pickup = models.CharField(max_length=255)
    drop_off = models.CharField(max_length=255)
    journey_date = models.CharField(max_length=255)
    return_date = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

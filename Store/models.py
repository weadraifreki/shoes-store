from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
    class Meta:
        db_table = "shoe_categories"

class Size(models.Model):
    size_number = models.IntegerField()
    def __str__(self):
        return str(self.size_number)
    class Meta:
        db_table = "shoe_sizes"

class Type(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title
    class Meta:
        db_table = "shoe_types"

class Shoe(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=250)
    price_sell = models.FloatField()
    price_buy = models.FloatField()
    date_buy = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    number_buy = models.IntegerField()
    number_left = models.IntegerField()
    categories = models.ManyToManyField(Category)
    type = models.ForeignKey(Type, null=True, on_delete=models.SET_NULL)
    class Meta:
        db_table = "shoes"

class Ad(models.Model):
    title = models.TextField()
    description = models.TextField()
    code = models.CharField(max_length=100)
    date_register = models.DateTimeField(default=timezone.now)
    date_publish = models.DateTimeField(default=timezone.now)
    date_expire = models.DateTimeField(default=timezone.now)
    price = models.FloatField()
    off = models.FloatField(default=0)
    shoe = models.ForeignKey(Shoe, null=True,  blank=True, on_delete=models.SET_NULL)
    is_special = models.BooleanField(default=False)
    class Meta:
        db_table = "shoe_ads"

class Picture(models.Model):
    # Name = models.CharField(max_length=200)
    image =  models.ImageField(upload_to="img")
    shoe = models.ForeignKey(Shoe, null=True,  blank=True, on_delete=models.SET_NULL)
    class Meta:
        db_table = "shoe_pictures"

class ShoeSize(models.Model):
    count = models.IntegerField()
    shoe = models.ForeignKey(Shoe, null=True, on_delete=models.SET_NULL)
    size = models.ForeignKey(Size, null=True, on_delete=models.SET_NULL)
    class Meta:
        db_table = "size_shoes"

class AdSize(models.Model):
    count = models.IntegerField()
    shoe = models.ForeignKey(Ad, null=True, on_delete=models.SET_NULL)
    size = models.ForeignKey(Size, null=True, on_delete=models.SET_NULL)
    class Meta:
        db_table = "size_ads"

class Customer(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=300, blank=True, null=True)
    mobile = models.CharField(max_length=11)
    address = models.TextField()
    postalcode = models.CharField(max_length=11)
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.SET_NULL)
    register_datetime = models.DateTimeField(default=timezone.now)
    social_network = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.Firstname + " " + self.Lastname
    class Meta:
        db_table = "customers"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.customer.save()

class Payment(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
    class Meta:
        db_table = "payments"

class Order(models.Model):
    order_datetime = models.DateTimeField(default=timezone.now)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    payment_method = models.ForeignKey(Payment, blank=True, null=True, on_delete=models.SET_NULL)
    is_pay = models.BooleanField(default=False)
    post_refer = models.CharField(max_length=35, blank=True, null=True)
    status = models.IntegerField()
    class Meta:
        db_table = "orders"

class OrderItem(models.Model):
    ad = models.ForeignKey(Ad, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    size = models.ForeignKey(Size, null=True, blank=True, on_delete=models.SET_NULL)
    count = models.IntegerField(default=1)
    class Meta:
        db_table = "orderitems"

class Ticket(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    ticketDate = models.DateTimeField(default=timezone.now)
    ticketText = models.TextField()
    response_datetime = models.DateTimeField(default=timezone.now)
    response_text = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    class Meta:
        db_table = "tickets"


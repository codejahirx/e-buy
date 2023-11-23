from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from taggit.managers import TaggableManager

# Create your models here.


class Profile(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.IntegerField(unique=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.name


class Address(models.Model):
    STATE_CHOICES = [
        ('AP', 'Andhra Pradesh'),
        ('AR', 'Arunachal Pradesh'),
        ('AS', 'Assam'),
        ('BR', 'Bihar'),
        ('CG', 'Chhattisgarh'),
        ('GA', 'Goa'),
        ('GJ', 'Gujarat'),
        ('HR', 'Haryana'),
        ('HP', 'Himachal Pradesh'),
        ('JH', 'Jharkhand'),
        ('KA', 'Karnataka'),
        ('KL', 'Kerala'),
        ('MP', 'Madhya Pradesh'),
        ('MH', 'Maharashtra'),
        ('MN', 'Manipur'),
        ('ML', 'Meghalaya'),
        ('MZ', 'Mizoram'),
        ('NL', 'Nagaland'),
        ('OD', 'Odisha'),
        ('PB', 'Punjab'),
        ('RJ', 'Rajasthan'),
        ('SK', 'Sikkim'),
        ('TN', 'Tamil Nadu'),
        ('TG', 'Telangana'),
        ('TR', 'Tripura'),
        ('UP', 'Uttar Pradesh'),
        ('UK', 'Uttarakhand'),
        ('WB', 'West Bengal'),
        ('CH', 'Chandigarh'),
        ('DL', 'Delhi'),
        ('PY', 'Puducherry')
    ]
    name = models.CharField(max_length=50)
    phone = models.IntegerField(unique=True, null=True)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug =  AutoSlugField(
        populate_from='name', unique=True, null=True, default=None)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    slug = AutoSlugField(
        populate_from='name', unique=True, null=True, default=None)
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.name
    
class Review(models.Model):
    RATING_CHOICES = [
        ('5', 'Five'),
        ('4', 'Four'),
        ('3', 'Three'),
        ('2', 'Two'),
        ('1', 'One'),
    ]
    name = models.CharField(max_length=50)    
    review = models.TextField(max_length=50)
    posted_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.CharField(max_length=1,choices=RATING_CHOICES,default='5')
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.quantity * self.product.price
    
    def __str__(self):
        return self.product.name
    

class Order(models.Model):
    ORDER_STATUS = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Packed', 'Packed'),
        ('On the way', 'On the way'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    ordered_date = models.DateField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    address = models.ForeignKey(Address,on_delete=models.SET_NULL,null=True)
    order_status = models.CharField(
        max_length=50, choices=ORDER_STATUS, default='Pending')
    
    def __str__(self):
        return self.product.name

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    message = models.TextField()

    def __str__(self):
        return self.name
    
class Wishlist(models.Model):     
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.product.name
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    user_roles = (
        ('buy', 'Buyer'),
        ('sell', 'Seller'),
        ('admin', 'Administrator')
    )
    role = models.CharField(max_length=15, choices=user_roles)
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Add a custom related_name
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
        related_query_name='customuser',
    )

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Add a custom related_name
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='customuser',
    )


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.IntegerField()
    availability = models.BooleanField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    number_of_items = models.IntegerField()
    image = models.ImageField(upload_to="products")

    def __str__(self):
        return self.product_name


class MyCart(models.Model):
    version_choice = (
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('ultra', 'Ultra'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    version = models.CharField(max_length=100, choices=version_choice, default='standard')
    quantity = models.PositiveIntegerField(default=1)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_role_display() + " " + self.product.product_name

class DeliveryInformation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=150)

    def __str__(self):
        return self.name + " " + self.surname

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total = models.IntegerField()
    info = models.ForeignKey(DeliveryInformation, on_delete=models.CASCADE, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order Date:" + self.date_creation.__str__()
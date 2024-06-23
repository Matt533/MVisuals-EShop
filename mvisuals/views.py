import datetime
from functools import wraps
from random import random

from django.contrib.auth.decorators import permission_required, user_passes_test, login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from mvisuals.models import Product, Category, MyCart, CustomUser, Order, DeliveryInformation, Post
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from mvisuals.forms import CustomAuthenticationForm, CustomerRegistrationForm, AddProductForm, ProductForm, \
    DeliveryInfoForm, AddPostForm, PostForm
from django.urls import reverse
from django.db.models import Q
import logging
from django.shortcuts import render
from .models import Product, Category
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render
from .models import Product, Category  # Import your Product and Category models
import random, datetime, hashlib

logger = logging.getLogger(__name__)


# Create your views here.

def aboutus(request):
    categories = Category.objects.order_by('id').all()
    context = {"categories": categories}
    return render(request, "aboutUs.html", context)

def add_product(request):
    categories = Category.objects.order_by('id').all()
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to the product details page or any other appropriate URL
            return redirect('product_details', product_id=form.instance.id)
    else:
        form = AddProductForm()
    context = {'form': form, 'categories': categories}
    return render(request, 'addProduct.html', context)

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            if 'image' not in request.FILES:
                form.fields['image'].required = False
            form.save()
            return redirect('product_details', product_id=product_id)
        else:
            print(form.errors)

    else:
        form = ProductForm(instance=product)
    return redirect('product_details', product_id=product_id)

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('/home')

def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            print(form.cleaned_data)  # Debug output
            form.save()
            return redirect('post_details', post_id=post_id)
        else:
            # Print form errors to the console for debugging
            print(form.errors)
    else:
        form = PostForm(instance=post)

    # Render the edit post page with the form and post object
    return render(request, 'postdetails.html', {'form': form, 'post': post})

def add_post(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            # Redirect to the product details page or any other appropriate URL
            return redirect('post_details', post_id=form.instance.id)
    else:
        form = AddPostForm(user=request.user)
    context = {'form': form}
    return render(request, 'addpost.html', context)



def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('/home')

def forum(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, 'forum.html', context)

def home(request):
    products = Product.objects.all()[:10]
    categories = Category.objects.order_by('id').all()

    all_products = Product.objects.all()
    if all_products:
        today = datetime.date.today().isoformat()
        hash_value = hashlib.md5(today.encode()).hexdigest()
        index = int(hash_value, 17) % len(all_products)
        random_product = all_products[index]
    else:
        random_product = None

    context = {
        "products": products,
        "categories": categories,
        "random_product": random_product,
    }
    return render(request, "home.html", context)

def filter_category(request):
    category_id = request.GET.get('category')

    categories = Category.objects.order_by('id').all()
    products = Product.objects.all()

    if category_id:
        products = products.filter(category=category_id)

    all_products = Product.objects.all()
    if all_products:
        today = datetime.date.today().isoformat()
        hash_value = hashlib.md5(today.encode()).hexdigest()
        index = int(hash_value, 17) % len(all_products)
        random_product = all_products[index]
    else:
        random_product = None

    context = {"categories": categories, "products": products, "random_product": random_product}
    return render(request,'home.html', context)

def searchbyword(request):
    keyword = request.GET.get('keyword')
    queryset = Product.objects.filter(
        Q(brand__icontains=keyword) |
        Q(product_name__icontains=keyword) |
        Q(category__name__icontains=keyword)
    ).distinct()[:10]

    categories = Category.objects.order_by('id').all()

    all_products = Product.objects.all()
    if all_products:
        today = datetime.date.today().isoformat()
        hash_value = hashlib.md5(today.encode()).hexdigest()
        index = int(hash_value, 17) % len(all_products)
        random_product = all_products[index]
    else:
        random_product = None


    context = {"products": queryset, "keyword": keyword, "categories": categories, "random_product": random_product}
    return render(request, "home.html", context)

def details(request, product_id=None):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.order_by('id').all()
    context = {"product": product, "categories": categories}
    return render(request, "details.html", context)

def posts(request, post_id=None):
    post = get_object_or_404(Post, id=post_id)
    users = CustomUser.objects.all()
    context = {"post": post, "users": users}
    return render(request, "postdetails.html", context)

def form_submission(request, product_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_cart':
            product = Product.objects.get(id=product_id)
            quantity = int(request.POST.get('quantity', 1))
            version = request.POST.get('version', 'Standard')
            # Try to get an existing cart item for the user and product combination
            item = MyCart.objects.filter(user=request.user, product=product).first()

            if item:
                # If the cart item exists, update the quantity
                new_quantity = item.quantity + quantity
                if new_quantity > product.number_of_items:
                    # Redirect to a page indicating that the maximum quantity is reached
                    return redirect(reverse('max'))
                item.quantity = new_quantity
                item.version = version
                item.save()
            else:
                # If the cart item does not exist, create a new one
                MyCart.objects.create(user=request.user, product=product, quantity=quantity, version=version)

        return redirect('/cart')

    # Add a default redirect in case of a GET request or invalid action
    return redirect('/')

def login_user(request):
    categories = Category.objects.order_by('id').all()
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/home')

    else:
        form = CustomAuthenticationForm()
    context = {'form': form, 'categories': categories}
    return render(request, 'login.html', context)


def logout_page(request):
    logout(request)
    return redirect('/home')

def register(request):
    categories = Category.objects.order_by('id').all()
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = CustomerRegistrationForm()
    context = {'form': form, "categories":categories}
    return render(request, 'registration.html', context)

def maxquantity(request):
    return render(request, "errorpage.html")

def set_order(request):
    user = request.user
    delivery_information = None
    categories = Category.objects.order_by('id').all()

    try:
        delivery_information = DeliveryInformation.objects.get(user=user)
        initial_data = {
            'name': delivery_information.name,
            'surname': delivery_information.surname,
            'address': delivery_information.address,
            'city': delivery_information.city,
            'country': delivery_information.country,
            'phone': delivery_information.phone,
        }
    except DeliveryInformation.DoesNotExist:
        initial_data = {}

    if request.method == 'POST':
        form = DeliveryInfoForm(request.POST)
        if form.is_valid():
            if delivery_information:
                delivery_information.name = form.cleaned_data['name']
                delivery_information.surname = form.cleaned_data['surname']
                delivery_information.address = form.cleaned_data['address']
                delivery_information.city = form.cleaned_data['city']
                delivery_information.country = form.cleaned_data['country']
                delivery_information.phone = form.cleaned_data['phone']
                delivery_information.save()
            else:
                delivery_information = DeliveryInformation.objects.create(
                    user=user,
                    name=form.cleaned_data['name'],
                    surname=form.cleaned_data['surname'],
                    address=form.cleaned_data['address'],
                    city=form.cleaned_data['city'],
                    country=form.cleaned_data['country'],
                    phone=form.cleaned_data['phone']
                )

            cart_items = MyCart.objects.filter(user=user)
            total_price = 0
            version_sum = 0
            for item in cart_items:
                if item.version == "Standard":
                    version_sum = 0
                elif item.version == "Premium":
                    version_sum = 250
                elif item.version == "Ultra":
                    version_sum = 500
            item.total_price = item.quantity * item.product.price + version_sum
            total_price += item.total_price

            order = Order.objects.create(
                user=user,
                info=delivery_information,
                total=total_price
            )
            return redirect('/confirm')
    else:
        form = DeliveryInfoForm(initial=initial_data)

    context = {'form': form, 'categories': categories}
    return render(request, "deliveryInfo.html", context)


def confirm_order(request):
    categories = Category.objects.order_by('id').all()
    context = {'categories': categories}
    MyCart.objects.filter(user=request.user).delete()
    return render(request, "Order Confirmed.html", context)

def cart(request):
    categories = Category.objects.order_by('id').all()
    user = request.user
    cart_products = MyCart.objects.filter(user=user)
    total = 0
    version_sum = 0
    for item in cart_products:
        if item.version == "Standard":
            version_sum = 0
        elif item.version == "Premium":
            version_sum = 250
        elif item.version == "Ultra":
            version_sum = 500
        item.total = item.quantity * item.product.price + version_sum
        total += item.total
    context = {'cart_products': cart_products, "total": total, "categories": categories}
    return render(request, "cart.html", context)

def remove_product_from_cart(request, item_id):
    item = MyCart.objects.get(id=item_id)
    item.delete()
    return redirect('/cart')

def is_buyer(user):
    return user.is_authenticated and hasattr(user, 'role') and user.role == 'buy'

def buyer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not is_buyer(request.user):
            return redirect('/login/')  # Replace '/login/' with the URL to redirect non-buyers.
        return view_func(request, *args, **kwargs)

    return _wrapped_view
import datetime
from functools import wraps

from django.contrib.auth.decorators import permission_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from mvisuals.models import Product, Category, MyCart, CustomUser, Order, DeliveryInformation
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from mvisuals.forms import CustomAuthenticationForm, CustomerRegistrationForm, AddProductForm, ProductForm, \
    DeliveryInfoForm


# Create your views here.

def aboutus(request):
    return render(request, "aboutUs.html")


def home(request):
    queryset = Product.objects.all()[:10]
    categories = Category.objects.all()[:4]
    context = {"products": queryset, "categories": categories}
    return render(request, "home.html", context)


def searchbybrand(request):
    keyword = request.GET.get('keyword')
    queryset = Product.objects.filter(brand__iexact=keyword)
    categories = Category.objects.all()[:4]
    context = {"products": queryset, "keyword": keyword, "categories": categories}
    return render(request, "home.html", context)


def filter_category(request):
    category = request.GET.get('category')
    categories = Category.objects.all()[:4]
    products = Product.objects.all()
    if category:
        products = Product.objects.filter(category=category)[:10]
    context = {"categories": categories, "products": products}
    return render(request, "home.html", context)


def cameras(request):
    queryset = Product.objects.filter(category__name="Camera").all()[:10]
    categories = Category.objects.all()[:4]
    context = {"products": queryset, "categories": categories}
    return render(request, "home.html", context)


def drones(request):
    queryset = Product.objects.filter(category__name="Drone").all()[:10]
    categories = Category.objects.all()[:4]
    context = {"products": queryset, "categories": categories}
    return render(request, "home.html", context)


def details(request, product_id=None):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    context = {"product": product, "categories": categories}
    return render(request, "details.html", context)


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
                    item.quantity += quantity
                    item.version = version
                    if item.quantity > product.number_of_items:
                        return redirect('/maxquantity')
                    item.save()


                else:
                    # If the cart item does not exist, create a new one
                    MyCart.objects.create(user=request.user, product=product, quantity=quantity, version=version)

                return redirect('/cart')

def login_user(request):
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
    context = {'form': form}
    return render(request, 'login.html', context)


def logout_page(request):
    logout(request)
    return redirect('/home')

def register(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = CustomerRegistrationForm()
    context = {'form': form}
    return render(request, 'registration.html', context)

def maxquantity(request):
    return render(request, "errorpage.html")

def set_order(request):
    user = request.user
    delivery_information = None

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

    context = {'form': form}
    return render(request, "deliveryInfo.html", context)


def confirm_order(request):
    MyCart.objects.filter(user=request.user).delete()
    return render(request, "Order Confirmed.html")


def sort_price(request):
    sort_order = 'lowest'
    categories = Category.objects.all()[:4]
    if request.method == "POST":
     sort_order = request.POST.get('sort_price', 'lowest')

    if sort_order == 'lowest':
        products = Product.objects.order_by('price')[:10]
    else:
        products = Product.objects.order_by('-price')[:10]
    return render(request, 'home.html', {'products': products, 'categories':categories})



def cart(request):
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
    context = {'cart_products': cart_products, "total": total}
    return render(request, "cart.html", context)

def remove_product_from_cart(request, item_id):
    item = MyCart.objects.get(id=item_id)
    item.delete()
    return redirect('/cart')

def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to the product details page or any other appropriate URL
            return redirect('product_details', product_id=form.instance.id)
    else:
        form = AddProductForm()
    context = {'form': form}
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

def is_buyer(user):
    return user.is_authenticated and hasattr(user, 'role') and user.role == 'buy'

def buyer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not is_buyer(request.user):
            return redirect('/login/')  # Replace '/login/' with the URL to redirect non-buyers.
        return view_func(request, *args, **kwargs)

    return _wrapped_view
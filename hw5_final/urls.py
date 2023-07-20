"""hw5_final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import permission_required
from django.urls import path

import mvisuals.views
from mvisuals.views import home, searchbybrand, aboutus, filter_category, drones, cameras, details, form_submission, \
    cart, remove_product_from_cart, maxquantity, login_user, register, logout_page, add_product, \
    edit_product, delete_product, set_order, confirm_order, sort_price, buyer_required
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('aboutus/', aboutus, name='aboutus'),
    path('home/', home, name='home'),
    path('search/', searchbybrand, name="search_brand"),
    path('filter/', filter_category, name="filter_category"),
    path('cameras/', cameras, name="cameras"),
    path('drones/', drones, name="drones"),
    path('products/<int:product_id>/', details, name="product_details"),
    path('add/<int:product_id>/', form_submission, name="add"),
    path('cart/', buyer_required(cart), name="cart"),
    path('cart/remove/<int:item_id>/', buyer_required(remove_product_from_cart), name="remove_product_from_cart"),
    path('maxquantity/', maxquantity, name="max"),
    path('login/', login_user),
    path('deliveryinfo/', buyer_required(set_order), name="set_order"),
    path('add-product/', add_product, name="add_product"),
    path('product/edit/<int:product_id>/', edit_product, name="edit_product"),
    path('product-delete/<int:product_id>/', delete_product, name="delete_product"),
    path('confirm/', buyer_required(confirm_order), name="confirm_order"),
    path('sort_price/', sort_price, name="sort_items"),
    path('register/', register),
    path('logout/', logout_page, name="logout_page")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


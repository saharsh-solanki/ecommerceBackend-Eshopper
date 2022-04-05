"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path

from products import views
from products.views import AdminProductView, AdminProductCatgeoryView, AdminProductImagesView

urlpatterns = [
    path("api/products/", views.ProductView.as_view()),
    path("api/products/<int:pk>", views.SingleProductView.as_view()),
    path("api/category/", views.ProductCategoryhView.as_view()),
    path("api/site/detail/", views.ExtraDetailView.as_view()),
    # Admin Products
    path("api/admin/product/", AdminProductView.as_view({"get": "list", "post": "create"}), name="adminUser"),
    path("api/admin/product/<int:pk>", AdminProductView.as_view({"delete": "destroy", "patch": "update"}),
         name="adminUsesr"),
    path("api/admin/product/category/", AdminProductCatgeoryView.as_view({"get": "list", "post": "create"}),
         name="adminUser"),
    path("api/admin/product/category/<int:pk>",
         AdminProductCatgeoryView.as_view({"delete": "destroy", "patch": "update"}),
         name="adminUsesr"),
    path("api/admin/product/product_image/", AdminProductImagesView.as_view({"get": "list", "post": "create"}),
         name="adminUser"),
    path("api/admin/product/product_image/<int:pk>",
         AdminProductImagesView.as_view({"delete": "destroy", "patch": "update"}),
         name="adminUsesr"),

]

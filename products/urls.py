from django.urls import path
from . import views

urlpatterns = [
    path('', views.women_products, name='women_products')
]
from django.urls import path
from app_name.views import ProductView

urlpatterns = [
    path('products/analytics/', ProductView.as_view(), name='product-analytics'),
]
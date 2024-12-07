from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q, Count, Avg
from app_name.models import Product


@method_decorator(cache_page(300), name='dispatch')
class AnalyticsAPIView(APIView):
    def get(self, request):
        data = {
            "total_products": 100,
            "average_price": 150.0,
            "total_stock_value": 20000,
        }
        return Response(data)


class ProductView(APIView):
    def get(self, request):
        category = request.GET.get('category', '').lower()
        min_price = request.GET.get('min_price', 0)
        max_price = request.GET.get('max_price', None)

        filters = Q(price__gte=min_price)
        if max_price:
            filters &= Q(price__lte=max_price)
        if category:
            filters &= Q(category__iexact=category)

        filtered_products = Product.objects.filter(filters)

        analytics = filtered_products.aggregate(
            total_products=Count('id'),
            average_price=Avg('price'),
        )
        response_data = {
            "total_products": analytics['total_products'],
            "average_price": analytics['average_price'] or 0,
        }
        return Response(response_data)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Promotion
from .serializers import ProductSerializer, PromotionSerializer
from django.utils import timezone

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Endpoint: /api/products/new_arrivals/
    @action(detail=False, methods=['get'])
    def new_arrivals(self, request):
        new_products = self.get_queryset().filter(is_new_arrival=True)[:2]
        if not new_products.exists():
            new_products = self.get_queryset()[:2] # Fallback ke 2 terbaru
        serializer = self.get_serializer(new_products, many=True)
        return Response(serializer.data)

class PromotionViewSet(viewsets.ModelViewSet):
    serializer_class = PromotionSerializer

    def get_queryset(self):
        today = timezone.now().date()
        # Filter hanya promo yang aktif dan valid hari ini
        return Promotion.objects.filter(
            is_active=True,
            start_date__lte=today,
            end_date__gte=today
        ).order_by('-start_date')
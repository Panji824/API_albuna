from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, PromotionViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'promotions', PromotionViewSet, basename='promotion')

urlpatterns = [
    path('', include(router.urls)),
]
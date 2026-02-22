from rest_framework import viewsets
from .models import Product,Category,Inventory,StockMovement
from .serializers import ProductSerializer,CategorySerializer,InventorySerializer,StockMovementSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category','storage_type').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name','category','storage_type']

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.select_related('product','bin').all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product','bin']

class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.select_related('product','bin').all()
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product','bin','movement_type']


from rest_framework import viewsets
from .models import SalesOrder,SalesOrderItem
from .serializers import SalesOrderSerializer,SalesOrderItemSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'order_number':['exact','icontains'],
        'status':['exact'],
        'created_at': ['date', 'date__gte', 'date__lte']
    }
class SalesOrderItemViewSet(viewsets.ModelViewSet):
    queryset = SalesOrderItem.objects.select_related('salesorder','product').all()
    serializer_class = SalesOrderItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'order':['exact','icontains'],
        'quantity':['exact','icontains']
    }
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch
from .models import Warehouse,Zone,Rack,Bin,StorageType
from .serializers import WarehouseSerializer,ZoneSerializer,RackSerializer,BinSerializer,StorageTypeSerializer
from accounts.permissions import IsAdmin,IsManager


#Warehouse Viewset
class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.select_related('manager').all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active','location']


#Zone ViewSet
class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.select_related('warehouse','storage_type').all()
    serializer_class = ZoneSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['warehouse','storage_type']

# Rack ViewSet
class RackViewSet(viewsets.ModelViewSet):
    queryset = Rack.objects.select_related('zone').all()
    serializer_class = RackSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['zone']

# Bin Viewset
class BinViewSet(viewsets.ModelViewSet):
    queryset = Bin.objects.select_related('rack').all()
    serializer_class = BinSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rack','is_available']

class StorageTypeViewSet(viewsets.ModelViewSet):
    queryset = StorageType.objects.all()
    serializer_class = StorageTypeSerializer
    permission_classes = [IsAuthenticated]
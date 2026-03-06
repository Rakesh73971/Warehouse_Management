from rest_framework import viewsets
from .models import SalesOrder,SalesOrderItem
from .serializers import SalesOrderSerializer,SalesOrderItemSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .services import confirm_sales_order
from rest_framework.exceptions import ValidationError
from .pagination import DefaultPageSize

# Create your views here.
class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    pagination_class = DefaultPageSize
    filterset_fields = {
        'order_number':['exact','icontains'],
        'status':['exact'],
        'created_at': ['date', 'date__gte', 'date__lte']
    }
    @action(detail=True, methods=["post"])
    def confirm(self, request, pk=None):
        order = self.get_object()

        try:
            confirm_sales_order(order)
        except ValidationError as e:
            return Response(
                {"error": str(e.detail[0] if isinstance(e.detail, list) else e.detail)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": "Order confirmed successfully"},
            status=status.HTTP_200_OK
        )
class SalesOrderItemViewSet(viewsets.ModelViewSet):
    queryset = SalesOrderItem.objects.select_related('order','product').all()
    serializer_class = SalesOrderItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    pagination_class = DefaultPageSize
    filterset_fields = {
        'order': ['exact'],
        'product': ['exact'],
        'quantity': ['exact', 'gte', 'lte']
    }
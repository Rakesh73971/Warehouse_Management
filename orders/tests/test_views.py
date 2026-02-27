import pytest
from orders.models import SalesOrder,SalesOrderItem
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from products.models import Category,StorageType,Product

User = get_user_model()

@pytest.mark.django_db
class TestOrderAPI:

    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='manager@gmail.com',
            full_name='Test Manager',
            password='password123',
            role='MANAGER'
        )
        self.client.force_authenticate(user=self.user)

    # -----------------
    # SALESORDER TEST
    # -----------------

    def test_create_salesorder(self):
        response = self.client.post(
            '/api/order/salesorders/',
            {
                'order_number':'AZ001',
                'customer_name':'rakesh',
                'status':'COMPLETED'
            },
            format='json'
        )

        assert response.status_code == 201
        assert SalesOrder.objects.count() == 1

    def test_filter_order_number(self):
        SalesOrder.objects.create(order_number='AB123',customer_name='Rakesh',status='COMPLETED')
        SalesOrder.objects.create(order_number='AB124',customer_name='Gukesh',status='PENDING')

        response = self.client.get('/api/order/salesorders/?order_number=AB123')

        assert response.status_code == 200
        assert len(response.data) == 1

    
    # ---------------------
    # SALESORDERITEM TEST
    # ---------------------
    def test_create_salesorderitem(self):
        category = Category.objects.create(
            name='fruits'
        )
        storage = StorageType.objects.create(
            name='Cold Storage',
            temperature_range='10 to 25c'
        )

        product = Product.objects.create(
            name='Banana',
            sku='BA006',
            storage_type=storage,
            category=category
        )
        order = SalesOrder.objects.create(
            order_number='AB002',
            customer_name='Rakesh',
            status='COMPLETED'
        )
        response = self.client.post(
            '/api/order/salesorderitems/',
            {
                'order':order.id,
                'product':product.id,
                'quantity':10
            },
            format='json'
        )

        assert response.status_code == 201
        assert SalesOrderItem.objects.count() == 1


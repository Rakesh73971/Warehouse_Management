import pytest
from products.models import Category,Product,Inventory,StockMovement
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from warehouse.models import StorageType,Warehouse,Zone,Rack,Bin


User = get_user_model()

@pytest.mark.django_db
class TestProductAPI:

    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='manager@gmail.com',
            full_name='Test Manager',
            password='password123',
            role='MANAGER'
        )
        self.client.force_authenticate(user=self.user)


    # --------------
    # CATEGORY TEST
    # --------------
    def test_create_category(self):
        response = self.client.post(
            '/api/product/categories/',
            {
                'name':'clothes'
            },
            format='json'
        )
        assert response.status_code == 201
        assert Category.objects.count() == 1

    # -------------
    # PRODUCT TEST
    # -------------
    def test_create_product(self):
        category = Category.objects.create(
            name='fruits'
        )
        storage = StorageType.objects.create(
            name = 'Cold Storage',
            temperature_range = '10 to 25c'
        )
        response = self.client.post(
            '/api/product/products/',
            {
                'name':'banana',
                'sku':'BAN001',
                'storage_type':storage.id,
                'category':category.id
            },
            format='json'
        )

        assert response.status_code == 201
        assert Product.objects.count() == 1

    # ---------------
    # INVENTORY TEST
    # ---------------
    

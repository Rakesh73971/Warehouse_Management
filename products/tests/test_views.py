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
    def test_create_inventory(self):
        category = Category.objects.create(
            name='fruits'
        )
        storage = StorageType.objects.create(
            name='Cold Storage',
            temperature_range='10 to 25c'
        )
        product = Product.objects.create(
            name='banana',
            sku='BAN001',
            storage_type=storage,
            category=category
        )
        warehouse = Warehouse.objects.create(
            name='Main Warehouse',
            location='Hyderabad',
            manager=self.user
        )
        zone = Zone.objects.create(
            warehouse = warehouse,
            name = 'Zone X',
            description = ' '
        )

        rack = Rack.objects.create(
            zone = zone,
            rack_code = 'R001',
            max_capacity = 100
        )

        bin = Bin.objects.create(
            rack = rack,
            bin_code = 'B001',
            max_capacity = 100,
            current_capacity = 50
        )
        response = self.client.post(
            '/api/product/inventories/',
            {
                'product':product.id,
                'bin':bin.id,
                'quantity':5
            },
            format='json'
        )

        assert response.status_code == 201
        assert Inventory.objects.count() == 1
    
    def test_create_stockmovement(self):
        category = Category.objects.create(
            name='fruits'
        )
        storage = StorageType.objects.create(
            name='Cold Storage',
            temperature_range='10 to 25c'
        )
        product = Product.objects.create(
            name='banana',
            sku='BAN002',
            storage_type=storage,
            category=category
        )
        warehouse = Warehouse.objects.create(
            name='Main Warehouse',
            location='Hyderabad',
            manager=self.user
        )
        zone = Zone.objects.create(
            warehouse = warehouse,
            name = 'Zone X',
            description = ' '
        )

        rack = Rack.objects.create(
            zone = zone,
            rack_code = 'R001',
            max_capacity = 100
        )

        bin = Bin.objects.create(
            rack = rack,
            bin_code = 'B001',
            max_capacity = 100,
            current_capacity = 50
        )
        response = self.client.post(
            '/api/product/stockmovements/',
            {
                'product':product.id,
                'bin':bin.id,
                'quantity':5,
                'movement_type':'INBOUND'
            },
            format='json'
        )
        assert response.status_code == 201
        assert StockMovement.objects.count() == 1
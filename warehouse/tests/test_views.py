import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from warehouse.models import Warehouse,StorageType,Zone,Rack,Bin

User = get_user_model()

@pytest.mark.django_db
class TestWarehouseSystemAPI:

    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="manager@test.com",
            full_name="Manager",
            password="password123",
            role="MANAGER"
        )
        self.client.force_authenticate(user=self.user)

    #-----------------
    #WAREHOUSE TESTS
    #-----------------
    def test_create_warehouse(self):
        response = self.client.post(
            "/api/warehouse/warehouses/",
            {
                "name": "Main Warehouse",
                "location": "Hyderabad",
                "manager": self.user.id,
            },
            format="json"
        )
        assert response.status_code == 201
        assert Warehouse.objects.count() == 1

    def test_filter_warehouse_by_location(self):
        Warehouse.objects.create(name='W1',location='Hyderabad',manager=self.user)
        Warehouse.objects.create(name='W2',location='Delhi',manager=self.user)

        response = self.client.get('/api/warehouse/warehouses/?location=Delhi')

        assert response.status_code == 200
        assert len(response.data) == 1

    
    # ------------
    # STORAGE TYPE TEST
    # ------------
    def test_create_storage_type(self):
        response = self.client.post(
            "/api/warehouse/storagetypes/",{
                'name':'Cold Storages',
                'temperature_range':'-10 to 5C'
            },
            format='json'
        )
        assert response.status_code == 201
        assert len(response.data) == 3

    # ------------
    # ZONE TESTS
    # ------------
    def test_create_zone(self):
        warehouse = Warehouse.objects.create(
            name='Main Warehouse',
            location='Hyderabad',
            manager=self.user
        )

        storage = StorageType.objects.create(
            name='Cold Storage',
            temperature_range='-10 to 25'
        )

        response = self.client.post(
            '/api/warehouse/zones/',
            {
                'name':'Zone A',
                'warehouse':warehouse.id,
                'storag_type':storage.id
            },
            format='json'
        )

        assert response.status_code == 201
        assert len(response.data) == 6

    # -----------------
    # RACK TESTS
    # ------------------
    def test_create_rack(self):
        warehouse = Warehouse.objects.create(
            name='Main Warehouse',
            location='Hyderabad',
            manager=self.user
        )
        zone = Zone.objects.create(
            name='Zone A',
            warehouse=warehouse
        )
        response = self.client.post(
            '/api/warehouse/racks/',
            {
                'zone':zone.id,
                'rack_code':'R001',
                'max_capacity':100
            },
            format='json'
        )

        assert response.status_code == 201
        assert Rack.objects.count() == 1


    # -------------
    # BIN TESTS
    # -------------
    def test_create_bin(self):
        warehouse = Warehouse.objects.create(
            name='Main Warehouse',
            location='Hyderabad',
            manager=self.user
        )
        zone = Zone.objects.create(
            name='Zone A',
            warehouse=warehouse
        )
        rack = Rack.objects.create(
            zone = zone,
            rack_code = 'R001',
            max_capacity = 100
        )

        response = self.client.post(
            '/api/warehouse/bins/',
            {
                'bin_code':'B001',
                'max_capacity':100,
                'current_capacity':50,
                'rack':rack.id
            },
            format='json'
        )

        assert response.status_code == 201
        assert Bin.objects.count() == 1
        assert Bin.objects.first().is_available is True


    # ---------------
    # AUTH TEST
    # ---------------
    def test_unauthenticated_access(self):
        self.client.force_authenticate(user=None)
        
        response = self.client.post('/api/warehouse/warehouses/')
        assert response.status_code == 401
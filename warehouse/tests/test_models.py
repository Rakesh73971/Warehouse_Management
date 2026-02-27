import pytest
from django.contrib.auth import get_user_model
from warehouse.models import Warehouse,StorageType,Zone,Rack,Bin

User = get_user_model()

@pytest.mark.django_db
def test_create_warehouse():
    user = User.objects.create(
        email='manager@gmail.com',
        full_name="Test Manager",
        password="password123",
        role="MANAGER"
    )

    warehouse = Warehouse.objects.create(
        name = 'Central Warehouse',
        location = 'Hyderabad',
        manager=user
        
    )

    assert warehouse.manager.email == 'manager@gmail.com'
    assert str(warehouse) == 'Central Warehouse'


@pytest.mark.django_db
def test_storagetype():
    storagetype = StorageType.objects.create(
        name = 'SV storages',
        temperature_range = '-100'
    )

    assert storagetype.name == 'SV storages'
    assert storagetype.temperature_range == '-100'


@pytest.mark.django_db
def test_zone():
    user = User.objects.create(
        email='manager@gmail.com',
        full_name='Test Manager',
        password='password123',
        role='MANAGER'
    )
    warehouse = Warehouse.objects.create(
        name = 'Main Warehouse',
        location = 'Hyderabad',
        manager = user
    )
    storage = StorageType.objects.create(
        name = 'Dry storage',
        temperature_range = "10 to 25°C"
    )
    
    zone = Zone.objects.create(
        warehouse = warehouse,
        name = 'Zone A',
        description = " ",
        storage_type = storage
    )
    assert zone.warehouse.name == 'Main Warehouse'
    assert zone.storage_type.name == 'Dry storage'
    assert str(zone) == "Main Warehouse - Zone A"


@pytest.mark.django_db
def test_rack_creation():
    user = User.objects.create(
        email='manager@gmail.com',
        full_name='Test Manager',
        password='password123',
        role='MANAGER'
    )
    warehouse = Warehouse.objects.create(
        name = 'Main Warehouse',
        location = 'Hyderabad',
        manager = user
    )
    zone = Zone.objects.create(
        warehouse = warehouse,
        name = 'Zone 1'
    )
    rack = Rack.objects.create(
        zone = zone,
        rack_code = 'R001',
        max_capacity = 100
    )

    assert rack.zone.warehouse.name == 'Main Warehouse'
    assert str(rack) == "Rack R001"

@pytest.mark.django_db
def test_bin_capacity_and_availability():
    user = User.objects.create(
        email='manager@gmail.com',
        full_name='Test Manager',
        password='password123',
        role='MANAGER'
    )
    warehouse = Warehouse.objects.create(
        name='Main Warehouse',
        location='Hyderabad',
        manager=user
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
    assert bin.is_available is True

    bin.current_capacity = 100
    bin.save()

    bin.refresh_from_db()
    assert bin.is_available is False
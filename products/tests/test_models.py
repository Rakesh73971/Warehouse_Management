import pytest
from products.models import Category,Product,Inventory,StockMovement
from warehouse.models import StorageType,Bin,Rack,Zone,Warehouse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_category():
    category = Category.objects.create(
        name='shoes'
    )

    assert category.name == 'shoes'

@pytest.mark.django_db
def test_product_model():
    category = Category.objects.create(
        name = 'clothes'
    )
    storage = StorageType.objects.create(
        name='Cold Storage',
        temperature_range='10 to 25c'
    )
    product = Product.objects.create(
        name='shirts',
        sku='',
        storage_type = storage,
        category = category
    )

    assert product.category.name == 'clothes'
    assert product.name == 'shirts'
    assert product.storage_type.name == 'Cold Storage'

@pytest.mark.django_db
def test_inventory_model():
    category = Category.objects.create(
        name='clothes'
    )
    storage = StorageType.objects.create(
        name='Cold Storage',
        temperature_range='10 to 25'
    )
    product  = Product.objects.create(
        name='shirts',
        sku='',
        storage_type=storage,
        category=category
    )

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
    inventory = Inventory.objects.create(
        product = product,
        bin = bin,
        quantity = 10
    )

    assert inventory.product.name == 'shirts'
    assert inventory.bin.rack.zone.warehouse.name == 'Main Warehouse'

@pytest.mark.django_db
def test_stockmovement_model():
    category = Category.objects.create(
        name='clothes'
    )
    storage = StorageType.objects.create(
        name='Cold Storage',
        temperature_range='10 to 25'
    )
    product  = Product.objects.create(
        name='shirts',
        sku='',
        storage_type=storage,
        category=category
    )

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
    stockmovement = StockMovement.objects.create(
        product = product,
        bin = bin,
        quantity = 3,
        movement_type = 'Inbound'
    )

    assert stockmovement.product.name == 'shirts'
    assert stockmovement.quantity == 3
    assert stockmovement.bin.rack.zone.warehouse.name == 'Main Warehouse'
    assert stockmovement.bin.rack.zone.warehouse.manager.full_name == 'Test Manager'
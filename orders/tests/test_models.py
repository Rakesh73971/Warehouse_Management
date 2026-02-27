import pytest
from orders.models import SalesOrder,SalesOrderItem
from products.models import Product,Category,StorageType

@pytest.mark.django_db
def test_salesorder_model():
    salesorder = SalesOrder.objects.create(
        order_number='AZ001',
        customer_name='rakesh',
        status="COMPLETED"
    )
    assert salesorder.customer_name == 'rakesh'

@pytest.mark.django_db
def test_salesorderitem_model():
    salesorder = SalesOrder.objects.create(
        order_number='AB001',
        customer_name='rakesh',
        status='COMPLETED'    
    )
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
    salesorderitem = SalesOrderItem.objects.create(
        order = salesorder,
        product = product,
        quantity = 10
    )
    
    assert salesorderitem.product.category.name == 'fruits'
    assert salesorderitem.quantity == 10

    
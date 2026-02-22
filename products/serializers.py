from rest_framework import serializers
from .models import Category,Product,Inventory,StockMovement

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name',read_only=True)
    storage_type_name = serializers.CharField(source='storage_type.name',read_only=True)
    class Meta:
        model = Product
        fields = ['name','sku','description','storage_type','storage_type_name','category','category_name','weight','created_at']

class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name',read_only=True)
    bin_name = serializers.CharField(source='bin.name',read_only=True)
    class Meta:
        model = Inventory
        fields = ['product','product_name','bin','bin_name','quantity']

class StockMovementSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name',read_only=True)
    bin_name = serializers.CharField(source='bin.name',read_only=True)

    class Meta:
        model = StockMovement
        fields = ['product','product_name','bin','bin_name','quantity','movement_type','created_at']
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Products, Item

class ProductsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Products
        fields = ['name', 'price', 'image', 'owner']

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['name', 'price', 'image', 'tag', 'best']


class UserSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, queryset=Products.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'products']

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
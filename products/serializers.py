from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Products, Item, Profile

class ProductsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Products
        fields = ['id', 'name', 'price', 'image', 'bought', 'owner']

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'name', 'price', 'image', 'tag', 'best']


class UserSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, queryset=Products.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'products']

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'password', 'image']
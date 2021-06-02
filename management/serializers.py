from rest_framework import serializers

from management.models import Category, Product


class CreateCustomerSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=15)
    last_name = serializers.CharField(max_length=15)
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField(max_length=30)


class LoginSerializer(serializers.Serializer):
    """
    This class is created for login.
    """

    email = serializers.EmailField(max_length=150)
    password = serializers.CharField(max_length=30)


class CategorySerializer(serializers.Serializer):
    """
    This class is created to validate the category field.
    """

    name = serializers.CharField(required=True)


class ProductSerializer(serializers.Serializer):
    """
    This class is created to validate the product field.
    """

    product_name = serializers.CharField()
    image = serializers.ImageField()
    category = serializers.IntegerField()
    description = serializers.CharField()


class ProductResponseSerializer(serializers.Serializer):
    """
    This class is created to validate the product field.
    """

    product_name = serializers.CharField()
    image = serializers.CharField()
    category = CategorySerializer()
    description = serializers.CharField()

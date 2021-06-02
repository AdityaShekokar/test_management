from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    """
    This model is created to for category management.
    """

    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    This model is created for product management.
    """

    product_name = models.CharField(max_length=255)
    # tags = models.ManyToManyField("tag", through_fields="products_tag")
    image = models.ImageField(upload_to="product_images/")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    description = models.CharField(max_length=255)

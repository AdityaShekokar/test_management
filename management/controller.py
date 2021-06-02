from http import HTTPStatus

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from service_objects.services import Service

from management.models import Category, Product
from management.serializers import CategorySerializer, ProductResponseSerializer
from management.signals import delete_product_image, delete_product_old_image


class CreateCategoryService(Service):
    """
    This class is created for the creation of categories.
    """

    def process(self):
        data = self.data
        cat = Category.objects.create(user=data.user, name=data.data["name"])
        return Response(
            {"message": "Successfully created the category..", "id": cat.id}
        )


class ListCategoryService(Service):
    """
    This class is created for the list of categories.
    """

    def process(self):
        categories = Category.objects.filter(user=self.data)
        serial_data = CategorySerializer(categories, many=True)
        return Response(
            {
                "message": "Successfully get the list of categories.",
                "data": serial_data.data,
            }
        )


class DetailCategoryService(Service):
    """
    This class is created for the detail of categories.
    """

    def process(self):
        try:
            data = self.data
            cat = Category.objects.get(id=data["pk"], user=data["user"])
            serial_data = CategorySerializer(cat)
            return Response(
                {
                    "message": "Successfully fetch the detail of category.",
                    "data": serial_data.data,
                }
            )
        except ObjectDoesNotExist:
            return Response(
                {"message": "Category doesn't exists."}, status=HTTPStatus.NOT_FOUND
            )


class DeleteCategoryService(Service):
    """
    This class is created for the delete of categories.
    """

    def process(self):
        try:
            data = self.data
            cat = Category.objects.get(id=data["pk"], user=data["user"])
            cat.delete()
            return Response({"message": "Successfully delete the category."})
        except ObjectDoesNotExist:
            return Response(
                {"message": "Category doesn't exists."}, status=HTTPStatus.NOT_FOUND
            )


class UpdateCategoryService(Service):
    """
    This class is created for the update of categories.
    """

    def process(self):
        try:
            data = self.data
            cat = Category.objects.get(id=data["pk"], user=data["user"])
            cat.name = data["data"]["name"]
            cat.save()
            return Response({"message": "Successfully update the category."})
        except ObjectDoesNotExist:
            return Response(
                {"message": "Category doesn't exists."}, status=HTTPStatus.NOT_FOUND
            )


class CreateProductService(Service):
    """
    This class is created to create the product.
    """

    def process(self):
        try:
            data = self.data.data
            category = Category.objects.get(id=data["category"])
            product = Product.objects.create(
                product_name=data["product_name"],
                image=data["image"],
                category=category,
                description=data["description"],
            )
            return Response(
                {"message": "Successfully created the products.", "id": product.id}
            )
        except ObjectDoesNotExist:
            return Response(
                {"message": "Category doesn't exists."}, status=HTTPStatus.NOT_FOUND
            )


class ListProductService(Service):
    """
    This class is created to fetch the list of products.
    """

    def process(self):
        products = Product.objects.filter(category_id__user=self.data)
        serial_data = ProductResponseSerializer(products, many=True)
        return Response(
            {
                "message": "Successfully get the list of product.",
                "data": serial_data.data,
            }
        )


class DetailProductService(Service):
    """
    This class is created to fetch the detail of products.
    """

    def process(self):
        try:
            data = self.data
            product = Product.objects.get(id=data["pk"], category_id__user=data["user"])
            serial_data = ProductResponseSerializer(product)
            return Response(
                {
                    "message": "Successfully fetch the detail of product.",
                    "data": serial_data.data,
                }
            )
        except ObjectDoesNotExist:
            return Response(
                {"message": "Product doesn't exists."}, status=HTTPStatus.NOT_FOUND
            )


class DeleteProductService(Service):
    """
    This class is created to fetch the delete of products.
    """

    def process(self):
        try:
            data = self.data
            product = Product.objects.get(id=data["pk"], category_id__user=data["user"])
            product.delete()
            return Response({"message": "Successfully delete the product."})
        except ObjectDoesNotExist:
            return Response(
                {"message": "Product doesn't exists."}, status=HTTPStatus.NOT_FOUND
            )


class UpdateProductService(Service):
    """
    This class is created to fetch the update of products.
    """

    def process(self):
        try:
            data = self.data["data"]
            category = Category.objects.get(id=data.data["category"], user=data.user)
            product = Product.objects.get(
                id=self.data["pk"], category_id__user=data.user
            )
            product.product_name = data.data["product_name"]
            product.image = data.data["image"]
            product.category = category
            product.description = data.data["description"]
            product.save()
            return Response({"message": "Successfully update the category."})
        except Category.DoesNotExist:
            return Response(
                {"message": "Category doesn't exists."}, status=HTTPStatus.NOT_FOUND
            )
        except Product.DoesNotExist:
            return Response(
                {"message": "Product doesn't exists."}, status=HTTPStatus.NOT_FOUND
            )

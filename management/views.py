from http import HTTPStatus

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from oauth2_provider.contrib.rest_framework import (
    OAuth2Authentication,
    TokenMatchesOASRequirements,
)
from oauth2_provider.models import Application
from rest_framework.response import Response
from rest_framework.views import APIView

from management.controller import (
    CreateCategoryService,
    CreateProductService,
    DeleteCategoryService,
    DeleteProductService,
    DetailCategoryService,
    DetailProductService,
    ListCategoryService,
    ListProductService,
    UpdateCategoryService,
    UpdateProductService,
)
from management.serializers import (
    CategorySerializer,
    CreateCustomerSerializer,
    LoginSerializer,
    ProductSerializer,
)
from management.utils import create_token, validate_email


class CreateLoginView(APIView):
    """
    This class is created to login the user.
    """

    @staticmethod
    def post(request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                with transaction.atomic():
                    serial_data = serializer.validated_data
                    username = serial_data.get("email")
                    password = serial_data.get("password")
                    user = User.objects.get(username=username)
                    validate_user = authenticate(username=username, password=password)
                    if validate_user is None:
                        return Response(
                            {"message": "invalid credential"},
                            status=HTTPStatus.BAD_REQUEST,
                        )
                app = Application.objects.filter(user=user)
                token = create_token(
                    user.username,
                    password,
                    app.first().client_id,
                    app.first().client_secret,
                )
                return Response(token, status=HTTPStatus.CREATED)
        except User.DoesNotExist:
            return Response(
                {"message": "User doesn't exists."}, status=HTTPStatus.NOT_FOUND
            )


class CreateRegisterView(APIView):
    """
    This class is created to register the user.
    """

    @staticmethod
    def post(request):
        serializer = CreateCustomerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                serial_data = serializer.validated_data
                email = serial_data.get("email")
                validate_email(email)
                user = User.objects.create(
                    first_name=serial_data.get("first_name"),
                    last_name=serial_data.get("last_name"),
                    username=email,
                    email=email,
                )
                user.set_password(serial_data.get("password"))
                user.save()
                application = Application.objects.create(
                    user=user,
                    authorization_grant_type="password",
                    client_type="confidential",
                    name="user",
                )
            token_data = create_token(
                user,
                serial_data.get("password"),
                application.client_id,
                application.client_secret,
            )
            return Response(token_data, status=HTTPStatus.CREATED)


class CreateListCategoryView(APIView):
    """
    This class is created for the list and create category views.
    """

    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenMatchesOASRequirements]

    required_alternate_scopes = {
        "POST": [["create"]],
        "GET": [["read"]],
    }

    @staticmethod
    def post(request):
        serial_data = CategorySerializer(data=request.data)
        if serial_data.is_valid(raise_exception=True):
            return CreateCategoryService.execute(inputs=request)

    @staticmethod
    def get(request):
        return ListCategoryService.execute(inputs=request.user)


class DetailCategoryView(APIView):
    """
    This class is created for the detail, update, delete category views.
    """

    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenMatchesOASRequirements]

    required_alternate_scopes = {
        "GET": [["read"]],
        "PUT": [["create"]],
        "DELETE": [["delete"]],
    }

    @staticmethod
    def get(request, pk):
        return DetailCategoryService.execute({"user": request.user, "pk": pk})

    @staticmethod
    def delete(request, pk):
        return DeleteCategoryService.execute({"user": request.user, "pk": pk})

    @staticmethod
    def put(request, pk):
        serial_data = CategorySerializer(data=request.data)
        if serial_data.is_valid(raise_exception=True):
            return UpdateCategoryService.execute(
                {"user": request.user, "data": request.data, "pk": pk}
            )


class CreateListProductView(APIView):
    """
    This class is created for the list and create products views.
    """

    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenMatchesOASRequirements]

    required_alternate_scopes = {
        "POST": [["create"]],
        "GET": [["read"]],
    }

    @staticmethod
    def post(request):
        serial_data = ProductSerializer(data=request.data)
        if serial_data.is_valid(raise_exception=True):
            return CreateProductService.execute(inputs=request)

    @staticmethod
    def get(request):
        return ListProductService.execute(inputs=request.user)


class DetailProductView(APIView):
    """
    This class is created for the detail, update, delete product views.
    """

    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenMatchesOASRequirements]

    required_alternate_scopes = {
        "GET": [["read"]],
        "PUT": [["create"]],
        "DELETE": [["delete"]],
    }

    @staticmethod
    def get(request, pk):
        return DetailProductService.execute({"user": request.user, "pk": pk})

    @staticmethod
    def delete(request, pk):
        return DeleteProductService.execute({"user": request.user, "pk": pk})

    @staticmethod
    def put(request, pk):
        serial_data = ProductSerializer(data=request.data)
        if serial_data.is_valid(raise_exception=True):
            return UpdateProductService.execute({"data": request, "pk": pk})

from django.urls import path

from management.views import (
    CreateListCategoryView,
    CreateListProductView,
    CreateLoginView,
    CreateRegisterView,
    DetailCategoryView,
    DetailProductView,
)

urlpatterns = [
    path(
        "categories/", CreateListCategoryView.as_view(), name="create_list_category_api"
    ),
    path(
        "category/<int:pk>/", DetailCategoryView.as_view(), name="detail_category_api"
    ),
    path("products/", CreateListProductView.as_view(), name="create_list_product_api"),
    path("product/<int:pk>/", DetailProductView.as_view(), name="detail_product_api"),
    path("register/", CreateRegisterView.as_view(), name="register_endpoint"),
    path("login/", CreateLoginView.as_view(), name="login_endpoint"),
]

from django.contrib import admin
from django.utils.safestring import mark_safe

from management.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_filter = ["name"]
    search_fields = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["product_name", "get_image", "category", "description"]
    list_filter = ["product_name"]
    search_fields = ["product_name"]

    def get_image(self, obj):
        """
        This method used to display image in recipes listing on admin panel.
        """
        if obj.image:
            return mark_safe(
                '<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(
                    obj.image.url
                )
            )
        return mark_safe("<p style='color:red;'>No-image</p>")

    # Added for heading name in recipes listing.
    get_image.short_description = "Image"

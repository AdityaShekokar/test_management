import os

from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from management.models import Product
from test_management.settings import MEDIA_URL


@receiver(pre_delete, sender=Product)
def delete_product_image(sender, instance, **kwargs):
    # on creation, signal callback won't be triggered
    if instance._state.adding and not instance.pk:
        return False

    try:
        image = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False
    path = MEDIA_URL[1:] + image.name
    if os.path.isfile(path):
        os.remove(path)


@receiver(pre_save, sender=Product)
def delete_product_old_image(sender, instance, **kwargs):
    # on creation, signal callback won't be triggered
    if instance._state.adding and not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False

    # comparing the new file with the old one
    image = instance.image
    path = MEDIA_URL[1:] + old_file.name
    if not old_file == image:
        if os.path.isfile(path):
            os.remove(path)

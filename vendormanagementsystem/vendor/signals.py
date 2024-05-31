from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder
from .views import update_vendor_performance

@receiver(post_save, sender=PurchaseOrder)
def update_performance(sender, instance, **kwargs):
    if instance.status == 'completed' and instance.vendor:
        update_vendor_performance(instance.vendor.id)

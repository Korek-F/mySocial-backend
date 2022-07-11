from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Notification
from main_auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .serializers import NotificationSerializer

@receiver(post_save, sender=Notification)
def create_new_notification(sender, instance, created, *args, **kwargs):
    print("TESTO")
    if created:
        channel_layer = get_channel_layer()
        print(instance.to_user.username)
        print(channel_layer)
        async_to_sync(channel_layer.group_send)(
            f'noti_{instance.to_user.username}',
            {
                "type":"send_status",
                "data":"TEST"
            }
        )
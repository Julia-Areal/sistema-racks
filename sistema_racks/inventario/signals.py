from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Switch, Porta

@receiver(post_save, sender=Switch)
def criar_portas(sender, instance, created, **kwargs):
    if created:
        for i in range(1, instance.quantidade_portas + 1):
            Porta.objects.create(switch=instance, numero=i)

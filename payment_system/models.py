from django.db import models

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


class Wallet(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    currency = models.CharField(max_length=3, default='USD', editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.owner}: {self.balance}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(owner=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.wallet.save()


class FillUp(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)


class Transfer(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='owner')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='recipient')
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.owner} -> {self.recipient}: {self.amount}'


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



import decimal
import logging
logger = logging.getLogger(__name__)

from django.db import transaction
# from django.contrib.auth.models import User

from rest_framework.exceptions import ValidationError
from rest_framework import generics

from .permissions import IsOwner
from .models import Wallet, Transfer, FillUp
from .serializers import FillUpSerializer, TransferSerializer, WalletSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class EnforceOwnerMixin:

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AdminReadAllRestOnlyOwnedMixin:

    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        else:
            return self.queryset.filter(owner=self.request.user)


class TransferCreate(generics.CreateAPIView, EnforceOwnerMixin):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        sender_wallet = Wallet.objects.get(owner=request.user.id)
        amount = decimal.Decimal(request.POST["amount"])

        if sender_wallet.balance < amount:
            msg = f"Current balance {sender_wallet.balance} is less than requested transfer {amount}"
            raise ValidationError(msg)

        recipient_id = request.POST["recipient"]
        recipient_wallet = Wallet.objects.get(owner=recipient_id)

        sender_wallet.balance -= amount
        recipient_wallet.balance += amount

        sender_wallet.save()
        recipient_wallet.save()

        return self.create(request, *args, **kwargs)


class FillUpCreate(generics.CreateAPIView, EnforceOwnerMixin):
    permission_classes = (IsAuthenticated,)
    queryset = FillUp.objects.all()
    serializer_class = FillUpSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        target_wallet = Wallet.objects.get(owner=request.user.id)
        amount = decimal.Decimal(request.POST["amount"])

        target_wallet.balance += amount
        target_wallet.save()

        return self.create(request, *args, **kwargs)


class TransferList(AdminReadAllRestOnlyOwnedMixin, generics.ListAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [IsAdminUser | IsOwner]


class FillUpList(generics.ListAPIView, AdminReadAllRestOnlyOwnedMixin):
    queryset = FillUp.objects.all()
    serializer_class = FillUpSerializer
    permission_classes = [IsAdminUser | IsOwner]


class WalletList(generics.ListAPIView, AdminReadAllRestOnlyOwnedMixin):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAdminUser | IsOwner]


from rest_framework import serializers
from .models import Wallet, Transfer, FillUp


class FillUpSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'owner', 'amount')
        model = FillUp


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'owner', 'balance', 'currency', 'created_at', 'updated_at')
        model = Wallet


class TransferSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'owner', 'recipient', 'amount', 'created_at')
        model = Transfer


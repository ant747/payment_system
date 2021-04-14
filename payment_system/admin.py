from django.contrib import admin
from .models import Wallet, Transfer, FillUp


admin.site.register(Wallet)
admin.site.register(FillUp)
admin.site.register(Transfer)

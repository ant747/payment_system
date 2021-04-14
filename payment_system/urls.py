from django.urls import path
from .views import TransferCreate, FillUpList, FillUpCreate, TransferList, WalletList

urlpatterns = [
    # path('<int:pk>/', PostDetail.as_view()),
    # path('payment_system', PostList.as_view()),
    path('transfer', TransferCreate.as_view()),
    path('transfers', TransferList.as_view()),
    path('fill_up', FillUpCreate.as_view()),
    path('fill_ups', FillUpList.as_view()),
    path('wallets', WalletList.as_view()),
]

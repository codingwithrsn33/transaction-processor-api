from django.contrib import admin
from django.urls import path
from transactions.views import HealthCheck, WebhookTransaction, TransactionStatus

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HealthCheck.as_view(), name='health'),
    path('v1/webhooks/transactions', WebhookTransaction.as_view(), name='webhook'),
    path('v1/transactions/<str:transaction_id>', TransactionStatus.as_view(), name='transaction-status'),
]

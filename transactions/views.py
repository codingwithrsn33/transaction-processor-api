from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction as db_transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
import threading, time

from .models import Transaction


# ---------- Background Processing ----------
def process_transaction(transaction_id):
    """Simulate external API delay and mark transaction as processed."""
    time.sleep(30)  # simulate 30-second external API delay
    try:
        tx = Transaction.objects.get(transaction_id=transaction_id)
        tx.status = "PROCESSED"
        tx.processed_at = timezone.now()
        tx.save()
        print(f"✅ Transaction {transaction_id} processed successfully.")
    except Transaction.DoesNotExist:
        print(f"⚠️ Transaction {transaction_id} not found for processing.")


# ---------- Health Check Endpoint ----------
class HealthCheck(APIView):
    def get(self, request):
        return Response({
            "status": "HEALTHY",
            "current_time": timezone.now().isoformat()
        })


# ---------- Webhook Receiver ----------
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import time

class WebhookTransaction(APIView):
    def post(self, request):
        data = request.data
        transaction_id = data.get("transaction_id")

        if not transaction_id:
            return Response(
                {"error": "transaction_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )




        # Idempotency check: only one transaction per ID
        with db_transaction.atomic():
            tx, created = Transaction.objects.get_or_create(
                transaction_id=transaction_id,
                defaults={
                    "source_account": data.get("source_account"),
                    "destination_account": data.get("destination_account"),
                    "amount": data.get("amount"),
                    "currency": data.get("currency"),
                    "status": "PROCESSING",
                    "created_at": timezone.now(),
                    "processed_at": None,
                }
            )

            if created:
                # Start background thread for processing
                threading.Thread(
                    target=process_transaction,
                    args=(transaction_id,),
                    daemon=True
                ).start()
                print(f"🟡 Started background processing for {transaction_id}.")
            else:
                print(f"ℹ️ Transaction {transaction_id} already exists (idempotent).")

        return Response({"message": "Accepted"}, status=status.HTTP_202_ACCEPTED)


# ---------- Transaction Status Check ----------
class TransactionStatus(APIView):
    def get(self, request, transaction_id):
        tx = get_object_or_404(Transaction, transaction_id=transaction_id)
        return Response({
            "transaction_id": tx.transaction_id,
            "source_account": tx.source_account,
            "destination_account": tx.destination_account,
            "amount": float(tx.amount),
            "currency": tx.currency,
            "status": tx.status,
            "created_at": tx.created_at,
            "processed_at": tx.processed_at
        })

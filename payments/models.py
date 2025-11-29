from django.db import models
import uuid
from django.utils import timezone
import os

def generate_txn_id():
    return f"TXN-{timezone.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"

def qr_upload_path(instance, filename):
    return os.path.join('qrs', f"{instance.txn_id}.png")

def invoice_upload_path(instance, filename):
    return os.path.join('invoices', f"{instance.txn_id}.pdf")

class Payment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    ]

    txn_id = models.CharField(max_length=40, unique=True, default=generate_txn_id)
    merchant = models.CharField(max_length=120, default="Mohammad Abrar Alam")
    upi_id = models.CharField(max_length=80, default="8757128380@ptaxis")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    qr_image = models.ImageField(upload_to=qr_upload_path, null=True, blank=True)
    invoice_pdf = models.FileField(upload_to=invoice_upload_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.txn_id} | ₹{self.amount} | {self.payment_status}"

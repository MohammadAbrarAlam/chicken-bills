
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, FileResponse
from .forms import PaymentForm
from .models import Payment
from .utils import generate_upi_url, generate_qr_file, create_invoice_pdf
import os

def payment_page(request):
    qr_url = None
    upi_url = None
    payment_obj = None

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            merchant = "Mohammad Abrar Alam"
            upi_id = "8757128380@ptaxis"
            # Create DB record first (so txn_id exists)
            payment_obj = Payment.objects.create(merchant=merchant, upi_id=upi_id, amount=amount)
            # Prepare paths
            qr_rel_path = f"qrs/{payment_obj.txn_id}.png"
            qr_full_path = os.path.join(settings.MEDIA_ROOT, qr_rel_path)
            upi_url = generate_upi_url(upi_id, merchant, str(amount))
            # Generate QR (upi_url embedded)
            try:
                generate_qr_file(upi_url, qr_full_path)
                # attach to model
                payment_obj.qr_image.name = qr_rel_path
                payment_obj.save()
            except Exception as e:
                # QR fail - still keep payment record
                print("QR gen failed:", e)
            # Create invoice PDF and attach
            invoice_rel = f"invoices/{payment_obj.txn_id}.pdf"
            invoice_full = os.path.join(settings.MEDIA_ROOT, invoice_rel)
            try:
                create_invoice_pdf(payment_obj, invoice_full)
                payment_obj.invoice_pdf.name = invoice_rel
                payment_obj.save()
            except Exception as e:
                print("Invoice generation failed:", e)

            # prepare template variables
            qr_url = settings.MEDIA_URL + payment_obj.qr_image.name if payment_obj.qr_image else None
            upi_url = upi_url
            return render(request, 'payments/payment_page.html', {
                'form': form, 'qr_url': qr_url, 'upi_url': upi_url, 'payment': payment_obj
            })
    else:
        form = PaymentForm()

    return render(request, 'payments/payment_page.html', {'form': form, 'qr_url': qr_url, 'upi_url': upi_url})

def history_view(request):
    payments = Payment.objects.order_by('-created_at')
    return render(request, 'payments/history.html', {'payments': payments})

def download_invoice(request, txn_id):
    payment = get_object_or_404(Payment, txn_id=txn_id)
    if not payment.invoice_pdf:
        return HttpResponse("Invoice not available", status=404)
    path = os.path.join(settings.MEDIA_ROOT, payment.invoice_pdf.name)
    return FileResponse(open(path, 'rb'), as_attachment=True, filename=os.path.basename(path))

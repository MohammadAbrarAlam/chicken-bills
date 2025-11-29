import qrcode
import os
from io import BytesIO
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.conf import settings

def generate_upi_url(upi_id: str, merchant: str, amount: str) -> str:
    # amount should be a string or decimal
    return f"upi://pay?pa={upi_id}&pn={merchant}&am={amount}&cu=INR"

def generate_qr_file(upi_url: str, output_path: str) -> str:
    # Ensure qrcode and pillow installed
    qr = qrcode.QRCode(box_size=8, border=2)
    qr.add_data(upi_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    # Save as PNG
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    return output_path

def create_invoice_pdf(payment, output_path: str) -> str:
    """Create a simple PDF invoice containing payment details and embedded QR image if present."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    c = canvas.Canvas(output_path, pagesize=A4)
    w, h = A4
    x = 50
    y = h - 80
    c.setFont('Helvetica-Bold', 18)
    c.drawString(x, y, 'Chicken Shop - Invoice')
    c.setFont('Helvetica', 12)
    y -= 30
    c.drawString(x, y, f"Transaction ID: {payment.txn_id}")
    y -= 18
    c.drawString(x, y, f"Merchant: {payment.merchant}")
    y -= 18
    c.drawString(x, y, f"UPI ID: {payment.upi_id}")
    y -= 18
    c.drawString(x, y, f"Amount: ₹{payment.amount}")
    y -= 18
    c.drawString(x, y, f"Date: {payment.created_at.strftime('%Y-%m-%d %H:%M:%S') if payment.created_at else ''}")
    y -= 30

    # If QR exists, embed it
    if payment.qr_image:
        try:
            qr_path = os.path.join(settings.MEDIA_ROOT, payment.qr_image.name)
            # Draw QR at right side of the page
            c.drawImage(qr_path, x, y-210, width=180, height=180)
        except Exception:
            pass

    c.showPage()
    c.save()
    return output_path

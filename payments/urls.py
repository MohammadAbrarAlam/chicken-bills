from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.payment_page, name='payment_page'),
    path('history/', views.history_view, name='history'),
    path('invoice/<str:txn_id>/download/', views.download_invoice, name='download_invoice'),
]

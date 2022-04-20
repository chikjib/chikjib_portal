from webbrowser import get
from django.urls import path,include

from dashboard.views import DashboardView, FundView, PaymentNotificationView, SupportView, TransactionView, portal_webhook

urlpatterns = [
   path('dashboard/',DashboardView.as_view(),name="dashboard"),
   path('transactions/',TransactionView.as_view(),name="transactions"),
   path('support/',SupportView.as_view(),name="support"),
   path('fund-wallet/',FundView,name="fund_wallet"),
   path('payment-notification/',PaymentNotificationView,name="payment_notification"),
   path('webhooks/portal/gSNASGvCxgbJTMthPQNXVRSfDdUtCLXJ/',portal_webhook, name="portal_webhook"),
   # path('check-transaction/',getFunds,name="getfunds"),
]
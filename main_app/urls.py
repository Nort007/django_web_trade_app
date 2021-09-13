from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_page, name='dashboard'),
    path('trade', views.trade_view, name='trade'),
    path('cancel_trade/<event_id>', views.cancel_trade, name='cancel_trade'),
    path('ajax/load-symbols', views.load_symbols, name='ajax_load_symbols'),
]
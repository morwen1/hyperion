from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OrderBookConfig(AppConfig):
    name = "orderbook_veinte.orderbook"
    verbose_name = _("OrderBook")


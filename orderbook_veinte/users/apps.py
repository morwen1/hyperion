from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "orderbook_veinte.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import orderbook_veinte.users.signals  # noqa F401
        except ImportError:
            pass

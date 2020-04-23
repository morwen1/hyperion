from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from orderbook_veinte.users.api.views import UserViewSet
from orderbook_veinte.orderbook.views import CreateBids
if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

#router.register("users", UserViewSet)
router.register('bids' , CreateBids)

app_name = "api"
urlpatterns = router.urls




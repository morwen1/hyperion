from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from orderbook_veinte.users.api.views import UserViewSet
from orderbook_veinte.orderbook.views import CreateBids, CreateAsks , TransactionViewset , OrderUserViewset
if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

#router.register("users", UserViewSet)
router.register(r'orderbook/bids/(?P<qty>[A-z]+)/(?P<price>[A-z]+)', CreateBids, basename='bids')
router.register(r'orderbook/asks/(?P<qty>[A-z]+)/(?P<price>[A-z]+)' , CreateAsks, basename='aks')
router.register(r'orderbook/transactions/(?P<qty>[A-z]+)/(?P<price>[A-z]+)' , TransactionViewset , basename='transactions')
router.register(r'user/orders' , OrderUserViewset , basename= 'orders_user')
app_name = "api"
urlpatterns = router.urls




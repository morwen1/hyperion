from rest_framework.viewsets import mixins , GenericViewSet
from rest_framework.permissions import AllowAny
from orderbook_veinte.orderbook.models import Transactions

from orderbook_veinte.orderbook.serializers import TransactionSerializer



class TransactionViewset(
    GenericViewSet, 
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin, 
    ):
    permission_classes = [AllowAny , ]
    serializer_class = TransactionSerializer
    queryset = Transactions.objects.all()[:10]
    
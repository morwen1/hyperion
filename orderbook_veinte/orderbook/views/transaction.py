from django.db.models import Q
from rest_framework.viewsets import mixins , GenericViewSet

from rest_framework.permissions import AllowAny
from orderbook_veinte.orderbook.models import Transactions

from orderbook_veinte.orderbook.serializers import TransactionSerializer



class TransactionViewset(
    GenericViewSet, 
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin, 
    ):


    def dispatch(self , request ,*args , **kwargs):
        self.qty = kwargs['qty']
        self.price = kwargs['price'] 
        return super(TransactionViewset , self).dispatch(request , *args , **kwargs)



    def get_queryset(self) :

        qry = Transactions.objects.filter(Q(market_qty = self.qty ) & Q(market_price = self.price)).order_by("-created_at")[:10]
        return qry
    permission_classes = [AllowAny , ]
    serializer_class = TransactionSerializer
    
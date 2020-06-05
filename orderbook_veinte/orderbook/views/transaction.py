from django.db.models import Q
from rest_framework.viewsets import mixins , GenericViewSet

from rest_framework.permissions import AllowAny

from orderbook_veinte.orderbook.models import Transactions

#permissions 
from orderbook_veinte.utils.permissions import LazyAuthenticated


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


            
    def get_permissions (self):
        permission = []
        if self.action in ['list','retrieve'] : 
            permision =  [AllowAny ,  IsAuthenticatedOrReadOnly ]
        elif self.action in[ 'create' , 'partial' , 'update']:
            permision = [LazyAuthenticated, ]
        
        return [p() for p in permision]


    def get_queryset(self) :

        qry = Transactions.objects.filter(Q(market_qty = self.qty ) & 
        Q(market_price = self.price)).order_by("-created_at")[:10]

        if self.action == 'retrieve':
            user_id = self.request.user.trader_id
            qry = Transactions.objects.filter(
                Q(buyer__TraderId=user_id) | Q(seller__TraderId=user_id) 
                 & Q(market_qty = self.qty ) & Q(market_price = self.price)
                ).order_by("-created_at")


        return qry
    permission_classes = [AllowAny , ]
    serializer_class = TransactionSerializer
    
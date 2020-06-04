#Rest framework
from rest_framework.generics import mixins 
from rest_framework.viewsets import GenericViewSet
#models 

from orderbook_veinte.orderbook.models.Order import Orders

#permissions 
from orderbook_veinte.utils.permissions import LazyAuthenticated

#serializer 
from orderbook_veinte.orderbook.serializers import UserOrderSerializer

class OrderUserViewset(GenericViewSet , mixins.ListModelMixin):
    

    permission_classes = [LazyAuthenticated , ]


    def get_queryset(self):
        user  = self.request.user 
        queryset = Orders.objects.filter(traderId = user.trader_id)
        return queryset
    
    serializer_class = UserOrderSerializer
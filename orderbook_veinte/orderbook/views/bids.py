#Rest framework
from rest_framework.generics import mixins 
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny
#models 
from orderbook.models.Order import Orders

#serializers
from orderbook.serializers import BidsSerializers 

class CreateBids( GenericViewSet,  mixins.CreateModelMixin , mixins.ListModelMixin):
    serializer_class = BidsSerializers
    queryset = Orders.objects.filter(Bid=True)
    permission_classes = [AllowAny , ]

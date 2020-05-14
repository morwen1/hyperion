#Rest framework
from rest_framework.generics import mixins 
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny
#models 
from orderbook_veinte.orderbook.models.Order import Orders

#serializers
from orderbook_veinte.orderbook.serializers import BidsSerializers ,UpdateBidSerializer

class CreateBids( 
    GenericViewSet,
    mixins.CreateModelMixin, 
    mixins.ListModelMixin,
    mixins.UpdateModelMixin):

            

    queryset = Orders.objects.filter(Bid=True)
    permission_classes = [AllowAny , ]

    def dispatch(self , request ,*args , **kwargs):
        self.qty_orderbook = kwargs['qty']
        self.price_orderbook = kwargs['price'] 
        return super(CreateBids , self).dispatch(request , *args , **kwargs)


    def get_serializer_context(self):
        return{
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'qty': self.qty_orderbook,
            'price':self.price_orderbook
        }



    def get_serializer_class(self):
        
        if self.action == 'list' or  self.action == 'create':
            serializer = BidsSerializers
        elif self.action == 'update' : 
            serializer = UpdateBidSerializer
        return serializer
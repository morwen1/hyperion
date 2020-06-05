#Rest framework
from rest_framework.generics import mixins 
from rest_framework.viewsets import GenericViewSet

#models 
from orderbook_veinte.orderbook.models.Order import Orders

#serializers
from orderbook_veinte.orderbook.serializers import BidsSerializers ,UpdateBidSerializer

#permissions 
from orderbook_veinte.utils.permissions import LazyAuthenticated
from rest_framework.permissions import AllowAny , IsAuthenticatedOrReadOnly



class CreateBids( 
    GenericViewSet,
    mixins.CreateModelMixin, 
    mixins.ListModelMixin,
    mixins.UpdateModelMixin):

            
    def get_permissions (self):
        permission = []
        if self.action in ['list','retrieve'] : 
            permission =  [AllowAny ,  IsAuthenticatedOrReadOnly ]
        elif self.action in[ 'create' , 'partial' , 'update']:
            permission = [LazyAuthenticated, ]
        
        return [p() for p in permission]

    


    def get_queryset(self):
        queryset = Orders.objects.filter(Bid=True)
        if self.action == "list":
            queryset = Orders.objects.filter(Bid=True).order_by("price")[:10]
        return queryset

    def dispatch(self , request ,*args , **kwargs):
        #import pdb; pdb.set_trace()
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
        serializer = BidsSerializers
        if self.action == 'list' or  self.action == 'create':
            serializer = BidsSerializers
        elif self.action == 'update' : 
            serializer = UpdateBidSerializer
        return serializer
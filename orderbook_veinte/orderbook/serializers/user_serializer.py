
#RESTFRAMEWORK
from rest_framework import serializers

#MODELS
from orderbook_veinte.orderbook.models import Orders , OrderStatus

class OrdersStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model  = OrderStatus
        fields = ('status' ,)

class UserOrderSerializer(serializers.ModelSerializer):
    status = OrdersStatusSerializer(read_only=True)
    class Meta:
        model =Orders 
        fields = ('Bid' , 'price' , 'qty' , 'close_qty' , 'status')
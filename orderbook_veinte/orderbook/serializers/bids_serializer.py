#DJANGO 

#REST FRAMEWORK
from rest_framework import serializers

#MODELS 

from orderbook_veinte.orderbook.models import Orders
#Orerbook
from orderbook_veinte.orderbook.tree import initializeTree
from orderbook_veinte.orderbook.tree import Bid
from orderbook_veinte.orderbook.tasks import AsincronicOrderProces




class BidsSerializers(serializers.ModelSerializer):
    class Meta : 
        model = Orders
        fields = ('traderId','timestamp' , 'qty' , 'price')
    def create(self , validated_data):

        bid = Bid(**validated_data  )
        #se activa la tarea de procesar orden
        AsincronicOrderProces.delay(
            order=bid.__dict__ , side ='bid' ,
            
            qty= self.context['qty'],
            price= self.context['price'])


        existence_order =False#Orders.objects.filter(**validated_data , Bid=True).exists()

        if  existence_order == False:
            order = Orders.objects.create(
                Bid = True , 
                market_qty= self.context['qty'],
                market_price =self.context['price'],
                Ask = False,
                **validated_data
            )
            #if order.orderId != bid.orderId:
            #    order.orderId = bid.orderId

            order.save()
        else: 
            order = Orders.objects.get(**validated_data , Bid=True)
            raise serializers.ValidationError(f'order {order.orderId} exists :c ' )


        return order   


class UpdateBidSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Orders
        fields = ('qty', )   
    
    def update(self , instance , validated_data ):
        ob = initializeTree()
        if ob.bids.orderExist(instance.orderId)== True:
            ob.bids.updateOrderQuatity(instance.orderId ,validated_data['qty'])
    
        return super(UpdateBidSerializer , self).update(instance , validated_data)
        

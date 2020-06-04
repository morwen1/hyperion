#DJANGO 

#REST FRAMEWORK
from rest_framework import serializers

#MODELS 
from orderbook_veinte.orderbook.models import Orders , OrderStatus
#Orerbook
from orderbook_veinte.orderbook.tree import Ask
from orderbook_veinte.orderbook.tasks import AsincronicOrderProces


class AsksSerializers(serializers.ModelSerializer):
    class Meta : 
        model = Orders
        fields = ('timestamp' , 'qty' , 'price')
    def create(self , validated_data):
        status = OrderStatus.objects.get(status = 'open')

        user = self.context['request'].user
        traderId = user.trader_id
        validated_data['traderId']=traderId
        ask = Ask(**validated_data  )
        AsincronicOrderProces.delay(order=ask.__dict__ , side ='ask', qty= self.context['qty'], price= self.context['price'] )


        order = Orders.objects.create(
                status = status,
                Ask = True , 
                market_qty= self.context['qty'],
                market_price =self.context['price'],
                Bid = False,
                close_qty = validated_data['qty'],
                **validated_data
            )

        order.save()
       
        return order   


class UpdateAskSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Orders
        fields = ('qty', )   
    
    def update(self , instance , validated_data ):
        ob = initializeTree()
        if ob.asks.orderExist(instance.orderId)== True:
            ob.asks.updateOrderQuatity(instance.orderId ,validated_data['qty'])
    
        return super(UpdateAskSerializer , self).update(instance , validated_data)
        

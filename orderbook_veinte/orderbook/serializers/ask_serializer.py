#DJANGO 

#REST FRAMEWORK
from rest_framework import serializers

#MODELS 
from orderbook.models import Orders
#Orerbook
from orderbook_veinte.orderbook.tree import initializeTree
from orderbook_veinte.orderbook.tree import Ask



class AsksSerializers(serializers.ModelSerializer):
    class Meta : 
        model = Orders
        fields = ('traderId','timestamp' , 'qty' , 'price')
    def create(self , validated_data):

        ob = initializeTree()
        ask = Ask(**validated_data  )
        ob.processOrder(ask)
        existence_order =Orders.objects.filter(**validated_data , Ask=True).exists()

        if  existence_order == False:
            order = Orders.objects.create(
                Ask = True , 

                Bid = False,
                **validated_data
            )
            if order.orderId != ask.orderId:
                order.orderId = ask.orderId

            order.save()
        else: 
            order = Orders.objects.get(**validated_data , Ask=True)
            raise serializers.ValidationError(f'order {order.orderId} exists :c ' )


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
        

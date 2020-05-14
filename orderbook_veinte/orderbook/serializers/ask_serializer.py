#DJANGO 

#REST FRAMEWORK
from rest_framework import serializers

#MODELS 
from orderbook_veinte.orderbook.models import Orders
#Orerbook
from orderbook_veinte.orderbook.tree import Ask
from orderbook_veinte.orderbook.tasks import AsincronicOrderProces


class AsksSerializers(serializers.ModelSerializer):
    class Meta : 
        model = Orders
        fields = ('traderId','timestamp' , 'qty' , 'price')
    def create(self , validated_data):
        ask = Ask(**validated_data  )
        AsincronicOrderProces.delay(order=ask.__dict__ , side ='ask', qty= self.context['qty'], price= self.context['price'] )

        existence_order =False #Orders.objects.filter(**validated_data , Ask=True).exists()

        if  existence_order == False:
            order = Orders.objects.create(
                Ask = True , 

                Bid = False,
                **validated_data
            )

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
        

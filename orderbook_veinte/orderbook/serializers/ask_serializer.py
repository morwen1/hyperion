#DJANGO 

#REST FRAMEWORK
from rest_framework import serializers

#MODELS 
from orderbook_veinte.orderbook.models import Orders , OrderStatus
#Orerbook
from orderbook_veinte.orderbook.tree import Ask
from orderbook_veinte.orderbook.tasks import AsincronicOrderProces


#Initialize Tree
from orderbook_veinte.orderbook.tree import initializeTree


class AsksSerializers(serializers.ModelSerializer):
    class Meta : 
        model = Orders
        fields = ( 'qty' , 'price')


#    def to_representation(self , instance):
#        representation = super(AsksSerializers , self).to_representation(instance)
#        representation['qty'] = format_output_qty(instance.qty , type_qty='btc')
#        return representation  


    def create(self , validated_data):
        status = OrderStatus.objects.get(status = 'open')

        user = self.context['request'].user
        traderId = user.trader_id
        validated_data['traderId']=traderId


        order = Orders.objects.create(
                status = status,
                Ask = True , 
                market_qty= self.context['qty'],
                market_price =self.context['price'],
                Bid = False,
                **validated_data
            )

        order.save()

        ask = Ask(**validated_data  )
     
        AsincronicOrderProces(
            order=ask.__dict__ , 
            side ='ask', 
            qty= self.context['qty'], 
            price= self.context['price'] )

        #AsincronicOrderProces.delay(order=ask.__dict__ , side ='ask', qty= self.context['qty'], price= self.context['price'] )

       
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
        

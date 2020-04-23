#DJANGO 

#REST FRAMEWORK
from rest_framework import serializers

#MODELS 
from orderbook.models import Orders
#Orerbook
from orderbook_veinte.orderbook.tree import initializeTree
from orderbook_veinte.orderbook.tree import Bid



class BidsSerializers(serializers.ModelSerializer):
    class Meta : 
        model = Orders
        fields = ('traderId','timestamp' , 'qty' , 'price')
    def create(self , validated_data):

        ob = initializeTree()
        bid = Bid(**validated_data  )
        ob.processOrder(bid)
        
        order = Orders.objects.create(
            Bid = True , 
            Ask = False,
            **validated_data
        )
        order.save()
        import pdb; pdb.set_trace()

        return order        
    
   
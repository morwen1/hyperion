#DJANGO 

#REST FRAMEWORK
from rest_framework import serializers


#MODELS 

from orderbook_veinte.orderbook.models import Orders , OrderStatus
#Orerbook
from orderbook_veinte.orderbook.tree import initializeTree
from orderbook_veinte.orderbook.tree import Bid
from orderbook_veinte.orderbook.tasks import AsincronicOrderProces
from orderbook_veinte.utils.manage_transaction import  format_output_qty

from orderbook_veinte.utils.hashing import  generatehash


#Initialize Tree
from orderbook_veinte.orderbook.tree import initializeTree



class BidsSerializers(serializers.ModelSerializer):


#
#   def to_representation(self , instance):
#       representation = super(BidsSerializers , self).to_representation(instance)
#        representation['qty'] = format_output_qty(instance.qty , type_qty='btc')
#       return representation        



 
    def create(self , validated_data):
        status_orders = OrderStatus.objects.all()
        status = status_orders.get(status = 'open')
        

        user = self.context['request'].user
        traderId = user.trader_id
        validated_data['traderId']=traderId


        #se activa la tarea de procesar orden
   


        existence_order =False 
        #import pdb; pdb.set_trace()
        order = Orders.objects.create(
            status = status,
            Bid = True , 
            market_qty= self.context['qty'],
            market_price =self.context['price'],
            **validated_data)


        return order
    def save(self, **kwargs ):

        validated_data = dict(
            list(self.validated_data.items()) +
            list(kwargs.items())
        )

        self.instance = self.create(validated_data) 
        order = self.instance
        order.close_qty = order.qty
        

        hash_order = generatehash([order.traderId , order.created_at.timestamp()])
        order.hash_order = hash_order
        validated_data['hash_order'] = hash_order
        bid = Bid(**validated_data  )

        
        
        order.save()
        
        AsincronicOrderProces.delay(
            order=bid.__dict__ , 
            side ='bid' ,
            qty= self.context['qty'],
            price= self.context['price'],
            )

        return order  



    class Meta : 
        model = Orders
        fields = ('qty' , 'price')
    
        
class UpdateBidSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Orders
        fields = ('qty', )   
    
    def update(self , instance , validated_data ):
        ob = initializeTree()
        if ob.bids.orderExist(instance.orderId)== True:
            ob.bids.updateOrderQuatity(instance.orderId ,validated_data['qty'])
    
        return super(UpdateBidSerializer , self).update(instance , validated_data)
        

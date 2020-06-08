#Django
from django.db import models 


#MODELS
from . import AbOrderbook





class OrderStatus (AbOrderbook):
    status = models.CharField(max_length=255)
    description  = models.TextField()


class Orders ( AbOrderbook):
    """
        Modelo de las ordernes 
        las ordenes pueden ser tipo ask o bid
        el __str__ o como se muestra el modelo en la terminal es {orden de la id , id del trader}
    """
    orderId = models.AutoField(primary_key = True , help_text = "id of the Trade auto increment field")
    traderId = models.CharField(max_length = 255) 
    qty = models.IntegerField()
    price = models.FloatField()
    close_qty = models.IntegerField(default=0)
    Bid = models.BooleanField(default=False)
    Ask = models.BooleanField(default=False)
    status = models.ForeignKey(
        to=OrderStatus,
        on_delete= models.SET_NULL ,
        null =True ,
        blank= True , )
    market_qty = models.CharField(max_length = 255)
    market_price = models.CharField(max_length = 255)
    def __str__(self):
        return f"{self.orderId } ,{self.market_price} , {self.market_qty}"
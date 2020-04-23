#Django
from django.db import models 


#MODELS
from . import AbOrderbook


class Orders ( AbOrderbook):
    """
        Modelo de las ordernes 
        las ordenes pueden ser tipo ask o bid
        el __str__ o como se muestra el modelo en la terminal es {orden de la id , id del trader}
    """
    orderId = models.AutoField(primary_key = True , help_text = "id of the Trade auto increment field")
    traderId = models.CharField(max_length = 255) 
    timestamp= models.TimeField()
    qty = models.FloatField()
    price = models.FloatField()
    Bid = models.BooleanField(default=False)
    Ask = models.BooleanField(default=False)
    
    def __str__(self):

        return f"{self.orderId } , {self.traderId}"
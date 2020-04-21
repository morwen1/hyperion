from django.db import models 

#models
from .Abstract_order import AbOrderbook


class Trades ( AbOrderbook):
    """
     trades in the order book 
    traders id's provisionales
    """
    qty   = models.FloatField()
    price = models.FloatField()
    timestamp = models.TimeField()
    p1_traderId  = models.CharField()
    p1_side = models.CharField()
    p1_orderId = models.CharField()
    p2_traderId  = models.CharField()
    p2_side  = models.CharField()
    p2_orderId = models.CharField()

    def get_traders(self) : 
        return f"{p1_traderId} , {p2_traderId}"
    
    
    def get_traders_with_side(self) :  
        return {self.p1_orderId : self.p1_side , self.p2_traderId : self.p2_side}
    
    
    def __str__(self):
        return f"{p1_orderId}-{p2_orderId}"
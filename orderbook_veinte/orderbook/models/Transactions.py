#Django
from django.db import models
#LOCAL 
from .Abstract_order import AbOrderbook


choices= [("partial" , "complete") , ]

class Transactions (AbOrderbook):
    """
        saving all transactions of the orderbook 
        that transaction have sides of the orders and 
        quantity, prices 
    """
    buyer = models.ForeignKey(
        to='orderbook.Orders' ,
        related_name= "transaction_buyer", 
        on_delete=models.CASCADE  
        )

    seller = models.ForeignKey(
        to='orderbook.Orders',
        related_name= "transaction_seller" ,
        on_delete=models.CASCADE
        )

    type_transaction = models.CharField(choices=choices , max_length = 120)
    qty = models.IntegerField()
    price = models.FloatField()
    market_qty = models.CharField(max_length = 255)
    market_price = models.CharField(max_length = 255)

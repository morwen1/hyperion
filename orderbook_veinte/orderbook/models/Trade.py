from django.db import models 



class Trades (models.Model):
    orderId = models.AutoField(primary_key = True , help_text = "id of the Trade auto increment field")
    traderId = models.CharField(max_length = 255) 
    timestamp= models.TimeField()
    qty = models.FloatField()
    price = models.FloatField
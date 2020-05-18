# settings
from django.conf import settings
import redis

# OrderBook
from .orderbook import OrderBook
from rest_framework import serializers

def initializeTree(qty, price):
    red = redis.StrictRedis.from_url(settings.REDIS['url'])
    print(qty , price)
    #todas contra todas menos con ella misma 

    ob = OrderBook(qty, price , red)
    return ob
   
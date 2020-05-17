# settings
from django.conf import settings
import redis

# OrderBook
from .orderbook import OrderBook
from rest_framework import serializers

def initializeTree(qty, price):
    red = redis.StrictRedis.from_url(settings.REDIS['url'])
    options = {
        "cripto": [
        'BTC',
        'LTC',
        'BSF',
        'PTR',
        'DSH'
        ], 
        "fiat": [
        "BSV",
        "USD",
        "PAR",
        "PCH"
    ]}
    print(qty , price)
    #todas contra todas menos con ella misma 
    if (qty in options['cripto'] or qty in options['fiat']) and (price in options['cripto'] or price in options['fiat']) and price != qty:

        ob = OrderBook(qty, price , red)
        return ob
    else :
        raise "not market registered"
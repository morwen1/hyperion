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
    if qty in options['cripto'] and price in options['fiat']:

        ob = OrderBook(qty, price , red)
        return ob
    else :
        raise "not market registered"
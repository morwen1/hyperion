#settings
from django.conf import settings
import redis

#OrderBook
from .orderbook import OrderBook 




def initializeTree():
    red = redis.StrictRedis.from_url(settings.REDIS['url'])
    
    ob = OrderBook('BTC' ,'XLT', red )
    return ob 




from celery.decorators import task 

from orderbook_veinte.orderbook.tree import initializeTree

from orderbook_veinte.orderbook.tree import Ask ,Bid


@task(name="processingOrder" )
def AsincronicOrderProces (order , side  ):
    del order['side']
    ob = initializeTree()
    if side == 'ask':
        orderobj = Ask(**order)
    elif side == 'bid':
        orderobj = Bid(**order)
    trades , orderInbook = ob.processOrder(orderobj)
    return trades 

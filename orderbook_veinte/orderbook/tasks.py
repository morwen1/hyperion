from celery.decorators import task 

from orderbook_veinte.orderbook.tree import initializeTree

from orderbook_veinte.orderbook.tree import Ask ,Bid




#Process order
@task(name="processingOrder" )
def AsincronicOrderProces (order , side , price , qty ):
    del order['side']
    ob = initializeTree(qty,price)
    if side == 'ask':
        orderobj = Ask(**order)
    elif side == 'bid':
        orderobj = Bid(**order)
    trades , orderInbook = ob.processOrder(orderobj)
    return trades 


#Transaction
def Transaction(transaction):
    pass


#Notifications
def Notifications(event):
    pass
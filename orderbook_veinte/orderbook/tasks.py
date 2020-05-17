

#celery
from celery.decorators import task 


#Initialize Tree
from orderbook_veinte.orderbook.tree import initializeTree


#Tree ASKS BIDS
from orderbook_veinte.orderbook.tree import Ask ,Bid

#models Ask , Bid
from orderbook_veinte.orderbook.models import Orders , OrderStatus

#model Transaction

from orderbook_veinte.orderbook.models import Transactions

#transaction 

from orderbook_veinte.utils.manage_transaction import TransactionsManger

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
    if len(trades) > 0 :
        Transaction.delay(trades)
    return trades 


#Transaction
@task(name="processingTransaction")
def Transaction(transaction):
    status = OrderStatus.objects.all()
       

    


#Notifications
def Notifications(event):
    pass
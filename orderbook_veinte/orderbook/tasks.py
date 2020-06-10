import time

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
def AsincronicOrderProces (order , side , price , qty  ):

    order_rel_exists = False 
    task_hash = order['hash_order']
    del order['side']
    while order_rel_exists == False :
        
        orders= Orders.objects.filter(hash_order = task_hash)
        if len(order) > 0 :
            order_rel_exists = True
        else : 
            time.sleep(0.2)

    
    ob = initializeTree(qty,price)
    if side == 'ask':
        orderobj = Ask(**order )
    elif side == 'bid':
        orderobj = Bid(**order )
    
    trades , orderInbook = ob.processOrder(orderobj)
    if len(trades) > 0 :
        buyer , seller = Transaction(trades)
        #import pdb; pdb.set_trace()




#Transaction
def Transaction(transaction):
    #tru = transaction unit
    #trm = transaction manager
    for tru in transaction : 
        side1 = tru['party2']
        side2 = tru['party1']

        qty = tru['qty']
        price = tru['price']
        time
        trm = TransactionsManger(side1 , side2 ,qty , price )
        
        return trm.saving_transactions()



#processing  order in remote site 


def RemoteTransaction(typeOrder:str):
    """
    request in a remote host a 
    """
    if typeOrder == 'lock':
        pass 
    elif typeOrder == 'unlock':
        pass 


#Notifications
def Notifications(event):
    pass
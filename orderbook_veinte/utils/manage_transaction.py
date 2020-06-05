#manejo de las transacciones
#manejo de las cantidades 
#manejo de los precios 
#DJANGO MODELS
from django.db.models import Count , Avg , Min ,Sum

from orderbook_veinte.orderbook.models import Transactions ,Orders , OrderStatus



class TransactionsManger :
    """
        Utilities to  general transactions in the orderbook 
    
    """
    def __init__(self, side1 , side2 , qty , price ):
        self.side1 =side1
        self.side2 = side2 
        self.qty = qty 
        self.price = price 

        
    def saving_transactions (self):
        status_orders = OrderStatus.objects.all()
        #verificacion de los lados de la transaccion
        if self.side1['side'] == 'ask':
            
            seller = Orders.objects.get( orderId = int(self.side1['orderId']))
            seller.close_qty = int( seller.qty  -  self.qty)
            buyer =Orders.objects.get( orderId = int(self.side2['orderId']))
            buyer.close_qty = int( buyer.qty  -  self.qty)



        elif self.side1['side'] == 'bid':
            buyer = Orders.objects.get( orderId = int(self.side1['orderId']))
            buyer.close_qty = int( buyer.qty  -  self.qty)

            buyer.save()
            seller =Orders.objects.get( orderId = int(self.side2['orderId']))
            seller.close_qty = int( seller.qty  -  self.qty)
            seller.save()

        #  WARNING celery tiene problemas con orm aveces 
        #validacion de los tipos de transacciones y los estados de las ordenes
        if seller.close_qty != 0 :
            transaction_type = 'partial'
            seller.status=status_orders.get(status = 'open')
            seller.save()

        if buyer.close_qty != 0 : 
            transaction_type = 'partial'
            buyer.status = status_orders.get(status='open')
            buyer.save()

        if seller.close_qty == 0  :
            transaction_type = 'partial'
            seller.status=status_orders.get(status = 'completed')
            seller.save()

        if buyer.close_qty == 0 : 
            transaction_type = 'partial'
            buyer.status = status_orders.get(status = 'completed')
            buyer.save()

        if (seller.close_qty == 0) and ( buyer.close_qty == 0)  : 
            transaction_type = 'complete'
            buyer.status = status_orders.get(status = 'completed')
            seller.status=status_orders.get(status = 'completed')
            buyer.save()
            seller.save()
        
        

    
        transaction = Transactions.objects.create(
            buyer = buyer ,
            seller = seller,
            qty = self.qty ,
            type_transaction = transaction_type ,
            price = self.price ,
            market_price = buyer.market_price,
            market_qty = buyer.market_qty,
        
        )



    def get_number_of_transactions(self):
        transactions = Transacctions.objects.count()
        return transactions
    
    def get_number_partial_complete_transactions(self):
        partial = Transactions.objects.filter(type_transaction='partial').count()
        complete = Transactions.objects.filter(type_transaction='complete').count()
        return partial, complete

    def get_avg_transactions_partials(self):
        qty_avg = Transactions.objects.filter(type_transaction='partial').aggregate(Avg('qty'))
        price_avg = Transactions.objects.filter(type_transaction='partial').aggregate(Avg('price'))
        return qty_avg ,price_avg


    def processTransaction(self):
        pass
    





def format_output_qty (qty , type_qty : str ):
    
    unity1 = 1e-8
    unity2 = 1e8
    if qty == float :
        return (qty + unity1) 

    if type_qty == 'btc' :
        rqty = float(qty * unity1)
        return '{:.8f}'.format(rqty)
    if type_qty == 'satoshi' and qty != int :
        rqty = int(float(qty) * unity2)
        return rqty




